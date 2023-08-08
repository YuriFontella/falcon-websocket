import falcon.asgi

from falcon.asgi import WebSocket
from falcon import WebSocketDisconnected

class WebsocketMiddleware:
    async def process_request_ws(self, req, ws: WebSocket):
        print(ws)
        print('middleware request ws')

    async def process_resource_ws(self, req, ws: WebSocket, resource, params):
        print(ws)
        print('middleware resource ws')

class WebsocketResource:
    connections = list()

    async def on_get(self, req, resp):
        print('on_get')
        print(self.connections)

        if self.connections:
            for ws in self.connections:
                await ws.send_text('hello')

        resp.media = True

    async def on_websocket(self, req, ws: WebSocket):
        print('on_websocket')

        try:
            await ws.accept()
        except WebSocketDisconnected:
            return

        print(ws)
        
        self.connections.append(ws)
        print(self.connections)

        while True:
            try:
                media = await ws.receive_media()
                
                media = media.get('status')

                print(media)
                await ws.send_media(media)

                if media == 'close':
                    await ws.close()

            except WebSocketDisconnected:
                print('disconnected')
                
                self.connections.remove(ws)
                break
                
app = falcon.asgi.App(middleware=[WebsocketMiddleware()])

app.add_route('/', WebsocketResource())
