import os


class Config:
    DB_CONN_STR = os.getenv("DB_CONN_STR", "mongodb://localhost:27017/")
    SCHEDUALER_INTERVAL_SEC = int(os.getenv("SCHEDUALER_INTERVAL_SEC", "120"))
    PARSING_URLS = os.getenv("PARSING_URLS", "https://pastebin.com/archive").split(",")
    NUM_OF_PROCESSES = int(os.getenv("NUM_OF_PROCESSES", "1"))
    UNDEFINED_VALUES = set(["guest", "unknown", "anonymous", "untitled"])
