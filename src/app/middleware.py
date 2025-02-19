import json

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.app.config import settings
from src.app.error import CustomHTTPException
from src.usecase.utils.user import User

# Define the timeout value
timeout = httpx.Timeout(10.0)

VERIFY_USER_PATH = "api/v1/auth/internal/verify"
VERIFY_USER_SCHEME = "https" if settings.AUTH_USE_TLS else "http"
VERIFY_USER_URL = f"{VERIFY_USER_SCHEME}://{settings.AUTH_HOST}:{settings.AUTH_PORT}/{VERIFY_USER_PATH}"


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/v1/calendar"):
            try:
                async with httpx.AsyncClient(
                    timeout=timeout
                ) as client:  # Set the timeout here
                    session_id = request.cookies.get("sessionid")
                    if not session_id:
                        return JSONResponse(
                            {"detail": "Session ID missing"}, status_code=401
                        )

                    data = json.dumps({"session_id": session_id})

                    headers = {
                        "Content-Type": "application/json",
                        "Accept-Language": request.headers.get(
                            "Accept-Language", "uzlat"
                        ),
                    }
                    auth = (
                        settings.AUTH_INTERNAL_USERNAME,
                        settings.AUTH_INTERNAL_PASSWORD,
                    )

                    response = await client.post(
                        url=VERIFY_USER_URL,
                        data=data,
                        headers=headers,
                        auth=auth,
                        timeout=None,  # Override the client-level timeout
                    )

                    if response.status_code != 200:
                        raise HTTPException(
                            status_code=401, detail="Invalid session ID"
                        )

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
            except httpx.ReadTimeout:
                raise CustomHTTPException(
                    status_code=404, detail="Authentication service timeout"
                )
        else:
            return JSONResponse({"detail": "Not Found"}, status_code=404)
