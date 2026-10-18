from pyos.memory import Memory
import sys

class MMU:
    def __init__(self, mem: Memory, tlb_size: int) -> None:
        self.mem: Memory = mem
        self.paging_enabled = True # Enable paging by default
        self.current_addr = 0
        self.SEGMENT_BITS = 4
        self.PAGE_BITS = 4
        self.PAGE_FRAME_BITS = self.SEGMENT_BITS + self.PAGE_BITS
        self.DISPLACEMENT_BITS = 8
        self.ADDR_SIZE = self.PAGE_FRAME_BITS + self.DISPLACEMENT_BITS
        self.tlb = TLB(entry_size=tlb_size)
    
    def resolve_addr(self, addr: int) -> int:
        self.current_addr = addr
        if self.paging_enabled:
            print("Resolving virtual address...")
            return self._resolve_virtual_addr()
        else:
            print("Resolving read address...")
            return self.current_addr

    """ 
        Virtual Address Composition:
            - (0..4)    Segment-bits
            - (4..8)    Page-bits
            - (8..16)   Displacement-bits

        Retrieve virtual address:
            1. Split 16bit int in half (lower, upper)
                -> displacement = upper
            2. Split lower in half, yielding (segment, page)
    """
    def _resolve_virtual_addr(self) -> int:
        (lower, displacement) = split_bits(self.current_addr, lower_bits=self.PAGE_FRAME_BITS, size=self.ADDR_SIZE)
        (segment, page) = split_bits(lower, lower_bits=self.SEGMENT_BITS, size=self.PAGE_FRAME_BITS)
        tlb_lookup = self.tlb.lookup(segment, page)
        if tlb_lookup:
            return join_bits(upper=displacement, lower=tlb_lookup, lower_bits=self.PAGE_FRAME_BITS, size=self.ADDR_SIZE)
        sys.exit("TODO: Walk segment-table & page-table to retrieve page-frame")

def split_bits(val: int, lower_bits: int, size: int) -> tuple[int, int]:
    assert val.bit_count() == size, f"Missmatch in int-size: expected {size}, got {val.bit_count()}"
    # Create a mask for the lower bits (e.g., 4 bits -> 0b1111 or 15)
    mask = (1 << lower_bits) - 1
    upper = val >> lower_bits
    lower = val & mask
    return (upper, lower)

def join_bits(upper: int, lower: int, lower_bits: int, size: int) -> int:
    assert upper.bit_count() + lower.bit_count() == size, f"Missmatch in int-size: expected {size}, got lower({lower.bit_count()} + upper({upper.bit_count()}))"
    return (upper << lower_bits) | lower


class TLB():
    MAX_ENTRIES_ABS = 512
    def __init__(self, entry_size: int) -> None:
        assert entry_size > 0 and entry_size <= self.MAX_ENTRIES_ABS, "Invalid TLB size"
        self.max_sz = entry_size
        self.num_entries = 0
        # {(segment_id, page_id): page_frame_id}
        self.data: dict[tuple[int, int], int] = {}

    def lookup(self, segment_id: int, page_id: int) -> int | None:
        if (segment_id, page_id) in self.data.keys():
            print("TLB-HIT!!!!!")
            return self.data[(segment_id, page_id)]
        else: 
            print("TLB-MISS!!!!!")
            return None

    def add_entry(self, segment_id: int, page_id: int, page_frame_id: int):
        if self.num_entries < self.max_sz: self.num_entries += 1
        else: self.data.popitem()
        self.data[(segment_id, page_id)] = page_frame_id
