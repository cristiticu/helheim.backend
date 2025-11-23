from fastapi import APIRouter
from pydantic import UUID4
from auth.dependencies import UserTokenDependency
from context import ApplicationContext

router = APIRouter(prefix="/account", tags=["Account"])
application_context = ApplicationContext()


@router.get("/{guid}")
def get_user(guid: UUID4, token: UserTokenDependency):
    user = application_context.accounts.get(guid)
    return user
