from enum import Enum


class SysCallType (Enum):
    WRITE = 1
    READ = 2
    OPEN = 3

class SysCall:
    def __init__(self, call_type: SysCallType, args: list = []) -> None:
        self.type = call_type
        self.args = args

