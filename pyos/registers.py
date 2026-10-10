import sys
from pyos.instruction import Instruction, InstructionArgType, InstructionType
from pyos.memory import Memory
from pyos.trap import Trap
from enum import IntEnum


class Register(IntEnum):
    RA=0
    RB=1
    RD=2
    RS=3

class CPU:
    REG_SIZE = 4
    def __init__(self, mem: Memory) -> None:
        self.ra: int = 0
        self.rb: int = 0
        self.rd: int = 0
        self.rs: int = 0
        self.mem: Memory = mem
        self.trap = Trap()

    def __str__(self) -> str:
        s = "\n  -".join([
            "CPU:",
            f"RA: {self.ra}",
            f"RB: {self.rb}",
            f"RD: {self.rd}",
            f"RS: {self.rs}",
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
            case InstructionType.MOV:
                print("Executing MOV")
                if len(instr.args) == 2: 
                    self._mov(instr)
                else:
                    sys.exit(f"Error: Expected MOV instruction to have 2 args. Got {len(instr.args)}")
            case InstructionType.SYSCALL:
                print("SYSCALLING me on my cellphone...")
                if len(instr.args) == 0:
                    self._syscall()
                else:
                    sys.exit(f"Error: Expected SYSCALL instruction to have 0 args. Got {len(instr.args)}")

    def _add(self, instr: Instruction):
        assert len(instr.args) == 2
        if (
            instr.args[0].arg_type == InstructionArgType.CONST 
            and instr.args[1].arg_type == InstructionArgType.REG
        ):
            print(f"Adding CONST({instr.args[0].val}) to REG({instr.args[1].val})")
            self._add_to_reg(instr.args[1].val, instr.args[0].val)
            return
        sys.exit("CPU-Error: Invalid ADD instruction")


    def _sub(self, instr: Instruction):
        assert len(instr.args) == 2
        if (
            instr.args[0].arg_type == InstructionArgType.CONST 
            and instr.args[1].arg_type == InstructionArgType.REG
        ):
            print(f"Subtracting CONST({instr.args[0].val}) to REG({instr.args[1].val})")
            self._sub_from_reg(Register(instr.args[1].val), instr.args[0].val)
            return
        sys.exit("CPU-Error: Invalid SUB instruction")

    def _mov(self, instr: Instruction):
        assert len(instr.args) == 2
        if (
            instr.args[0].arg_type == InstructionArgType.REG
            and instr.args[1].arg_type == InstructionArgType.CONST
        ):
            print(f"MOVing CONST({instr.args[1].val}) into REG({instr.args[0].val})")
            self._mov_const_to_reg(instr.args[1].val, Register(instr.args[0].val))
        elif (
            instr.args[0].arg_type == InstructionArgType.REG
            and instr.args[1].arg_type == InstructionArgType.REG
        ):
            print(f"MOVing REG({instr.args[1].val}) into REG({instr.args[0].val})")
            self._mov_reg_to_reg(Register(instr.args[1].val), Register(instr.args[0].val))
        elif (
            instr.args[0].arg_type == InstructionArgType.REG
            and instr.args[1].arg_type == InstructionArgType.MEM
        ):
            print(f"MOVing MEM({instr.args[1].val}) into REG({instr.args[0].val})")
            self._mov_mem_to_reg(instr.args[1].val, Register(instr.args[0].val))
        elif (
            instr.args[0].arg_type == InstructionArgType.MEM
            and instr.args[1].arg_type == InstructionArgType.REG
        ):
            print(f"MOVing REG({instr.args[1].val}) into MEM({instr.args[0].val})")
            self._mov_reg_to_mem(Register(instr.args[1].val), instr.args[0].val)
        else:
            sys.exit("CPU-Error: Invalid MOV instruction (might just be an unhandled case though)")


    def _syscall(self):
        print("Executing syscall")
        self.trap.syscall()

    def has_trapped(self) -> bool:
        return self.trap.has_trapped

    def _add_to_reg(self, reg_id: int, val: int):
        match reg_id:
            case 0:
                self.ra += val
            case 1:
                self.rb += val
            case _:
                sys.exit(f"Error: Unknown CPU register {reg_id}")

    def _sub_from_reg(self, reg_id: Register, val: int):
        match reg_id:
            case Register.RA:
                self.ra -= val
            case Register.RB:
                self.rb -= val
            case Register.RD:
                self.rd -= val
            case Register.RS:
                self.rs -= val

    def _mov_reg_to_reg(self, val: Register, target: Register):
        reg_val = 0
        match val:
            case Register.RA:
                reg_val = self.ra
            case Register.RB:
                reg_val = self.rb
            case Register.RD:
                reg_val = self.rd
            case Register.RS:
                reg_val = self.rs
        
        match target:
            case Register.RA:
                self.ra = reg_val 
            case Register.RB:
                self.rb = reg_val 
            case Register.RD:
                self.rd = reg_val 
            case Register.RS:
                self.rs = reg_val 

    def _mov_const_to_reg(self, val: int, target: Register):
        match target:
            case Register.RA:
                self.ra = val 
            case Register.RB:
                self.rb = val 
            case Register.RD:
                self.rd = val 
            case Register.RS:
                self.rs = val 

    def _mov_mem_to_reg(self, address: int, target: Register):
        val = self.mem.read_register(address)
        match target:
            case Register.RA:
                self.ra = val 
            case Register.RB:
                self.rb = val 
            case Register.RD:
                self.rd = val 
            case Register.RS:
                self.rs = val 

    def _mov_reg_to_mem(self, reg: Register, address: int):
        val = 0
        match reg:
            case Register.RA:
                val = self.ra
            case Register.RB:
                val = self.rb
            case Register.RD:
                val = self.rd
            case Register.RS:
                val = self.rs
        self.mem.write_register(address, val.to_bytes(length=4, byteorder="big", signed=False))

