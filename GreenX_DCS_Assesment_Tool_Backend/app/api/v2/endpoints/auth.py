from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.auth_schema import SignIn, SignUp, SignInResponse
from app.schema.user_schema import User as UserSchema
from app.schema.user_schema import BaseUser, NewPasswordResponse
from app.schema.otp_schema import OtpBase, ResetPassword
from app.services.auth_service import AuthService
from app.core.security import JWTBearer

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in", response_model=SignInResponse)
@inject
async def sign_in(user_info: SignIn, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_in(user_info)


@router.post("/sign-up", response_model=UserSchema)
@inject
async def sign_up(user_info: SignUp, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_up(user_info)

@router.post("/logout", response_model=dict)
@inject
async def logout(current_user: User = Depends(get_current_active_user), service: AuthService = Depends(Provide[Container.auth_service]), access_token: str = Depends(JWTBearer())):
    return service.logout(access_token)


@router.get("/me", response_model=UserSchema)
@inject
async def get_me(current_user: User = Depends(get_current_active_user)):
    user = UserSchema()
    user.name = current_user.name
    user.email = current_user.email
    user.created_at = current_user.created_at
    return user

# Changing password of the user if forgotten
@router.post("/verify-email", response_model=dict)
@inject
async def verify_email(email: str, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.verify_email(email) 

@router.post("/send-otp", response_model=bool)
@inject
async def send_otp(otp_payload: OtpBase, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.validateOTPCode(otp_payload)
 
@router.post("/reset-password", response_model=dict)
@inject
async def reset_password(otp_payload: ResetPassword, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.reset_password(otp_payload)      
