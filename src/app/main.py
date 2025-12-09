from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from src.app.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    """Lifespan manager of application context"""

    logger.info("App startup initiated")
    pass
    logger.info("App startup complete")

    yield

    logger.info("App shutdown initiated")
    pass
    logger.info("App shutdown complete")


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app)
