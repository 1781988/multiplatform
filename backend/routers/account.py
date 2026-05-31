from fastapi import APIRouter
from pydantic import BaseModel

from database.db import list_platform_accounts, logout_platform_account, upsert_platform_account

router = APIRouter(prefix="/account")


class MockLoginRequest(BaseModel):
    platform: str
    account_name: str


class AccountLogoutRequest(BaseModel):
    platform: str


@router.post("/mock-login")
def mock_login(payload: MockLoginRequest):
    token = f"mock_{payload.platform}_token"
    data = upsert_platform_account(
        platform=payload.platform,
        account_name=payload.account_name,
        auth_type="mock",
        token=token,
        status="logged_in",
    )
    return {"code": 200, "message": "模拟登录成功", "data": data}


@router.get("/list")
def account_list():
    return {"code": 200, "data": list_platform_accounts()}


@router.post("/logout")
def account_logout(payload: AccountLogoutRequest):
    data = logout_platform_account(payload.platform)
    return {"code": 200, "message": "账号已退出登录", "data": data}
