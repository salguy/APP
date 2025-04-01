from fastapi import APIRouter, Depends, HTTPException, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from domain.stt.crud import *
from domain.stt.schema import *
from fastapi.responses import FileResponse
import requests
from domain.tts.tts import text_to_voice
import os

router = APIRouter()

@router.post("/api/stt", summary="음성 데이터 STT 처리 후 반환")
async def process_stt(audio: UploadFile = File(...)):
    # 업로드된 파일의 데이터 읽기
    try:
        contents = await audio.read()
        return speech_to_text(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/api/test", summary="1차 통합 테스트")
async def process_stt(audio: UploadFile = File(...)):
    # 업로드된 파일의 데이터 읽기
    try:
        contents = await audio.read()
        text = speech_to_text(contents)
        url = "https://044e-34-87-67-32.ngrok-free.app/api/inference"
        data = {"message": text}

        res = requests.get(url, json=data)
        print("response: ", res.json())
        # 텍스트를 음성으로 변환하여 파일 생성
        filename = text_to_voice(res.json()["parsed"]["response"])
        # 파일이 정상적으로 생성되었는지 확인
        if not os.path.exists(filename):
            raise HTTPException(status_code=500, detail="TTS 파일 생성 실패")
        # 생성된 파일을 클라이언트에 반환 (MIME 타입: audio/mpeg)
        return FileResponse(path=filename, media_type="audio/mpeg", filename="output.mp3")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    