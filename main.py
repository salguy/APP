from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from domain.user import router as userRouter
from domain.medications import router as medicationRouter

tags_metadata = [
    {
        "name": "users",
        "description": "회원 기능",
    },
    {
        "name": "medications",
        "description": "약 정보",
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


<<<<<<< HEAD
app.include_router(medicineInfoRouter.router, tags=["medicineInfo"])


if __name__ == '__main__':
=======
app.include_router(userRouter.router, tags=["users"])
app.include_router(medicationRouter.router, tags=["medications"])

if __name__ == "__main__":
>>>>>>> develop
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)