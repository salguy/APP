from models import *
from domain.stt.stt import voice_to_text
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, UploadFile
from domain.stt.schema import *
from sqlalchemy.orm import Session
from domain.test.schema import *
from dotenv import load_dotenv
import os
import json
import requests
from domain.tts.tts import text_to_voice
from datetime import datetime



load_dotenv()  # .env 파일 로드

AI_URL = os.getenv("AI_SERVER_URL")

def speech_to_text(content):
    transcript = voice_to_text(content)
    #return JSONResponse(content={"transcript": transcript})
    return transcript


async def testapi_logic( request: Request, db: Session, record: ScheduleID, audio: UploadFile):
    schedule = db.query(MedicationSchedule).filter(MedicationSchedule.id == record.scheduleId).first()
    if not schedule:
        if record.scheduleId != -1:
            raise HTTPException(status_code=404, detail=f"존재하지 않는 scheduleId: {record.scheduleId}")

    contents = await audio.read()
    text = speech_to_text(contents)
    # print("📦 보내는 텍스트:", text)
    # print("📦 보내는 스케줄 ID:", record.scheduleId)
    url = AI_URL+"/api/inferences"
    data = {"input_text": text, "scheduleId": record.scheduleId}
    payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    # print("📦 전송 전 payload:", payload)

    res = requests.post(
        url,
        data=payload,  # ← json=대신 data=에 직접 직렬화된 JSON
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    print("data: ", data)
    print("🔁 AI서버 응답 상태코드:", res.status_code)
    print("📦 AI서버 응답 내용:", res.text)
    if "json" not in res.json()["model_output"] or "response" not in res.json()["model_output"]:
            raise HTTPException(status_code=500, detail="AI 서버 응답 형식 오류")
    # 텍스트를 음성으로 변환하여 파일 생성
    res_data = res.json()
    model_output = res_data["model_output"]
    response_text = model_output["response"]
    med_time = res_data.get("med_time")
    
    if record.scheduleId != -1:
        if med_time:
            try:
                updated = update_taken_at_if_empty(db, schedule.id, med_time)
                if updated:
                    print(f"✅ 복약 스케줄(id: {schedule.id}의 taken_at을 업데이트했습니다: {med_time}")
                else:
                    print("⏩ 이미 taken_at이 존재합니다. 업데이트 생략")
            except ValueError as e:
                print(f"❌ 복약 시각 저장 실패: {str(e)}", "error")
        
    filename = text_to_voice(response_text)
    
    # 파일이 정상적으로 생성되었는지 확인
    if not os.path.exists(filename):
        raise HTTPException(status_code=500, detail="TTS 파일 생성 실패")
    # 생성된 파일을 클라이언트에 반환 (MIME 타입: audio/mpeg)
    
    file_url = f"{request.base_url}{filename}"
    
    return {
            "message": res.json()["model_output"]["response"],
            "file_url": file_url
            }
    
    
def update_taken_at_if_empty(db: Session, schedule_id: int, taken_at_str: str) -> bool:
    """
    복약 스케줄 ID에 해당하는 레코드의 taken_at이 비어 있을 경우에만 채워넣는다.
    
    Returns:
        bool: 실제로 업데이트되었으면 True, 아니면 False
    """
    # 1. 스케줄 조회
    schedule = db.query(MedicationSchedule).filter(MedicationSchedule.id == schedule_id).first()
    if not schedule:
        raise ValueError(f"존재하지 않는 scheduleId: {schedule_id}")
    
    # 2. taken_at이 이미 있으면 업데이트 생략
    if schedule.taken_at is not None:
        return False

    # 3. 문자열을 datetime으로 변환
    try:
        taken_at_dt = datetime.strptime(taken_at_str, "%y.%m.%d.%H.%M")
    except ValueError:
        raise ValueError(f"날짜 형식 오류: {taken_at_str} (YY.MM.DD.HH.MM 이어야 함)")

    # 4. 업데이트 수행
    schedule.taken_at = taken_at_dt
    db.commit()
    db.refresh(schedule)
    return True