import asyncio
import websockets

async def connect():
    uri = 'ws://localhost:8000'

    async with websockets.connect(uri) as websocket:
        await websocket.send('Hello, WebSocket Server!')
        response = await websocket.recv()
        print('Received:', response)

asyncio.run(connect())