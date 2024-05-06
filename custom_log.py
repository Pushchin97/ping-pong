from datetime import datetime
import logging
import os

class CustomLogger:
    """
    Класс CustomLogger предоставляет возможность логирования сообщений в файлы.

    """
    def __init__(self, name):
        self.name = name
        self.current_time = datetime.now().strftime('%H-%M-%S')
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.log_folder = self._create_log_folder()
        self.loger = self._setup_logger()
  
    def _create_log_folder(self):
        log_folder_path = os.path.join(os.getcwd(), f'logs/logs_{self.current_date}')
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        name_folder_path = os.path.join(log_folder_path, self.name)
        if not os.path.exists(name_folder_path):
            os.makedirs(name_folder_path)
        return name_folder_path

    def _setup_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        log_file_path = os.path.join(self._create_log_folder(), f'{self.name}_{self.current_time}.log')
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def info(self, message):
        self.loger.info(message)
