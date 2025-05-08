from domain.state import queues
import asyncio
from fastapi import HTTPException

async def send_message(user_id: str, message: str):
    if user_id not in queues:
        print(f"[SSE] {user_id} not connected")
        raise HTTPException(status_code=404, detail="User not found in queues")
    await queues[user_id].put(message)
    print(queues)
    await asyncio.sleep(0)  # 컨텍스트 스위칭 강제

    