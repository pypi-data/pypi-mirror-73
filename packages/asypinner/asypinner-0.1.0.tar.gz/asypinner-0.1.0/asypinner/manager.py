#!/usr/bin/env python3
import sys
import asyncio
from typing import List, Awaitable
from dataclasses import dataclass

from .misc import CursorMove
from .store import TaskInfoStore


@dataclass(init=False)
class TaskManager:

    task_info_stores: List[TaskInfoStore]
    watch_interval_ms: int

    def __init__(
        self,
        task_info_stores: List[TaskInfoStore],
        watch_interval_ms: int = 200,
    ) -> None:
        self.task_info_stores = task_info_stores
        self.watch_interval_ms = watch_interval_ms
        return

    def all_finishied(self) -> bool:
        return all([store.is_finished for store in self.task_info_stores])

    def print_task_info(self) -> None:
        for store in self.task_info_stores:
            print(store.get_line())
        print(CursorMove.up(len(self.task_info_stores)), end='')
        return

    def print_task_summary(self) -> None:
        for store in self.task_info_stores:
            store.print_summary()
        return

    def flush(self) -> None:
        print(CursorMove.down(len(self.task_info_stores)), end='')
        sys.stdout.flush()
        return

    async def watch(self) -> None:
        while (not self.all_finishied()):
            await asyncio.sleep(self.watch_interval_ms / 1000)
            self.print_task_info()

    async def run(self, async_tasks: List[Awaitable[None]]) -> bool:
        """
        Run all async job given.
        It returens whether all tasks finished successfully.
        """
        await asyncio.gather(*async_tasks, self.watch())
        self.flush()
        self.print_task_summary()
        return all([store.is_success for store in self.task_info_stores])
