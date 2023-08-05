#!/usr/bin/env python3
import re
import sys
import asyncio
import subprocess as sp
import unicodedata
from typing import List, Optional, Awaitable
from dataclasses import dataclass

from .misc import CursorMove
from .store import TaskInfoStore

char_width_map = {
    'F': 2,
    'W': 2,
    'A': 2,
    'H': 1,
    'Na': 1,
    'N': 1,
}

DEFAULT_WIDTH = 120

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def _rune_width(s: str) -> int:
    s = ANSI_ESCAPE.sub('', s)
    return sum(char_width_map[unicodedata.east_asian_width(c)] for c in s)


def _tty_width() -> Optional[int]:
    try:
        res = sp.run(['stty', 'size'], stdout=sp.PIPE, stderr=sp.DEVNULL)
        _, column = res.stdout.decode('utf-8').split()
    except Exception:
        return None
    return int(column)


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
        width = _tty_width()
        if width is None:
            return
        line_break_count = 0
        for store in self.task_info_stores:
            display_lines = store.get_line().split('\n')
            for line in display_lines:
                line_width = _rune_width(line)
                line_break_count += ((line_width - 1) // width) + 1
                print(f'{line}\033[K')
        print(CursorMove.up(line_break_count), end='')
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

    async def run(
        self,
        async_tasks: List[Awaitable[None]],
        prints_summary: bool = False
    ) -> bool:
        """
        Run all async job given.
        It returens whether all tasks finished successfully.
        """
        await asyncio.gather(*async_tasks, self.watch())
        self.flush()
        if prints_summary:
            self.print_task_summary()
        return all([store.is_success for store in self.task_info_stores])
