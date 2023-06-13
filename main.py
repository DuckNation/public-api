import uvicorn
from fastapi import FastAPI

from api import router as protected_api
from database import RedisSingleton

app = FastAPI(title="Quacking API", version="0.0.1", docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")

app.include_router(
    protected_api
)


@app.on_event("shutdown")
async def shutdown_event():
    await RedisSingleton.close_redis_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6420)
