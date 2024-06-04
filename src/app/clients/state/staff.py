import json

import httpx
from fastapi import HTTPException, Request

from src.app.config import settings
from src.app.error import CustomHTTPException

VERIFY_EMPOYMENTVALIDATION_PATH = "api/v1/state/internal/employment/validate/"
VERIFY_EMPOYMENTVALIDATION_SCHEME = "https" if settings.AUTH_USE_TLS else "http"
VERIFY_EMPOYMENTVALIDATION_URL = f"{VERIFY_EMPOYMENTVALIDATION_SCHEME}://{settings.STATE_HOST}:{settings.STATE_PORT}/{VERIFY_EMPOYMENTVALIDATION_PATH}"

VERIFY_EMPOYMENTLIST_PATH = "api/v1/state/internal/employments/"
VERIFY_EMPOYMENTLIST_PATH_SCHEME = "https" if settings.AUTH_USE_TLS else "http"
VERIFY_EMPOYMENTLIST_PATH_URL = f"{VERIFY_EMPOYMENTLIST_PATH_SCHEME}://{settings.STATE_HOST}:{settings.STATE_PORT}/{VERIFY_EMPOYMENTLIST_PATH}"

timeout = httpx.Timeout(10.0)


class StateClient:
    async def get_employments(self, organization_id: int, pinfl: str, search: str):
        async with httpx.AsyncClient(timeout=timeout) as client:
            headers = {
                "Content-Type": "application/json",
                "Accept-Language": "uzlat",
            }
            auth = (
                settings.STATE_INTERNAL_USERNAME,
                settings.STATE_INTERNAL_PASSWORD,
            )

            response = await client.get(
                url=VERIFY_EMPOYMENTLIST_PATH_URL,
                headers=headers,
                params={"orgId": organization_id, "pinfl": pinfl, "search": search},
                auth=auth,
                timeout=None,
            )

            if response.status_code != 200:
                raise CustomHTTPException(
                    status_code=response.status_code,
                    detail=response.text,
                )
            return response.json()
    
    async def employment_validate(self, organization_id, employment_ids, pinfl: str):
        async with httpx.AsyncClient(timeout=timeout) as client:
            headers = {
                "Content-Type": "application/json",
                "Accept-Language": "uzlat",
            }
            auth = (
                settings.STATE_INTERNAL_USERNAME,
                settings.STATE_INTERNAL_PASSWORD,
            )
            data = json.dumps(
                {"employmentIds": employment_ids, "orgId": organization_id, "pinfl": pinfl}
            )

            response = await client.post(
                url=VERIFY_EMPOYMENTVALIDATION_URL,
                data=data,
                headers=headers,
                auth=auth,
                timeout=None,
            )

            if response.status_code != 200:
                raise CustomHTTPException(
                    status_code=response.status_code,
                    detail=response.text,
                )
            return response.json()
