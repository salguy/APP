from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from database import get_db
from domain.test.crud import *
from domain.test.schema import *
import os

router = APIRouter()


@router.post("/api/test", summary="1차 통합 테스트")
async def testapi( request: Request, audio: UploadFile = File(...), record: ScheduleID = Depends(), db: Session = Depends(get_db)):
    # 업로드된 파일의 데이터 읽기
    try:
        return await first_test(request, db, record, audio)
    except ValueError as e:
        error_message = str(e)
        if "존재하지 않는 scheduleId" in error_message:
            raise HTTPException(status_code=404, detail=error_message)
        elif "AI 서버 응답 형식 오류" in error_message or "TTS 파일 생성 실패" in error_message:
            raise HTTPException(status_code=500, detail=error_message)
        else:
            raise HTTPException(status_code=400, detail=error_message)
    


@router.post("/api/test2", summary="2차 통합 테스트")
async def testapi( request: Request, audio: UploadFile = File(...), record: TestSchema = Depends(), db: Session = Depends(get_db)):
    """
    2차 통합 테스트 API
    
    Parameters:
        - audio: 음성 파일 (UploadFile)
        - record: TestSchema 객체
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
        return await second_test(request, db, record, audio)
    except ValueError as e:
        error_message = str(e)
        if "존재하지 않는 scheduleId" in error_message:
            raise HTTPException(status_code=404, detail=error_message)
        elif "AI 서버 응답 형식 오류" in error_message or "TTS 파일 생성 실패" in error_message:
            raise HTTPException(status_code=500, detail=error_message)
        else:
            raise HTTPException(status_code=400, detail=error_message)