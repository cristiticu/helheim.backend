from typing import Annotated
from fastapi import APIRouter, Depends
from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext

router = APIRouter(prefix="/account", tags=["Account"])
application_context = ApplicationContext()


@router.get("")
def get_user(token: Annotated[UserTokenData, Depends(user_token_data)]):
    user = application_context.accounts.get(token.user_guid)
    return user
