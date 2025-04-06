from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from database import get_db
from domain.test.crud import *
from domain.test.schema import *
from fastapi.responses import FileResponse
import requests
from domain.tts.tts import text_to_voice
import os
from dotenv import load_dotenv
import json

router = APIRouter()
load_dotenv()  # .env 파일 로드

AI_URL = os.getenv("AI_SERVER_URL")

@router.post("/api/test", summary="1차 통합 테스트")
async def testapi( request: Request, audio: UploadFile = File(...), record: ScheduleID = Depends(), db: Session = Depends(get_db)):
    # 업로드된 파일의 데이터 읽기
    try:
        schedule = db.query(MedicationSchedule).filter(MedicationSchedule.id == record.scheduleId).first()
        if not schedule:
            raise HTTPException(status_code=404, detail=f"존재하지 않는 scheduleId: {record.scheduleId}")
        contents = await audio.read()
        text = speech_to_text(contents)
        print("📦 보내는 텍스트:", text)
        print("📦 보내는 스케줄 ID:", record.scheduleId)


        url = AI_URL+"/api/inferences"
        # data = {"input_text": text}
        data = {"input_text": text, "scheduleId": record.scheduleId}
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        print("📦 전송 전 payload:", payload)

        res = requests.post(
            url,
            data=payload,  # ← json=대신 data=에 직접 직렬화된 JSON
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        print("data: ", data)
        print("🔁 AI서버 응답 상태코드:", res.status_code)
        print("📦 AI서버 응답 내용:", res.text)

        print("response: ", res.json())
        if "json" not in res.json()["model_output"] or "response" not in res.json()["model_output"]:
            raise HTTPException(status_code=500, detail="AI 서버 응답 형식 오류")
        # 텍스트를 음성으로 변환하여 파일 생성
        filename = text_to_voice(res.json()["model_output"]["response"])
        
        # 파일이 정상적으로 생성되었는지 확인
        if not os.path.exists(filename):
            raise HTTPException(status_code=500, detail="TTS 파일 생성 실패")
        # 생성된 파일을 클라이언트에 반환 (MIME 타입: audio/mpeg)
        
        file_url = f"{request.base_url}{filename}"
        return {
                "message": res.json()["model_output"]["response"],
                "file_url": file_url
                }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    