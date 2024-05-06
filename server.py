import asyncio
import random
import re
from datetime import datetime

from custom_log import CustomLogger

class Server:
    """
    Асинхронный сервер для обработки сообщений от клиентов и отправки ответов.

    """
    def __init__(self, name='server', host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.clients = {}
        self.response_number = 0
        self.client_counts = 1
        self.log = CustomLogger(name)
        self.current_date = datetime.now().strftime('%Y-%m-%d')

    async def run(self):
        """
        Метод для запуска сервера и ожидания входящих подключений.
        """
        server = await asyncio.start_server(self._message_processing, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'Server {addr}')   

        async with server:
            asyncio.create_task(self._send_keepalive())
            await server.serve_forever()

    async def _message_processing(self, reader, writer):
        """
        Метод для обработки входящих сообщений от клиентов.

        """
        client_address = writer.get_extra_info('peername')
        if client_address not in self.clients:
            self.clients[client_address] = {'client_number': self.client_counts, 'writer': writer}
            self.client_counts += 1

        while True:
            data = await reader.read(100)
            if not data:
                break

            request_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            text_message = data.decode().strip()
            client_number = self.clients[client_address]['client_number']

            if random.randint(0, 99) > 10:
                await self._send_message(writer, client_number, text_message, request_time)
            else:
                log_info = f'{self.current_date}; {request_time}; {text_message}; (проигнорировано)'
                self.log.info(log_info)
                print(log_info)

    async def _send_message(self, writer, client_number, text_message, request_time):
        request_number = int(re.search(r'\[(\d+)\]', text_message).group(1))
        message = f'[{self.response_number}/{request_number}] PONG ({client_number})'
        self.response_number += 1
        delay = random.randint(100, 1000) / 1000
        await asyncio.sleep(delay)
        writer.write(message.encode())
        await writer.drain()

        response_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        log_info = (f'{self.current_date}; {request_time}; {text_message}; '
                    f'{response_time}; {message}')
        self.log.info(log_info)
        print(log_info)
 
    async def _send_keepalive(self):
        while True:
            for client in self.clients:
                writer = self.clients[client]['writer']
                message = f'[{self.response_number}] keepalive'
                writer.write(message.encode())
                self.response_number += 1

                send_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                log_info = f'{self.current_date}; {send_time}; {message}'
                # self.log.info(log_info)
                # В т.з. не гворилось о логировании keepalive
                print(log_info)
            await asyncio.sleep(5)
