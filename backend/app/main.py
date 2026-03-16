from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import interview_session, upload_interview, create_user
from contextlib import asynccontextmanager


async def create_table_if_not_exists():
    async with engine.begin() as conn:
        print("connected to the user database")
        await conn.run_sync(models.Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table_if_not_exists()
    yield

app=FastAPI(lifespan=lifespan)


app.include_router(interview_session.router)
app.include_router(upload_interview.router)
app.include_router(create_user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], #allowed for all so as to test all apis  
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)