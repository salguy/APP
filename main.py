from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from database import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Hello World!")
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# CORS 설정 (필요한 경우)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(test_router.router, prefix="/api/test")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)