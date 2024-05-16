import json

import httpx
from fastapi import HTTPException, Request

from src.app.config import settings
from src.app.error import CustomHTTPException

VERIFY_STAFF_PATH = "api/v1/state/internal/employee/validate/"
VERIFY_STAFF_SCHEME = "https" if settings.AUTH_USE_TLS else "http"
VERIFY_STAFF_URL = f"{VERIFY_STAFF_SCHEME}://{settings.STATE_HOST}:{settings.STATE_PORT}/{VERIFY_STAFF_PATH}"

timeout = httpx.Timeout(10.0)


class StateClient:
    async def employee_validate(self, pinfls, organization_id):
        async with httpx.AsyncClient(timeout=timeout) as client:
            data = json.dumps(
                {"pinfls": pinfls, "organization_id": organization_id}
            )
            headers = {
                "Content-Type": "application/json",
                "Accept-Language": "uzlat",
            }
            auth = (
                settings.STATE_INTERNAL_USERNAME,
                settings.STATE_INTERNAL_PASSWORD,
            )
            print(data)

            response = await client.post(
                url=VERIFY_STAFF_URL,
                data=data,
                headers=headers,
                auth=auth,
                timeout=None,
            )
            print(response.text)

            if response.status_code != 200:
                raise CustomHTTPException(
                    status_code=response.status_code,
                    detail=f"some of users did not find: {response.text}",
                )
            return response.json()
