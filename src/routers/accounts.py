from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import UUID4
from auth.dependencies import UserTokenDependency
from context import ApplicationContext, get_application_context

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/{guid}")
def get_user(
    guid: UUID4,
    token: UserTokenDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    user = ctx.accounts.get(guid)
    return user
