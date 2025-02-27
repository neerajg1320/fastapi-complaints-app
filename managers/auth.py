from typing import Optional

import jwt
from datetime import datetime, timedelta
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from db import database
from models import user, RoleType


class AuthManager:
    @staticmethod
    def encode_token(_user):
        try:
            payload = {
                "sub": _user["id"],
                "exp": datetime.utcnow() + timedelta(minutes=120),
            }

            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
        except Exception as ex:
            # Log the exception
            raise ex


class CustomHttpBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        # return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
        res = await super().__call__(request)

        try:
            payload = jwt.decode(
                res.credentials, config("SECRET_KEY"), algorithms=["HS256"]
            )
            user_data = await database.fetch_one(
                user.select().where(user.c.id == payload["sub"])
            )
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError as ex:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Token is not valid")


# User with the Depends in the resources
oauth2_scheme = CustomHttpBearer()


def is_complainer(request: Request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(403, "Forbidden")


def is_approver(request: Request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(403, "Forbidden")


def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(403, "Forbidden")
