from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session
from database import get_db
from domain.test.crud import *
from domain.test.schema import *
import asyncio


router = APIRouter()
# queues = {}
from domain.state import queues


async def send_message(user_id: str, message: str):
    if user_id not in queues:
        raise HTTPException(status_code=404, detail="User not found")
    await queues[user_id].put(message)
    
@router.post("/api/wake")
async def wake(user_id: str):
    await send_message(user_id, "살가이가 듣는 중이에요...")
    return {"message": "Wake 메시지 전송 완료"}

@router.get("/api/events/{user_id}")
async def events(request: Request, user_id: str):
    if user_id not in queues:
        queues[user_id] = asyncio.Queue()

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    print(f"User {user_id} disconnected")
                    break
                message = await queues[user_id].get()
                yield f"data: {message}\n\n"
        finally:
            print(f"Cleaning up for user {user_id}")
            queues.pop(user_id, None)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/api/test", summary="1차 통합 테스트", response_model=TestResponse)
async def testapi(
    request: Request,
    audio: UploadFile = File(...),
    record: ScheduleID = Depends(),
    db: Session = Depends(get_db)
) -> TestResponse:
    """
    1차 통합 테스트 API
    
    Parameters:
        - audio: 음성 파일 (UploadFile)
        - record: ScheduleID 객체
            - scheduleId: int : 복약 스케줄 ID (-1인 경우 스케줄 검증 생략)
    
    Returns:
        - message: AI 서버의 응답 메시지
        - file_url: 생성된 음성 파일의 URL
    
    Raises:
        - HTTPException(400): 잘못된 입력값
        - HTTPException(404): 존재하지 않는 스케줄 ID
        - HTTPException(500): 서버 내부 오류
    """
    try:
        return await first_test(request, db, record, audio)
    except TestInputError as e:
        if "존재하지 않는 scheduleId" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except TestProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TestResponseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/test2", summary="2차 통합 테스트", response_model=TestResponse)
async def testapi2(
    request: Request,
    audio: UploadFile = File(...),
    record: TestSchema = Depends(),
    db: Session = Depends(get_db)
) -> TestResponse:
    """
    2차 통합 테스트 API
    
    Parameters:
        - audio: 음성 파일 (UploadFile)
        - record: TestSchema 객체
            - userId: int : 유저 ID
            - scheduleId: int : 복약 스케줄 ID (-1인 경우 스케줄 검증 생략)
            - responsetype: str : 응답 타입
                - check_meal: 복약 전 식사여부 체크
                - induce_medicine: 복약 유도
                - taking_medicine_time: 복약 시점 도달
                - check_medicine: 복용 완료 확인
    
    Returns:
        - message: AI 서버의 응답 메시지
        - file_url: 생성된 음성 파일의 URL
    
    Raises:
        - HTTPException(400): 잘못된 입력값
        - HTTPException(404): 존재하지 않는 스케줄 ID
        - HTTPException(500): 서버 내부 오류
    """
    try:
        # 여기서 먼저 "살가이가 생각하는 중이에요..." 문구 보내기
        user_id = record.userId  # <- record 안에 user_id가 있어야 해 (없으면 수정 필요)
        await send_message(user_id, "살가이가 생각하는 중이에요...")
        
        result = await second_test(request, db, record, audio)
    
         # ✅ 그 결과 중 message를 프론트에도 보내기
        await send_message(user_id, result.message)

        # ✅ 마지막으로 클라이언트에 반환
        return result
    
    except TestInputError as e:
        if "존재하지 않는" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except TestProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TestResponseError as e:
        raise HTTPException(status_code=500, detail=str(e))