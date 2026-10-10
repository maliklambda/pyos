from pyos.kernel import Kernel
from pyos.registers import CPU
from pyos.memory import Memory
from pyos.process import make_processes

def main():
    mem = Memory(512)
    cpu = CPU(mem)
    kernel = Kernel()
    processes = make_processes(cpu)
    print(f"Processes: {processes}")

    for p in processes:
        kernel.add_process(p)

    kernel.run()
    print(cpu)
    print(mem)


if __name__ == "__main__": main()


