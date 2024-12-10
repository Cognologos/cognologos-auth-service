from fastapi import FastAPI

from auth_service.routers import router


app = FastAPI()

app.include_router(router)
