from enum import Enum
import sys

from pyos.instruction import Instruction, InstructionArg, InstructionArgType, InstructionType
from pyos.registers import CPU, Register
from pyos.state import StateKind, StateLog
from pyos.syscall import SysCall, SysCallType
from pyos.trap import TrapType


class ProcessStatus(Enum):
    RUNNING=1
    READY=2
    BLOCKED=3
    FINISHED=4


class Process:
    def __init__(
        self, 
        pid: int, 
        status: ProcessStatus, 
        address_space, 
        instructions: list[Instruction],
        cpu: CPU,
        fds: list[int] = [],
    ) -> None:
        self.pid = pid
        self.status = status
        self.child_processes = []
        self.fds = fds
        self.instructions = instructions
        self.cpu = cpu
        self.current_instruction = 0
        self.address_space = address_space
        self.stack = [0, 0] # initialize stack with zero registers

    def __str__(self) -> str:
        s = "\n  -".join([
            f"Process {self.pid} is {self.status}:",
            f"Children:      {self.child_processes}",
            f"Fds:           {self.fds}",
            f"Address space: {self.fds}",
            f"Instructions:  {self.instructions}",
            f"Current instr: {self.current_instruction}",
            f"Stack: {self.stack}",
        ])
        return s
    
    def execute_instr(self, debug):
        if self.status == ProcessStatus.FINISHED:
            sys.exit(f"Error: Trying to execute finished process {self.pid}.")
        elif self.current_instruction >= len(self.instructions):
            print("\tNo more instructions. Finishing process.")
            self.status = ProcessStatus.FINISHED
            print("Process finished with CPU state:\n", self.cpu)
            return
        instr = self.instructions[self.current_instruction]
        print(f"\tExecuting instruction {instr} for pid: {self.pid}")
        self.current_instruction += 1
        self.cpu.exec_instr(instr)
        if debug:
            debug.history.append(StateLog(kind=StateKind.Instruction, info={"cpu": str(self.cpu), "pid": self.pid, "instr": str(instr)}))

    def save_state(self):
        self.status = ProcessStatus.READY
        self.stack.extend([self.cpu.ra, self.cpu.rb])
        print(f"Saving process state for pid {self.pid}")
        print(self.stack)

    def load_state(self):
        self.status = ProcessStatus.RUNNING
        if len(self.stack) < 2:
            sys.exit(f"Trying to load state for process with too small stack: {self.stack}")
        print(f"Loading process state for pid {self.pid}")
        print("CPU before:", self.cpu)
        self.cpu.rb = self.stack.pop()
        self.cpu.ra = self.stack.pop()
        print("CPU after:", self.cpu)

    def _get_syscall(self) -> SysCall:
        # assert that trap is active and of type syscall
        assert self.cpu.trap 
        assert self.cpu.trap.type == TrapType.SYSCALL

        if max(TrapType, key=lambda c: c.value).value < self.cpu.ra:
            sys.exit(f"Error: Invalid syscall value {self.cpu.ra}")
        call_type = SysCallType(self.cpu.ra)
        args = []
        print("call type:", call_type)
        match call_type:
            case SysCallType.WRITE:
                # TODO: get sys call args from registers
                assert self.cpu.ra in self.fds, f"Unknown FD {self.cpu.ra}. FDs are {self.fds}"
                args = [self.cpu.ra, self.cpu.rb, bytearray([1,2,3])]
            case _: sys.exit("Error: Unhandled CPU trap")

        return SysCall(call_type, args)

def make_processes(cpu: CPU) -> list[Process]:
    p0 = Process(
        pid=0, 
        status=ProcessStatus.READY, 
        instructions=[
            Instruction(type=InstructionType.ADD, args=[
                InstructionArg(20, InstructionArgType.CONST),
                InstructionArg(int(Register.RA), InstructionArgType.REG)
            ]),
            Instruction(type=InstructionType.ADD, args=[
                InstructionArg(30, InstructionArgType.CONST),
                InstructionArg(int(Register.RA), InstructionArgType.REG)
            ]),
        ],
        cpu = cpu,
        address_space=[]
    )
    p1 = Process(
        pid=1, 
        status=ProcessStatus.READY, 
        instructions=[
            Instruction(type=InstructionType.ADD, args=[
                InstructionArg(30, InstructionArgType.CONST),
                InstructionArg(int(Register.RA), InstructionArgType.REG)
            ]),
            Instruction(type=InstructionType.SUB, args=[
                InstructionArg(29, InstructionArgType.CONST),
                InstructionArg(int(Register.RA), InstructionArgType.REG)
            ]),
            Instruction(type=InstructionType.MOV, args=[
                InstructionArg(int(Register.RB), InstructionArgType.REG),
                InstructionArg(int(Register.RA), InstructionArgType.REG)
            ]),
            Instruction(type=InstructionType.MOV, args=[
                InstructionArg(int(Register.RD), InstructionArgType.REG),
                InstructionArg(int(Register.RA), InstructionArgType.REG)
            ]),
            Instruction(type=InstructionType.MOV, args=[
                InstructionArg(int(Register.RB), InstructionArgType.REG),
                InstructionArg(2, InstructionArgType.MEM)
            ]),
            Instruction(type=InstructionType.MOV, args=[
                InstructionArg(int(Register.RA), InstructionArgType.REG),
                InstructionArg(500, InstructionArgType.CONST)
            ]),
            Instruction(type=InstructionType.MOV, args=[
                InstructionArg(2, InstructionArgType.MEM),
                InstructionArg(int(Register.RA), InstructionArgType.REG)
            ]),
            Instruction(type=InstructionType.MOV, args=[
                InstructionArg(int(Register.RB), InstructionArgType.REG),
                InstructionArg(2, InstructionArgType.MEM)
            ]),
            # Instruction(type=InstructionType.SYSCALL, args=[]),
        ],
        cpu = cpu,
        address_space=[]
    )
    return [p0, p1]
