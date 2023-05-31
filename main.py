import time
from rapid_crawler.workers.parser_worker import create_workers, queue
from rapid_crawler.config import Config
from rapid_crawler.parsers.parser_factory import ParserFactory
from rapid_crawler.log import create_logger
from rapid_crawler.validators.url import is_valid_url

if __name__ == "__main__":
    logger = create_logger()
    create_workers(logger)
    while True:
        unique_urls = list(set(Config.PARSING_URLS))
        for url in unique_urls:
            if not is_valid_url(url):
                logger.info(f"skipping not valid url {url}")
                continue
            try:
                parser_factory = ParserFactory(url)
                parser = parser_factory.create_parser()
                queue.put(parser)
            except Exception as error:
                logger.error(error)

        time.sleep(Config.SCHEDUALER_INTERVAL_SEC)
