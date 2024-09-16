from os import environ
from dotenv import load_dotenv, dotenv_values, set_key

FILE_PATH = 'settings.env'

class Config:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_settings()
        return cls._instance

    def load_settings(self):
        load_dotenv()
        [setattr(self, key, value) for key, value in dotenv_values(FILE_PATH).items()]

    def update_value(self, key, value):
        setattr(self, key, value)
        set_key(FILE_PATH, key, value)

    def get_value(self, key):
        return getattr(self, key, None)

