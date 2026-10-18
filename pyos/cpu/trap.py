from enum import Enum
from typing import Optional


class TrapType(Enum):
    SYSCALL=1

class Trap:
    def __init__(self) -> None:
        self.has_trapped = False
        self.type: Optional[TrapType] = None

    def __bool__(self) -> bool:
        return self.has_trapped
    
    def syscall(self):
        self.has_trapped = True
        self.type = TrapType.SYSCALL

