import asyncio
from domain.state import queues, clients

async def broadcast_loop():
    while True:
        for user_id, queue in list(queues.items()):
            if not queue.empty():
                message = await queue.get()
                if user_id in clients:
                    await clients[user_id].put(message)
        await asyncio.sleep(0.01)
