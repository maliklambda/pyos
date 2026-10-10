from enum import Enum

class State:
    def __init__(self) -> None:
        self.history = []

    def __bool__(self) -> bool:
        return True

    def __str__(self) -> str:
        return f"States: {self.history}"

class StateKind(Enum):
    Instruction=0
    Trap=1
    ContextSwitch=2

class StateLog:
    def __init__(self, kind: StateKind, info: dict) -> None:
        self.kind = kind
        self.info = info

    def __str__(self) -> str:
        return f"{self.kind} " + str(self.info)



