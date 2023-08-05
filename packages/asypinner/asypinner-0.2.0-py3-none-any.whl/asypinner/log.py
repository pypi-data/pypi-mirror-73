from enum import Enum, auto
from datetime import datetime
from dataclasses import dataclass

from .misc import red, blue, green, yellow


class LogStatus(Enum):

    INFO = auto()
    SUCCESS = auto()
    FAILURE = auto()
    WARNING = auto()


@dataclass(frozen=True)
class TaskLog:

    message: str
    time: datetime
    log_status: LogStatus

    def __repr__(self) -> str:
        if self.log_status == LogStatus.INFO:
            return ('{} {}'.format(
                blue(f'[{self.time}]'),
                self.message,
            ))
        elif self.log_status == LogStatus.SUCCESS:
            return ('{} {}'.format(
                green(f'[{self.time}]'),
                self.message,
            ))
        elif self.log_status == LogStatus.FAILURE:
            return ('{} {}'.format(
                red(f'[{self.time}]'),
                self.message,
            ))
        elif self.log_status == LogStatus.WARNING:
            return ('{} {}'.format(
                yellow(f'[{self.time}]'),
                self.message,
            ))
        raise ValueError
