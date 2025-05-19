import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware
from domain.user import router as userRouter
from domain.medications import router as medicationRouter
from domain.stt import router as sttrouter
from domain.tts import router as ttsrouter
from domain.test import router as testrouter


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

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
app.mount("/test/assets", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static/assets")), name="assets")

@app.get("/test")
@app.get("/test/{full_path:path}")
async def serve_react_app(request: Request, full_path: str =""):
    return FileResponse(os.path.join("static", "index.html"))

origins = [
    "http://localhost:5173",
    "http://3.34.179.85:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(userRouter.router, tags=["users"])
app.include_router(medicationRouter.router, tags=["medications"])
app.include_router(sttrouter.router, tags=["stt"])
app.include_router(ttsrouter.router, tags=["tts"])
app.include_router(testrouter.router, tags=["test"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=1,           # 워커를 1개로 고정 (SSE 필수!)
        loop="uvloop",       # 고성능 이벤트 루프
        http="httptools"     # 빠른 HTTP 처리
    )