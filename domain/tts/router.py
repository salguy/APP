from fastapi import APIRouter, HTTPException, APIRouter
from domain.tts.crud import *
from domain.tts.schema import *
from fastapi.responses import FileResponse
from domain.tts.tts import text_to_voice
import os

router = APIRouter()

@app.post("/api/tts", summary="텍스트를 음성으로 변환하여 파일 반환")
async def process_tts(input_data: TextInput):
    """
    입력받은 텍스트를 음성파일로 반환하는 엔드포인트입니다.
    
    - **text**: 음성파일로 변환할 텍스트
    """
    try:
        # 텍스트를 음성으로 변환하여 파일 생성
        filename = text_to_voice(input_data.text)
        # 파일이 정상적으로 생성되었는지 확인
        if not os.path.exists(filename):
            raise HTTPException(status_code=500, detail="TTS 파일 생성 실패")
        # 생성된 파일을 클라이언트에 반환 (MIME 타입: audio/mpeg)
        return FileResponse(path=filename, media_type="audio/mpeg", filename="output.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    