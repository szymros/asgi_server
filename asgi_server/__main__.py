import asyncio
import sys
import importlib
from asgi_server.server import Server


if __name__ == "__main__":
    app_path = sys.argv[1].split(":")
    port = int(sys.argv[2])
    module = importlib.import_module(app_path[0])
    app = getattr(module, app_path[1])
    server = Server("", port, app)
    asyncio.run(server.listen())
