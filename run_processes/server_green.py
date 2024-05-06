import asyncio
from server import Server

server = Server('server_green')
asyncio.run(server.run())