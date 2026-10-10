
class Memory():
    MIN_SIZE = 512
    def __init__(self, size: int) -> None:
        assert size >= self.MIN_SIZE, f"Need at mem-size of at least {self.MIN_SIZE}, got {size}."
        arr = [0]*size
        self.data = bytearray(arr)

    def __str__(self) -> str:
        s = f"{self.data}"
        return s

    def _assert_address_range_abs(self, address: int, n: int):
        assert address > 0 and address < len(self.data), f"Invalid address: {address} (data: {len(self.data)})"
        assert n > 0 and address + n < len(self.data), f"Invalid address (n): {address} ({n})"

    def _read(self, address: int, n: int):
        self._assert_address_range_abs(address, n)
        return self.data[address:address+n]

    def read_krnl(self, address: int, n: int):
        return self._read(address, n)

    def read_process(self, address: int, n: int):
        # TODO: enforce constraints on memory-reads for non-kernel processes
        return self._read(address, n)

    # read a value of size Register-Value
    def read_register(self, address: int):
        bytes = self.read_process(address, 4)
        return int.from_bytes(bytes, byteorder='big', signed=False)

    def _write(self, address: int, val: bytes):
        print("Writing to address ", address)
        self._assert_address_range_abs(address, len(val))
        self.data = self.data[0:address] + val + self.data[address+len(val):]

    def write_krnl(self, address: int, val: bytes):
        self._write(address, val)

    def write_process(self, address: int, val: bytes):
        # TODO: enforce constraints on memory-writes for non-kernel processes
        self._write(address, val)

    # write a value of size Register-Value
    def write_register(self, address: int, val: bytes):
        self.write_process(address, val)

