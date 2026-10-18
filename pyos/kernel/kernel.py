import sys

from .process import Process, ProcessStatus
from .syscall import SysCall, SysCallType
from pyos.state import StateKind, StateLog
from pyos.cpu.trap import TrapType


class Kernel:
    def __init__(self) -> None:
        # TODO: Add priority to each process
        self.active_processes: list[Process] = []
        # The id of the process that is currently being executed
        self.current_pid = None

    def __str__(self) -> str:
        processes_str = "\n".join([p.__str__() for p in self.active_processes])
        return "\n".join([
            "Scheduler:",
            f" Current-PID: {self.current_pid}",
            " Processes:",
            processes_str,
        ])

    def run(self, debug = None):
        self._grab_new_current_process()
        idx = 0

        while len(self.active_processes) > 0:
            print(f"\n--- Current PID: {self.current_pid} ---")
            new_pid = self.active_processes[idx%len(self.active_processes)].pid
            print(f"--- New PID: {new_pid} ---")
            self.exec_process(new_pid, debug)
            idx += 1
            if debug:
                debug.history.append(StateLog(kind=StateKind.ContextSwitch, info={"ctx": True}))

    def add_process(self, process: Process):
        if process.pid in [p.pid for p in self.active_processes]:
            sys.exit(f"Error: Duplicate PID {process.pid}")
        self.active_processes.append(process)

    def _get_current_process(self) -> Process | None:
        process_lst = [p for p in self.active_processes if p.pid == self.current_pid]
        if len(process_lst) != 1: 
            print(f"Process {self.current_pid} is not active")
            [print(p.pid) for p in self.active_processes]
            print([p.pid for p in self.active_processes if p.pid == self.current_pid])
            return None
        assert len(process_lst) == 1
        print(process_lst)
        [print(p.pid) for p in self.active_processes]
        return process_lst[0]
    
    def _grab_new_current_process(self):
        if len(self.active_processes) > 0:
            self.current_pid = self.active_processes[0].pid

    def _switch_context(self, new_pid: int):
        print(f"Switching context from {self.current_pid} to {new_pid}")
        # Save state of the old process
        current_process = self._get_current_process()
        if current_process: current_process.save_state()

        # switch to new process
        if new_pid not in [p.pid for p in self.active_processes]:
            sys.exit(f"Error: PID {new_pid} cannot be switched to, as it is not known by the scheduler")
        print(f"Updating current pid from {self.current_pid} to {new_pid}")
        self.current_pid = new_pid

        # Load state of the new process
        current_process_new = self._get_current_process()
        if not current_process_new:
            return
        current_process_new.load_state()

    def exec_process(self, pid: int, debug):
        self._switch_context(pid)
        print("switched context")
        num_of_instructions = 1
        process = self._get_current_process()
        if not process: return
        print(f"Executing {num_of_instructions} instruction(s) for process {process.pid}")
        for _ in range(num_of_instructions):
            process.execute_instr(debug)
            if process.cpu.has_trapped():
                if debug:
                    debug.history.append(StateLog(kind=StateKind.Trap, info={"trap": True}))
                print("CPU trapped")
                self._handle_cpu_trap(process)
            if process.status == ProcessStatus.FINISHED: 
                print(f"Removing process {process.pid}")
                self.remove_process(process.pid)

    def remove_process(self, pid: int):
        self.active_processes = [p for p in self.active_processes if p.pid != pid]

    def _handle_cpu_trap(self, process: Process):
        print("Handling cpu trap")
        match process.cpu.trap.type:
            case TrapType.SYSCALL:
                call = process._get_syscall()
                self._syscall(call)
            case _:
                sys.exit("Error: Unhandled CPU trap")

    def _syscall(self, syscall: SysCall):
        match syscall.type:
            case SysCallType.WRITE:
                print("Write-SysCall")
                assert len(syscall.args) >= 3, "Cannot execute WRITE syscall with less than 3 args. Need fd, offset, buffer"
                self._write(syscall.args[0], syscall.args[1], syscall.args[2])
            case SysCallType.OPEN:
                print("Open-SysCall")
                assert len(syscall.args) >= 3, "Cannot execute WRITE syscall with less than 3 args. Need fd, offset, buffer"
                self._write(syscall.args[0], syscall.args[1], syscall.args[2])
            case _: sys.exit(f"Error: Unhandled syscall-kernel-interface: {syscall.type}")

    def _write(self, fd: int, offset: int, buffer: bytearray):
        sys.exit(f"TODO: write syscall kernel")


