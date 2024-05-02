from src.app.middleware import AuthMiddleware
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


app = FastAPI(lifespan=lifespan)
app.add_middleware(AuthMiddleware)
app.openapi_version = "3.1.0"

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
