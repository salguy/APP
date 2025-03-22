from database import Base, engine
from models import *  # ORM 모델 로드


print("테이블 생성 중...")
Base.metadata.drop_all(bind=engine)  # 기존 테이블 삭제
Base.metadata.create_all(bind=engine)  # 새 테이블 생성
print("테이블 생성 완료!")
from sqlalchemy import inspect

inspector = inspect(engine)
print(inspector.get_table_names())  