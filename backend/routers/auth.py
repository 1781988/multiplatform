from uuid import uuid4

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database.db import create_user, find_user_by_account, find_user_by_token

router = APIRouter(prefix="/auth")


class RegisterRequest(BaseModel):
    username: str
    account: str
    password: str


class LoginRequest(BaseModel):
    account: str
    password: str


@router.post("/register")
def register(payload: RegisterRequest):
    if find_user_by_account(payload.account):
        return JSONResponse(status_code=400, content={"code": 400, "message": "账号已存在"})

    token = f"mock_{uuid4().hex}"
    user = create_user(payload.username, payload.account, payload.password, token)
    return {"code": 200, "message": "注册成功", "data": user}


@router.post("/login")
def login(payload: LoginRequest):
    user = find_user_by_account(payload.account)
    if not user or user["password"] != payload.password:
        return JSONResponse(status_code=401, content={"code": 401, "message": "账号或密码错误"})

    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "id": user["id"],
            "username": user["username"],
            "account": user["account"],
            "token": user["token"],
        },
    }


@router.get("/profile")
def profile(authorization: str | None = Header(default=None)):
    token = (authorization or "").replace("Bearer ", "").strip()
    user = find_user_by_token(token) if token else None
    if not user:
        return JSONResponse(status_code=401, content={"code": 401, "message": "未登录"})

    return {"code": 200, "data": user}
