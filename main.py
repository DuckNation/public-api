import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from api import router as protected_api
from database import RedisSingleton
from slowapi import Limiter, _rate_limit_exceeded_handler

app = FastAPI(title="Quacking API", version="0.0.1")

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    protected_api
)


@app.on_event("shutdown")
async def shutdown_event():
    await RedisSingleton.close_redis_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6420)
