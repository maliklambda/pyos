from enum import Enum

class InstructionType(Enum):
    ADD=1 # ADD val to dst
    SUB=2 # SUB val from dst
    SYSCALL=3 # Initiate syscall
    MOV=4 # MOV into dst val

class InstructionArgType(Enum):
    CONST=1
    REG=2
    MEM=3

class InstructionArg:
    def __init__(self, val: int, arg_type: InstructionArgType) -> None:
        self.val = val
        self.arg_type = arg_type

    def __str__(self) -> str:
        return f"{self.val} ({self.arg_type})"

class Instruction:
    def __init__(self, type: InstructionType, args: list[InstructionArg] = []) -> None:
        self.type = type
        self.args = args

    def __str__(self) -> str:
        s = " ".join([
            "Instruction:",
            str(self.type),
            "(",
            " - ".join(str(arg) for arg in self.args),
            ")"
        ])
        return s

