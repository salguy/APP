# state.py
import asyncio

queues: dict[str, asyncio.Queue] = {}
clients: dict[str, asyncio.Queue] = {}