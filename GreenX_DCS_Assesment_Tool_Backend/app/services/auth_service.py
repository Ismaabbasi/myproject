from datetime import timedelta
from typing import List
from fastapi import HTTPException, status
from datetime import datetime

from app.core.config import configs
from app.core.exceptions import AuthError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.model.user import User

from app.repository.user_repository import UserRepository
from app.repository.user_profile_repository import UserProfileRepository
from app.repository.user_measures_repository import UserMeasuresRepository
from app.repository.roles_repository import RolesRepository

from app.schema.auth_schema import Payload, SignIn, SignUp
from app.schema.user_schema import FindUser
from app.schema.otp_schema import OtpBase, ResetPassword
from app.services.base_service import BaseService
from app.util.hash import get_rand_hash
import traceback
import re

from email.message import EmailMessage
import ssl
import smtplib


def validate_email(email):
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
        return {
            "status": True,
            "message": "Valid Email"
        }
    return {
        "status": False,
        "message": "Invalid Email. Please enter a valid email address."
    }

def validate_name(name):
    if re.search(r'[^a-zA-Z\s]', name) or re.search(r'\d', name) or name == "string" or name == "" or name == " ":
        return {
            "status": False,
            "message": "Invalid name. Special characters, numbers and empty values not allowed in name."
        }
    return {
        "status": True,
        "message": "Valid String"
    }

