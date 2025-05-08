from models import *
from domain.stt.stt import voice_to_text
from fastapi import Request, UploadFile
from domain.stt.schema import *
from sqlalchemy.orm import Session
from domain.test.schema import *
from dotenv import load_dotenv
import os
import json
import requests
from domain.tts.tts import text_to_voice
from datetime import datetime
from domain.test.sse import send_message
import asyncio



load_dotenv()  # .env 파일 로드

AI_URL = os.getenv("AI_SERVER_URL")

def speech_to_text(content: bytes) -> str:
    """음성을 텍스트로 변환합니다."""
    return voice_to_text(content)

def update_taken_at_if_empty(db: Session, schedule_id: int, taken_at_str: str) -> bool:
    """
    복약 스케줄 ID에 해당하는 레코드의 taken_at이 비어 있을 경우에만 채워넣는다.
    현재 시각보다 이전이어야 함
    
    Args:
        db (Session): 데이터베이스 세션
        schedule_id (int): 복약 스케줄 ID
        taken_at_str (str): 복약 시각 문자열 (YY.MM.DD.HH.MM 형식)
    
    Returns:
        bool: 실제로 업데이트되었으면 True, 아니면 False
    
    Raises:
        TestInputError: 잘못된 입력값
    """
    # 1. 스케줄 조회
    schedule = db.query(MedicationSchedule).filter(MedicationSchedule.id == schedule_id).first()
    if not schedule:
        raise TestInputError(f"존재하지 않는 scheduleId: {schedule_id}")
    
    # 2. taken_at이 이미 있으면 업데이트 생략
    if schedule.taken_at is not None:
        return False
    
    # 3. 문자열을 datetime으로 변환
    try:
        taken_at_dt = datetime.strptime(taken_at_str, "%y.%m.%d.%H.%M")
        if taken_at_dt > datetime.now():
            raise TestInputError("taken_at은 현재 시각보다 과거여야 합니다.")
    except ValueError:
        raise TestInputError(f"날짜 형식 오류: {taken_at_str} (YY.MM.DD.HH.MM 이어야 함)")

    # 4. 업데이트 수행
    schedule.taken_at = taken_at_dt
    db.commit()
    db.refresh(schedule)
    return True

async def first_test(request: Request, db: Session, record: ScheduleID, audio: UploadFile) -> TestResponse:
    """
    1차 통합 테스트를 수행합니다.
    
    Args:
        request (Request): FastAPI 요청 객체
        db (Session): 데이터베이스 세션
        record (ScheduleID): 스케줄 ID 정보
        audio (UploadFile): 업로드된 음성 파일
    
    Returns:
        TestResponse: 테스트 결과
    
    Raises:
        TestInputError: 잘못된 입력값
        TestProcessingError: 처리 과정 중 오류
        TestResponseError: 응답 처리 중 오류
    """
    schedule = db.query(MedicationSchedule).filter(MedicationSchedule.id == record.scheduleId).first()
    if not schedule and record.scheduleId != -1:
        raise TestInputError(f"존재하지 않는 scheduleId: {record.scheduleId}")

    try:
        contents = await audio.read()
        text = speech_to_text(contents)
        
        url = AI_URL + "/api/inferences"
        data = {"input_text": text}
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")

        res = requests.post(
            url,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
        if res.status_code != 200:
            raise TestResponseError(f"AI 서버 응답 오류: {res.status_code}")
            
        res_data = res.json()
        if "json" not in res_data["model_output"] or "response" not in res_data["model_output"]:
            raise TestResponseError("AI 서버 응답 형식 오류")
            
        model_output = res_data["model_output"]
        response_text = model_output["response"]
        med_time = res_data.get("med_time")
        
        if record.scheduleId != -1 and med_time:
            try:
                updated = update_taken_at_if_empty(db, schedule.id, med_time)
                if updated:
                    print(f"✅ 복약 스케줄(id: {schedule.id}의 taken_at을 업데이트했습니다: {med_time}")
                else:
                    print("⏩ 이미 taken_at이 존재합니다. 업데이트 생략")
            except TestInputError as e:
                print(f"❌ 복약 시각 저장 실패: {str(e)}", "error")
        
        filename = text_to_voice(response_text)
        if not os.path.exists(filename):
            raise TestProcessingError("TTS 파일 생성 실패")
            
        file_url = f"{request.base_url}{filename}"
        
        return TestResponse(
            message=response_text,
            file_url=file_url
        )
        
    except requests.RequestException as e:
        raise TestProcessingError(f"AI 서버 통신 오류: {str(e)}")
    except Exception as e:
        raise TestProcessingError(f"처리 중 오류 발생: {str(e)}")

async def second_test(request: Request, db: Session, record: TestSchema, audio: UploadFile) -> TestResponse:
    """
    2차 통합 테스트를 수행합니다.
    
    Args:
        request (Request): FastAPI 요청 객체
        db (Session): 데이터베이스 세션
        record (TestSchema): 테스트 스키마
        audio (UploadFile): 업로드된 음성 파일
    
    Returns:
        TestResponse: 테스트 결과
    
    Raises:
        TestInputError: 잘못된 입력값
        TestProcessingError: 처리 과정 중 오류
        TestResponseError: 응답 처리 중 오류
    """
    await send_message(record.userId, "살가이가 생각하는 중이에요...") 
    asyncio.sleep(0)  # 컨텍스트 스위칭 강제
    
    schedule = db.query(MedicationSchedule).filter(MedicationSchedule.id == record.scheduleId).first()
    if not schedule and record.scheduleId != -1:
        raise TestInputError(f"존재하지 않는 scheduleId: {record.scheduleId}")
    user = db.query(User).filter(User.id == record.userId).first()

    if not user:
        raise TestInputError(f"존재하지 않는 userId: {record.userId}")

    try:
        contents = await audio.read()
        text = speech_to_text(contents)
        
        url = f"{AI_URL}/api/inference/{record.responsetype}"
        data = {"input_text": text}
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")

        res = requests.post(
            url,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
        if res.status_code != 200:
            raise TestResponseError(f"AI 서버 응답 오류: {res.status_code}")
            
        res_data = res.json()
        if "model_output" not in res_data or "json" not in res_data["model_output"] or "response" not in res_data["model_output"]:
            raise TestResponseError("AI 서버 응답 형식 오류")
            
        model_output = res_data["model_output"]
        response_text = model_output["response"]
        med_time = res_data.get("med_time")
        
        await send_message(record.userId, response_text)
        
        
        if record.scheduleId != -1 and med_time:
            try:
                updated = update_taken_at_if_empty(db, schedule.id, med_time)
                if updated:
                    print(f"✅ 복약 스케줄(id: {schedule.id}의 taken_at을 업데이트했습니다: {med_time}")
                else:
                    print("⏩ 이미 taken_at이 존재합니다. 업데이트 생략")
            except TestInputError as e:
                print(f"❌ 복약 시각 저장 실패: {str(e)}", "error")
        
        filename = text_to_voice(response_text)
        if not os.path.exists(filename):
            raise TestProcessingError("TTS 파일 생성 실패")
            
        file_url = f"{request.base_url}{filename}"
        
        return TestResponse(
            message=response_text,
            file_url=file_url
        )
        
    except requests.RequestException as e:
        raise TestProcessingError(f"AI 서버 통신 오류: {str(e)}")
    except Exception as e:
        raise TestProcessingError(f"처리 중 오류 발생: {str(e)}")
