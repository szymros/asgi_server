import asyncio
from asgi_server.parser import HttpParser
from asgi_server.asgi_interface import AsgiInterface
import logging


class AsgiProtocol(asyncio.Protocol):
    def __init__(self, loop: asyncio.AbstractEventLoop, app):
        self.loop = loop
        self.app = app

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        logging.info(f"Connected to peer {self.peername}")

    def data_received(self, data: bytes) -> None:
        logging.info(f"Received data from peer {self.peername}")
        request = data.decode()
        parsed_request = HttpParser.parse(request)
        self.loop.create_task(self.handle_asgi(parsed_request))

    async def handle_asgi(self, request: dict):
        logging.info(f"Dispatched request to app for peer {self.peername}")
        asgi_handler = AsgiInterface(request)
        await asgi_handler.run(self.app)
        logging.info(f"App processed request for peer {self.peername}")
        response = HttpParser.parse_response(asgi_handler.response)
        logging.info(f"Sending response to peer {self.peername}")
        self.transport.write(response.encode())
        self.transport.close()
        logging.info(f"Response sent to peer {self.peername} connection closed")


class Server:
    def __init__(self, host: str, port: int, app) -> None:
        self.host = host
        self.port = port
        self.app = app

    async def listen(self):
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            lambda: AsgiProtocol(loop, self.app), self.host, self.port
        )
        await server.serve_forever()
