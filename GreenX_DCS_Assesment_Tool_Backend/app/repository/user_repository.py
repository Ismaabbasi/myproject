from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session

from app.model.user import User
from app.repository.base_repository import BaseRepository
from app.schema.otp_schema import OtpBase
from fastapi import HTTPException, status
from sqlalchemy import text

class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    def get_user_by_id(self, user_id: int):
        try: 
            with self.session_factory() as session:
                user = session.execute(f"select * from user where id = {user_id}").fetchone()

                if user is None:
                    raise ValueError("No such id exists in the user table.")
                return {
                    "name": user.name,
                    "email": user.email,
                }
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail= f"An error occurred while retrieving the user: {e}"
            )
        
    def logout(self, access_token: str):
        try:
            with self.session_factory() as session:
                session.execute(text("INSERT INTO token_blacklist (access_token) VALUES (:access_token)"), {'access_token': access_token})
                session.commit()
                return {
                    "status": True,
                    "message": "Logged out successfully."
                }
        except IntegrityError as e:
            # Log the error for debugging
            print(f"IntegrityError: {e}")
            raise HTTPException(
                status_code=400,
                detail="A database integrity error occurred."
            )
        except Exception as e:
            # Log the general exception for debugging
            print(f"Exception: {e}")
            raise HTTPException(
                status_code=500, 
                detail="An error occurred while logging out."
            )
    
    def check_if_token_blacklisted(self, access_token: str):
        try:
            with self.session_factory() as session:
                token = session.execute(text("SELECT 1 FROM token_blacklist WHERE access_token = :access_token"), {'access_token': access_token}).fetchone()
                print(f"Thissssssssssssssssssssssssss is the tokeeeeeeeeeeeeeen: {token}")
                if token is None:
                    return False
                return True
        except Exception as e:
            # Log the general exception for debugging
            print(f"Exception: {e}")
            raise HTTPException(
                status_code=500, 
                detail="An error occurred while checking the token blacklist."
            )
        
    def add_otp_code(self, email: str, code: str, expiration_time):
        try:
            with self.session_factory() as session:
                # Check if email exists in the user table
                email_exists = session.execute(text("SELECT 1 FROM otp_password WHERE user_email = :email"), {'email': email}).fetchone()
                if email_exists is None:
                    # Insert new OTP code
                    session.execute(text("INSERT INTO otp_password (user_email, code, expiration_date) VALUES (:email, :code, :expire)"), {'email': email, 'code': code, 'expire': expiration_time})
                else:
                    # Update existing OTP code
                    session.execute(
                        text("UPDATE otp_password SET code = :code, expiration_date = :expiration_time WHERE user_email = :email"),
                        {'email': email, 'code': code, 'expiration_time': expiration_time}
                    )
                session.commit()
        except IntegrityError as e:
            # Log the error for debugging
            print(f"IntegrityError: {e}")
            raise HTTPException(
                status_code=400,
                detail="A database integrity error occurred."
            )
        except Exception as e:
            # Log the general exception for debugging
            print(f"Exception: {e}")
            raise HTTPException(
                status_code=500, 
                detail="An error occurred while adding the OTP code."
            )

    def check_otp_code(self, otp_payload: OtpBase, current_time):
        try:
            with self.session_factory() as session:
                # Check if email exists in the user table
                email = otp_payload.email
                code = otp_payload.code
                email_exists = session.execute(text("SELECT * FROM otp_password WHERE user_email = :email AND code = :code"), {'email': email, 'code': code}).fetchone()
                if email_exists is None:
                    return False

                expiration_date = email_exists.expiration_date

                print(f"THIS IS THE expiration_date -------------> {expiration_date}")
            
                if current_time > expiration_date:
                    return False  # OTP code has expired

                return True
        except Exception as e:
            # Log the general exception for debugging
            print(f"Exception: {e}")
            raise HTTPException(
                status_code=500, 
                detail="An error occurred while checking the OTP code."
            )
        
    def reset_password(self, email:str, password: str):
        # Update the password of the user with the email
        try:
            with self.session_factory() as session:
                session.execute(text("UPDATE user SET password = :password WHERE email = :email"), {'email': email, 'password': password})
                session.execute(text("DELETE FROM otp_password WHERE user_email = :email"), {'email': email})
                session.commit()

                return True
        except IntegrityError as e:
            # Log the error for debugging
            print(f"IntegrityError: {e}")
            raise HTTPException(
                status_code=400,
                detail="A database integrity error occurred."
            )
        except Exception as e:
            # Log the general exception for debugging
            print(f"Exception: {e}")
            raise HTTPException(
                status_code=500, 
                detail="An error occurred while resetting the password."
            )


