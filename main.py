from pyos.kernel import Kernel
from pyos.registers import CPU
from pyos.process import make_processes

def main():
    cpu = CPU()
    kernel = Kernel()
    p0, p1 = make_processes(cpu)
    print(f"p: {p0}\n{p1}")

    kernel.add_process(p0)
    kernel.add_process(p1)

    kernel.run()
    print(cpu)


if __name__ == "__main__": main()


