#!/usr/bin/env python

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

from src.conf.config import config
from src.routes import auth, users, images, tags, comments

app = FastAPI(title="YOPS.FUN App",
    description = "<h2>Your Opinions, Pictures, Status for FUN</h2><br>" \
                  "https://YOPS.FUN",
    summary='Time Trillers',
    version="5.0.5",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router, prefix="/api")
app.include_router(images.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(comments.router, prefix="/api")


@app.on_event("startup")
async def startup():
    """
    Initialize Redis connection and FastAPILimiter on startup.

    This function creates a connection to the Redis server using the
    configuration parameters and initializes the FastAPILimiter with the
    Redis connection.

    Returns:
        None
    """
    r = await redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    """
    Default route to greet the user.

    Returns:
        dict: A dictionary containing a greeting message.
    """
    return {"message": "Your Own Pictures and Status API."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True, log_level="info")
