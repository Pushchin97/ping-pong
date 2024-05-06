import asyncio
from client import Client

client = Client('client_blue')
asyncio.run(client.run())