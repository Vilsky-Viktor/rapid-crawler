import asyncio
import atexit
from logging import Logger
from multiprocessing import Queue, Process
from rapid_scrawler.config import Config
from rapid_scrawler.db.posts import PostsTable
from rapid_scrawler.log import create_logger

queue = Queue()


def parser_worker(queue: Queue) -> None:
    db_manager = PostsTable()
    db_manager.set_client()
    logger = create_logger()
    while True:
        parser = queue.get()
        parser.set_db(db_manager)
        parser.set_logger(logger)
        asyncio.run(parser.run())


def create_workers(logger: Logger) -> None:
    processes = []
    for _ in range(Config.NUM_OF_PROCESSES):
        process = Process(target=parser_worker, args=(queue,))
        process.daemon = True
        process.start()
        processes.append(process)
    logger.info(f"parser workers ({Config.NUM_OF_PROCESSES}) have been created")

    def kill_processes():
        for process in processes:
            process.terminate()
            logger.info(f"{process} has been killed")

    atexit.register(kill_processes)
