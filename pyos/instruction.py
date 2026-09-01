from enum import Enum

class InstructionType(Enum):
    ADD=1
    SUB=2
    SYSCALL=3

class InstructionArgType(Enum):
    CONST=1
    MEM=2
    REG=3

class InstructionArg:
    def __init__(self, val: int, arg_type: InstructionArgType) -> None:
        self.val = val
        self.arg_type = arg_type

class Instruction:
    def __init__(self, type: InstructionType, args: list[InstructionArg] = []) -> None:
        self.type = type
        self.args = args

    def __str__(self) -> str:
        return f"{self.type} ({self.args})"
