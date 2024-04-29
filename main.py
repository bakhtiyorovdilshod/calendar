from src.app.config import Settings
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

settings = Settings()
app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=int(settings.SERVER_PORT),
        reload=True,
    )