class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_in(self, sign_in_info: SignIn):
        find_user = FindUser()
        find_user.email = sign_in_info.email
        user: List[User] = self.user_repository.read_by_options(find_user)["founds"]
        if len(user) < 1:
            raise AuthError(detail="Incorrect email or password")
        found_user = user[0]
        if not found_user.is_active:
            raise AuthError(detail="Account is not active")
        if not verify_password(sign_in_info.password, found_user.password):
            raise AuthError(detail="Incorrect email or password")
        delattr(found_user, "password")


        # Checking if the user has a profile
        user_profile_repo = UserProfileRepository(session_factory=self.user_repository.session_factory)
        user_has_profile = user_profile_repo.user_profile_exists(user_profile_id = found_user.id)

        # Getting domain and role of the user
        domain_id = -1
        role_id = -1

        role_name = ""

        has_top_of_mind = False
        has_value_drivers = False
        has_main_challenges = False

        if user_has_profile:
            result = user_profile_repo.get_domain_and_role_id(user_id = found_user.id)
            domain_id = result["domain_id"]
            role_id = result["role_id"]

            # Getting the role name
            role_repo = RolesRepository(session_factory=self.user_repository.session_factory)
            role_name = role_repo.get_role_by_id(role_id)["role_name"]

            # Checking if user has selected top of mind measures
            user_measures_repo = UserMeasuresRepository(session_factory=self.user_repository.session_factory)
            has_top_of_mind = user_measures_repo.user_has_measures(user_id= found_user.id, sustainability_measures_type_id= 1)


            # Check if user has selected primary value drivers
            has_value_drivers = user_measures_repo.user_has_measures(user_id= found_user.id, sustainability_measures_type_id= 2)

            # Check if user has main challenges
            has_main_challenges = user_measures_repo.user_has_measures(user_id= found_user.id, sustainability_measures_type_id= 3)

        payload = Payload(
            id=found_user.id,
            email=found_user.email,
            name=found_user.name,
            is_superuser=found_user.is_superuser,
        )

        token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.dict(), token_lifespan)
        sign_in_result = {
            "access_token": access_token,
            "expiration": expiration_datetime,
            "user_info": found_user,
            "group_id": domain_id,
            "role_id": role_id,
            "role": role_name,
            "has_profile": user_has_profile,
            "has_top_of_mind": has_top_of_mind,
            "has_value_drivers": has_value_drivers,
            "has_main_challenges": has_main_challenges
        }

        return sign_in_result

    def sign_up(self, user_info: SignUp):
        try: 
            # User token is created here
            user_token = get_rand_hash()

            user = User(**user_info.dict(exclude_none=True), is_active=True, is_superuser=False, user_token=user_token)

            # Validate email and name
            is_valid_email = validate_email(user.email)
            is_valid_name = validate_name(user.name)
            if not is_valid_email["status"]:
                raise ValueError(validate_email(user_info.email)["message"])
            if not is_valid_name["status"]:
                raise ValueError(validate_name(user_info.name)["message"])
            
            print("USERRRRRR", user)

            # Hash the password
            user.password = get_password_hash(user_info.password)

            # User is created in DB
            created_user = self.user_repository.create(user)

            delattr(created_user, "password")
            return created_user
        
        except HTTPException as http_exc:
                raise http_exc

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while signing up in auth service: {e}"
            )
        
    # Changing password of the user
    # 1) Get the email by the user
    # 2) Check if the user exists
    # 3) If exists, add a record in the table which will consist of the foreign key user id, email and the code.
    # 4) Send the email to the user with the code

    def logout(self, access_token: str):
        try:
            return self.user_repository.logout(access_token)
        
        except AuthError as ae:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ae.detail
            )
        
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in auth_service: {e}"
            )


    def send_code(self, email: str, code: str, name_of_user: str):
        try:
            email_sender = "ahmedkayani786@gmail.com"
            password = "zdao eyut tgmh tnzg"

            email_receiver = email

            subject = "Cisco Sustainability Password Change Request"
            body = f"Hi {name_of_user}, \n\nYou have requested to change your password. Please use the following OTP to change your password: {code}\n\nThis OTP will expire in 10 minutes.\n\nRegards,\nCisco Sustainability Team"

            em = EmailMessage()
            em["from"] = email_sender
            em["to"] = email_receiver
            em["subject"] = subject
            em.set_content(body)

            print(f"In the send code, the em is {em}")

            context = ssl.create_default_context()

            print(f"In the send code, the context is {context}")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(email_sender, password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
        except:
            pass

    # Sending code for password change
    def verify_email(self, email: str):
        try:
            find_user = FindUser()

            print(f"This is the find_user: {find_user}")

            find_user.email = email

            print(f"This is the find_user email: {find_user.email}")

            user: List[User] = self.user_repository.read_by_options(find_user)["founds"]

            print(f"This is the user: {user}")
            print(f"This is the length of the user: {len(user)}")

            if len(user) < 1:
                raise AuthError(detail="Email doesn't exist.")
            found_user = user[0]
            if not found_user.is_active:
                raise AuthError(detail="Account is not active")
            
            # Generate a random 6 digit code
            code = get_rand_hash(length=4)

            print(f"This is the code: {code}")

            name_of_user = found_user.name

            print(f"This is the name of the user: {name_of_user}")

            # Expiration time for the otp code
            # Expiration time is after 10 minutes
            expiration_time = datetime.now() + timedelta(minutes=10)

            print(f"This is the expiration time: {expiration_time}")

            self.send_code(email, code, name_of_user)

            print(f"This is the email: {email}")

            self.user_repository.add_otp_code(email, code, expiration_time)

            return {
                "status": True,
                "message": "OTP Code has been sent to your email."
            }
        
        except AuthError as ae:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ae.detail
            )
        
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in auth_service while verifying email: {e}"
            )
    
    def validateOTPCode(self, otp_payload: OtpBase):
        try:

            current_time = datetime.now()
            return self.user_repository.check_otp_code(otp_payload, current_time)
        
        except AuthError as ae:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ae.detail
            )
        
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in auth_service while validating OTP code: {e}"
            )
    
    def reset_password(self, otp_payload: ResetPassword):
        email = otp_payload.email
        password = otp_payload.password
        password_repeat = otp_payload.password_repeat

        if password != password_repeat:
            raise AuthError(detail="Passwords do not match.")

        hashed_password = get_password_hash(password)
        try:
            has_changed = self.user_repository.reset_password(email, hashed_password)

            if has_changed is True:
                return {
                    "status": True,
                    "message": f"Password of {email} has been changed successfully."
                }
            
            else:
                return {
                    "status": False,
                    "message": f"Password of {email} could not be changed. Please try again."
                }
        
        except AuthError as ae:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ae.detail
            )
        
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in auth_service while resetting password: {e}"
            )



        
