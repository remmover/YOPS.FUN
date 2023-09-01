import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

from src.routes import auth, users
from src.conf.config import config

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router, prefix="/api")


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
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True, log_level="info")