from typing import Set, Coroutine, Union
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import logging
from datetime import datetime

import aiohttp

from spyder.parser.Parser import Parser
from spyder.parser.data.Data import Data
from spyder.dao.Base import DB
from spyder.dao.DataDAO import DataDAO
from spyder.dao.TaskDAO import TaskDAO
from spyder.dao.model.TaskModel import Task
from spyder.dao.model.DataModel import ParseData


class Spyder:
    """
    Spyder application
    Parse links and save result to postgres
    """
    logger = logging.getLogger(__name__)
    MAX_DEPTH = 2  # max parse depth, throw exception

    def __init__(self):
        self._db = DB()
        self._task_dao = TaskDAO(self._db)
        self._data_dao = DataDAO(self._db)
        self.parsed_urls: Set[str] = set()
        self._loop = asyncio.get_event_loop()
        self._pool: ThreadPoolExecutor = None
        self._client: aiohttp.ClientSession = None
        self._depth: int = 0
        self._task_id: int = None

    def parse(self, result: str, url: str) -> Data:
        """
        Get title and links from html
        Save parsed data to DB
        :param result: html
        :param url: source url
        :return: parsed data
        """
        data: Data = None
        if result:
            data = Parser.parse(result, url)
            if data:
                self._data_dao.save_data(
                    ParseData(url=data.uri,
                              title=data.title,
                              html=data.html,
                              created=datetime.now(),
                              task_id=self._task_id))
        return data

    async def request(self, url: str) -> (str, str):
        html: str = None
        try:
            result = await self._client.get(url)
            if result.status == 200:
                html = await result.text()
        except Exception:
            Spyder.logger.error(f"Request error url: {url}", exc_info=True)
        return html, url

    async def worker(self,
                     future: Union[Coroutine, asyncio.Future],
                     depth: int) -> None:
        """
        Make request to url async and parse data in thread
        Start new workers for parsed urls
        :param future: result of self.parse function
        :param depth: current depth
        """
        futures = []
        if depth < self._depth:
            data: Data = await future
            if data:
                urls_to_parse = data.urls - self.parsed_urls
                self.parsed_urls |= data.urls
                for request_future in asyncio.as_completed(
                        [self.request(url) for url in urls_to_parse]):
                    parse_future = \
                        self._loop.run_in_executor(self._pool,
                                                   self.parse,
                                                   *(await request_future))

                    futures.append(
                        asyncio.ensure_future(
                            self.worker(parse_future, depth + 1)))

        if futures:
            await asyncio.wait(futures)

    async def start_worker(self, url: str) -> None:
        """
        Entry worker
        Create mock future, initialize aiohttp pool and thread pool
        :param url: start url
        """
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
            self._pool = pool
            async with aiohttp.ClientSession() as client:
                self._client = client
                initial_future = self._loop.create_future()
                initial_future.set_result(Data(None, None, None, {url}))
                await self.worker(future=initial_future, depth=-1)
                # start depth -1 for process mock future

    def set_depth(self, depth: int):
        """
        Set parse depth
        :raises ValueError: if depth > MAX_DEPTH
        :param depth
        :return:
        """
        if depth > Spyder.MAX_DEPTH:
            raise ValueError(f"Depth should be less then {Spyder.MAX_DEPTH}")
        self._depth = depth

    def start(self, url: str, depth: int):
        """
        Entry point
        :param url: start url
        :param depth:
        """
        self.set_depth(depth)
        self._task_id = self._task_dao.save_data(
                                        Task(url=url, created=datetime.now()))
        try:
            self._loop.run_until_complete(
                self.start_worker(url))
        except Exception:
            Spyder.logger.error("Spyder error", exc_info=True)
        finally:
            self._loop.close()
            Spyder.logger.info(f"Parse complete, parsed urls count: "
                               f"{len(self.parsed_urls)}")

    def get_parsed_data(self, url: str, limit: int) -> str:
        tasks = self._task_dao.get_by_url(url)
        # TODO: Can be more than one result
        if tasks:
            id = tasks[0].id
            result = self._data_dao.get_data_by_task_id(id, limit)
            return "\n".join([r.url + " " + r.title for r in result])
        else:
            return "Empty result"
