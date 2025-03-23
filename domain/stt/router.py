from fastapi import APIRouter, Depends, HTTPException, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from domain.stt.crud import *
from domain.stt.schema import *
from fastapi.responses import JSONResponse
router = APIRouter()

@router.post("/api/stt", summary="음성 데이터 STT 처리")
async def process_stt(audio: UploadFile = File(...)):
    # 업로드된 파일의 데이터 읽기
    try:
        contents = await audio.read()
        return speech_to_text(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    