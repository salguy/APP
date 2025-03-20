from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from domain.medicineInfo import router as medicineInfoRouter

tags_metadata = [
    {
        "name": "users",
        "description": "회원 기능",
    },
    {
        "name": "medicineInfo",
        "description": "복약 정보",
    }
]

app = FastAPI(
    openapi_tags=tags_metadata
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(medicineInfoRouter.router, tags=["medicineInfo"])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)