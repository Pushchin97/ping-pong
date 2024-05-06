import asyncio
from datetime import datetime, timedelta
import random
import re

from custom_log import CustomLogger

class Client:
    """
    Асинхронный клиент для отправки запросов на сервер и чтения ответов.

    """
    def __init__(self, name='client', host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.request_number = 0
        self.log = CustomLogger(name)
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.sent_messages = {}

    def _check_ignored_messages(self):
        """
        Метод для проверки игнорируемых сообщений и записи информации о них в лог.

        Если сообщение не получено в течение 5 секунд, оно записывается в лог как проигнорированное.
        """
        for mess in list(self.sent_messages.keys()):
            time_now = datetime.now()
            time_send = self.sent_messages[mess]['time']
            text_message = self.sent_messages[mess]['text']
            timeout = time_now - time_send
            if timeout > timedelta(seconds=5):
                timeout = "{:02d}.{:03d}".format(timeout.seconds, timeout.microseconds // 1000)
                log_info = (
                    f'{self.current_date}; {time_send.strftime('%H:%M:%S.%f')[:-3]}; '
                    f'{text_message}; {timeout}; (таймаут)'
                )
                self.log.info(log_info)
                del self.sent_messages[mess]
                print(log_info)

    async def _send_message(self):
        while True:
            delay = random.randint(300, 3000) / 1000
            message = f'[{self.request_number}] PING'
            request_number = self.request_number
            self.request_number += 1
            await asyncio.sleep(delay)
            self.writer.write(message.encode())
            await self.writer.drain()
            request_time = datetime.now()
            self.sent_messages[request_number] = {'time':request_time, 'text': message}

    async def _read_responses(self):
        while True:
            data = await self.reader.read(100)
            response_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            if not data:
                break

            elif 'keepalive' in data.decode():
                log_info = f'{self.current_date}; {response_time}; {data.decode()}'
                self.log.info(log_info)
                print(log_info)
                continue

            number = int(re.search(r'\[\d+/(\d+)\]', data.decode()).group(1))
            request_time = self.sent_messages[number]['time'].strftime('%H:%M:%S.%f')[:-3]
            text_message = self.sent_messages[number]['text']
            log_info = (
                f'{self.current_date}; {request_time}; {text_message}; '
                f'{response_time}; {data.decode()}'
            )
            self.log.info(log_info)
            print(log_info)
            del self.sent_messages[number]

            self._check_ignored_messages()

    async def run(self):
        """
        Метод для запуска клиента и асинхронного выполнения отправки сообщений и чтения ответов.
        """
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        await asyncio.gather(self._send_message(), self._read_responses())
