# state.py
import asyncio

queues: dict[str, asyncio.Queue] = {}