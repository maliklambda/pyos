from .process import ProcessStatus, Process
from pyos.cpu import CPU, Register, Instruction, InstructionType, InstructionArg, InstructionArgType


def make_processes(cpu:CPU) -> list[Process]:
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
