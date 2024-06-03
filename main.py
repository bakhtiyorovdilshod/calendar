from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.app.error import CustomHTTPException
from src.app.middleware import AuthMiddleware
from src.infrastructure.postgres.database import async_session, engine
from src.usecase.api.notes import router as router_notes

all_routers = [
    router_notes,
]

import uvicorn
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect database
    async_session.configure(bind=engine)
    yield
    # disconnect database
    async with async_session() as session:
        await session.close()


def http_exception_handler(request, exc):
    return JSONResponse(exc.response_body(), status_code=exc.status_code)


app = FastAPI(
    lifespan=lifespan,
    docs_url="/swagger/",
    openapi_url="/openapi.json",
    redoc_url=None,
    root_path="/api/v1/calendar",
)

# Initialize the CORSMiddleware with the appropriate arguments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the AuthMiddleware after CORSMiddleware
app.add_middleware(AuthMiddleware)
app.add_exception_handler(CustomHTTPException, http_exception_handler)

for router in all_routers:
    app.include_router(router, prefix="")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )


    
