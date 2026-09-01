from pyos.scheduler import Scheduler
from pyos.registers import CPU
from pyos.process import make_processes

def main():
    scheduler = Scheduler()
    cpu = CPU()
    p0, p1 = make_processes(cpu)
    print(f"p: {p0}\n{p1}")

    scheduler.add_process(p0)
    scheduler.add_process(p1)

    scheduler.loop()
    print(cpu)


if __name__ == "__main__": main()


