import json
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.app.config import settings
import httpx

from src.usecase.utils.user import User


VERIFY_USER_PATH = "api/v1/auth/internal/verify"
VERIFY_USER_SCHEME = "https" if settings.AUTH_USE_TLS else "http"
VERIFY_USER_URL = f"{VERIFY_USER_SCHEME}://{settings.AUTH_HOST}:{settings.AUTH_PORT}/{VERIFY_USER_PATH}"


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        async with httpx.AsyncClient() as client:
            session_id = request.cookies.get("sessionid")
            if not session_id:
                raise HTTPException(status_code=401, detail="Session ID missing")

            data = json.dumps({"session_id": session_id})

            headers = {
                "Content-Type": "application/json",
                "Accept-Language": request.headers.get("Accept-Language", "uzlat"),
            }
            auth = (settings.AUTH_INTERNAL_USERNAME, settings.AUTH_INTERNAL_PASSWORD)

            response = await client.post(
                url=VERIFY_USER_URL,
                data=data,
                headers=headers,
                auth=auth,
                timeout=5,
            )

            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid session ID")

            session_data = response.json()
            user_data = session_data["user"]
            user = User(
                id=user_data.get("id"),
                pinfl=user_data.get("pinfl"),
                last_organization_id=user_data.get("last_organization_id"),
                roles=user_data.get("roles"),
                organizations=user_data.get("organizations"),
            )
            request.state.user = user
            return await call_next(request)


