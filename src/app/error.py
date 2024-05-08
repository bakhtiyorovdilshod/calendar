from fastapi import HTTPException as FastAPIHTTPException


class CustomHTTPException(FastAPIHTTPException):
    def response_body(self) -> dict:
        return {"error": self.detail}
