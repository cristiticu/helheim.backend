from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.dependencies import refresh_token_data
from auth.model import RefreshTokenData
from context import ApplicationContext, get_application_context
from accounts.model import CreateAccount


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("")
def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    tokens = ctx.authentication.authenticate(
        form_data.username,
        form_data.password
    )

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "access_token": tokens["access_token"],
                            "refresh_token": tokens["refresh_token"],
                            "token_type": "bearer"
                        }
                        )


@router.post("/register")
def register(
    user_payload: CreateAccount,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    user = ctx.accounts.create(user_payload)
    return user


@router.post("/refresh")
def refresh(
    refresh_token: Annotated[RefreshTokenData, Depends(refresh_token_data)],
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    tokens = ctx.authentication.refresh(
        refresh_token.raw_token,
        refresh_token.user_guid
    )

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "access_token": tokens["access_token"],
                            "refresh_token": tokens["refresh_token"],
                            "token_type": "bearer"
                        }
                        )
