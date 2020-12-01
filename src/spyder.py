from typing import Set, Coroutine, Union
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import logging
from datetime import datetime
import time

import aiohttp

from parser.Parser import Parser
from parser.data.Data import Data
from dao.base import DB
from dao.DataDAO import DataDAO
from dao.TaskDAO import TaskDAO
from dao.TaskModel import Task
from dao.DataModel import ParseData


class Spyder:
    logger = logging.getLogger(__name__)
    MAX_DEPTH = 2  # parse depth

    def __init__(self):
        self.__db = DB()
        self.__task_dao = TaskDAO(self.__db)
        self.__data_dao = DataDAO(self.__db)
        self.parsed_urls: Set[str] = set()
        self.__loop = asyncio.get_event_loop()
        self.__pool: ThreadPoolExecutor = None
        self.__client: aiohttp.ClientSession = None
        self._depth: int = 0
        self.__task_id: int = None

    def parse(self, result: str, url: str) -> Data:
        data: Data = None
        if result:
            data = Parser.parse(result, url)
            if data:
                self.__data_dao.save_data(
                    ParseData(url=data.uri,
                              title=data.title,
                              html=data.html,
                              created=datetime.now(),
                              task_id=self.__task_id))
        return data

    async def request(self, url: str) -> (str, str):
        html: str = None
        try:
            result = await self.__client.get(url)
            if result.status == 200:
                html = await result.text()
        except Exception:
            Spyder.logger.error(f"Request error url: {url}", exc_info=True)
        return html, url

    async def worker(self,
                     future: Union[Coroutine, asyncio.Future],
                     depth: int) -> None:
        futures = []
        if depth < self._depth:
            data = await future
            if data:
                urls_to_parse = data.urls - self.parsed_urls
                self.parsed_urls |= data.urls
                for request_future in asyncio.as_completed(
                    [self.request(url) for url in urls_to_parse]):
                    parse_future = \
                        self.__loop.run_in_executor(self.__pool,
                                                    self.parse,
                                                    *(await request_future))

                    futures.append(
                        asyncio.ensure_future(
                            self.worker(parse_future, depth + 1)))

        if futures:
            await asyncio.wait(futures)

    async def start_worker(self, url: str) -> None:
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
            self.__pool = pool
            async with aiohttp.ClientSession() as client:
                self.__client = client
                initial_future = self.__loop.create_future()
                initial_future.set_result(Data(None, None, None, {url}))
                await self.worker(initial_future, -1)

    def set_depth(self, depth: int):
        if depth > Spyder.MAX_DEPTH:
            raise ValueError(f"Depth should be less then {Spyder.MAX_DEPTH}")
        self._depth = depth

    def start(self, url: str, depth: int):
        self.set_depth(depth)
        self.__task_id = self.__task_dao.save_data(Task(url=url,
                                                        created=datetime.now()))
        try:
            self.__loop.run_until_complete(
                self.start_worker(url))
        except Exception as e:
            Spyder.logger.error("Spyder error", exc_info=True)
        finally:
            self.__loop.close()
            Spyder.logger.info(f"Parse complete, parsed urls count: "
                               f"{len(self.parsed_urls)}")

    def get_parsed_data(self, url: str, limit: int) -> str:
        tasks = self.__task_dao.get_by_url(url)
        if tasks:
            id = tasks[0].id
            result = self.__data_dao.get_data_by_task_id(id, limit)
            return "\n".join([r.url + " " + r.title for r in result])
        else:
            return "Empty result"
