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
        return await testapi_logic(request, db, record, audio)

        
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    