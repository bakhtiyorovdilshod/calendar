from src.app.middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.postgres.database import engine, async_session
from src.usecase.api.notes import router as router_notes
from contextlib import asynccontextmanager

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


app = FastAPI(lifespan=lifespan, docs_url="/api/v1/calendar/swagger/", openapi_url="/api/v1/calendar/openapi.json")

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

for router in all_routers:
    app.include_router(router, prefix="/api/v1/calendar")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
