import sys
from pyos.instruction import Instruction, InstructionArgType, InstructionType
from pyos.trap import Trap


class CPU:
    def __init__(self) -> None:
        self.ra: int = 0
        self.rb: int = 0
        self.trap = Trap()

    def __str__(self) -> str:
        s = "\n  -".join([
            "CPU:",
            f"RA: {self.ra}",
            f"RB: {self.rb}",
        ])
        return s

    def exec_instr(self, instr: Instruction):
        print("CPU executing instr")
        match instr.type:
            case InstructionType.ADD:
                print("Executing ADD")
                if len(instr.args) == 2: 
                    self._add(instr)
                else:
                    sys.exit(f"Error: Expected ADD instruction to have 2 args. Got {len(instr.args)}")
            case InstructionType.SUB:
                print("Executing SUB")
                if len(instr.args) == 2: 
                    self._sub(instr)
                else:
                    sys.exit(f"Error: Expected SUB instruction to have 2 args. Got {len(instr.args)}")
            case InstructionType.SYSCALL:
                print("SYSCALLING me on my cellphone...")
                if len(instr.args) == 0:
                    self._syscall()
                else:
                    sys.exit(f"Error: Expected SYSCALL instruction to have 0 args. Got {len(instr.args)}")
            case _:
                sys.exit(f"Error: Unhandled instruction type: {instr.type}")

    def _add(self, instr: Instruction):
        assert len(instr.args) == 2
        if (
            instr.args[0].arg_type == InstructionArgType.CONST 
            and instr.args[1].arg_type == InstructionArgType.REG
        ):
            print(f"Adding CONST({instr.args[0].val}) to REG({instr.args[1].val})")
            self._add_to_reg(instr.args[1].val, instr.args[0].val)
            return
        sys.exit("Todo: CPU execute ADD")


    def _sub(self, instr: Instruction):
        assert len(instr.args) == 2
        if (
            instr.args[0].arg_type == InstructionArgType.CONST 
            and instr.args[1].arg_type == InstructionArgType.REG
        ):
            print(f"Subtracting CONST({instr.args[0].val}) to REG({instr.args[1].val})")
            self._sub_from_reg(instr.args[1].val, instr.args[0].val)
            return
        sys.exit("Todo: CPU execute SUB")

    def _syscall(self):
        print("Executing syscall")
        self.trap.syscall()

    def has_trapped(self) -> bool:
        return self.trap

    def _add_to_reg(self, reg_id: int, val: int):
        match reg_id:
            case 0:
                self.ra += val
            case 1:
                self.rb += val
            case _:
                sys.exit(f"Error: Unknown CPU register {reg_id}")

    def _sub_from_reg(self, reg_id: int, val: int):
        match reg_id:
            case 0:
                self.ra -= val
            case 1:
                self.rb -= val
            case _:
                sys.exit(f"Error: Unknown CPU register {reg_id}")
