import asyncio
from client import Client

client = Client('client_red')
asyncio.run(client.run())