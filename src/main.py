from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from src.exceptions.handlers import app_exceptions_handler, app_http_exceptions_handler

from src.core.database import test_db_connection
from src.core.redis import redis_client

from src.permissions.router import router as permissions_router
from src.supplies.router import router as supplies_router
from src.products.router import router as products_router
from src.users.router import router as users_router
from src.auth.router import router as auth_router

app = FastAPI()


@asynccontextmanager
async def lifespan(application: FastAPI):
    print("API STARTED")
    await test_db_connection()
    yield
    await redis_client.close()
    print("API STOPPED")


app = FastAPI(title="API", lifespan=lifespan)

app.add_exception_handler(Exception, app_exceptions_handler)
app.add_exception_handler(HTTPException, app_http_exceptions_handler)

app.include_router(router=auth_router)
app.include_router(router=users_router)
app.include_router(router=permissions_router)
app.include_router(router=supplies_router)
app.include_router(router=products_router)
