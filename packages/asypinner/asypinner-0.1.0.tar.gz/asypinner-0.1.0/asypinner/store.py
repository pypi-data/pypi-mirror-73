from enum import Enum, auto
from typing import List
from datetime import datetime
from dataclasses import dataclass

from .log import TaskLog, LogStatus
from .misc import red, blue, green

SPINNERS = [
    "⠋",
    "⠙",
    "⠹",
    "⠸",
    "⠼",
    "⠴",
    "⠦",
    "⠧",
    "⠇",
    "⠏"
]

SUCCESS_MARKER = "✔"
FAILURE_MARKER = "✖"


class TaskStatus(Enum):

    WAITING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILURE = auto()


@dataclass
class TaskInfoStore:

    title: str
    logs: List[TaskLog]
    exit_log: TaskLog
    status: TaskStatus

    spinner_index: int

    @property
    def message(self) -> str:
        if self.logs == []:
            return ''
        else:
            return self.logs[-1].message

    @property
    def is_success(self) -> bool:
        return self.status == TaskStatus.SUCCESS

    @property
    def is_failed(self) -> bool:
        return self.status == TaskStatus.FAILURE

    @property
    def is_finished(self) -> bool:
        return self.is_success or self.is_failed

    def __init__(self, title: str) -> None:
        self.title = title
        self.logs = []
        self.exit_log = TaskLog(
            '',
            datetime.now(),
            LogStatus.INFO,
        )
        self.status = TaskStatus.WAITING
        self.spinner_index = 0
        return

    def _start_running(self) -> None:
        if self.status == TaskStatus.WAITING:
            self.status = TaskStatus.RUNNING
            self.spinner_index = 0
        return

    def _log_wrapper(self, message: str, log_status: LogStatus) -> None:
        self._start_running()
        self.logs.append(TaskLog(
            message=message,
            time=datetime.now(),
            log_status=log_status,
        ))

    def info(self, message: str) -> None:
        return self._log_wrapper(message, LogStatus.INFO)

    def success(self, message: str) -> None:
        return self._log_wrapper(message, LogStatus.SUCCESS)

    def warning(self, message: str) -> None:
        return self._log_wrapper(message, LogStatus.WARNING)

    def failure(self, message: str) -> None:
        return self._log_wrapper(message, LogStatus.FAILURE)

    def finish(self, exit_message: str, is_success: bool = True) -> None:
        self.exit_log = TaskLog(
            message=exit_message,
            time=datetime.now(),
            log_status=LogStatus.SUCCESS if is_success else LogStatus.FAILURE
        )
        if is_success:
            self.status = TaskStatus.SUCCESS
        else:
            self.status = TaskStatus.FAILURE
        return

    def get_line(self) -> str:
        """
        Get status marker of the job.
        """
        if self.status == TaskStatus.WAITING:
            return '{} {} : {}\033[K'.format(
                blue(self.get_spinner()),
                self.title,
                "Waiting job to start",
            )
        elif self.status == TaskStatus.RUNNING:
            return '{} {} : {}\033[K'.format(
                green(self.get_spinner()),
                self.title,
                self.message,
            )
        elif self.status == TaskStatus.FAILURE:
            return '{} {} : {}\033[K'.format(
                red(FAILURE_MARKER),
                self.title,
                self.exit_log.message,
            )
        elif self.status == TaskStatus.SUCCESS:
            return '{} {} : {}\033[K'.format(
                green(SUCCESS_MARKER),
                self.title,
                self.exit_log.message,
            )
        else:
            raise ValueError

    def print_summary(self) -> None:
        """ Print finished summary information.
        """
        print(f'Taks {self.title}')
        for log in self.logs:
            print(log)
        print(self.exit_log)
        return

    def get_spinner(self) -> str:
        """
        Get the current spinner.
        It modifies the current spinner, so the next call to this function,
        will change its content.
        """
        current_spinner = SPINNERS[self.spinner_index]
        self.__increment_spinner_index()
        return current_spinner

    def __increment_spinner_index(self) -> None:
        if self.spinner_index >= len(SPINNERS) - 1:
            self.spinner_index = 0
        self.spinner_index += 1
        return
