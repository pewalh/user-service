from fastapi import FastAPI

from user_service.api.v1.endpoints.user import router as user_router

app = FastAPI()
app.include_router(user_router, prefix="/api/v1")

