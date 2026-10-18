from re import split

from pyos.memory import Memory
import sys
import struct

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
        addr_bytes = pack_16bit(self.current_addr)
        assert len(addr_bytes) == self.ADDR_SIZE/8, "Missmatch in addr_bytes-conversion: Expected {self.ADDR_SIZE/8}, got {len(addr_bytes)}"
        (lower_byte, displacement_byte) = addr_bytes[0:1], addr_bytes[1:]
        displacement = int.from_bytes(displacement_byte, byteorder='big', signed=False)
        (segment, page) = split_bits(lower_byte)
        tlb_lookup = self.tlb.lookup(segment, page)
        if tlb_lookup:
            return join_bits(upper=displacement, lower=tlb_lookup, lower_bits=self.PAGE_FRAME_BITS, size=self.ADDR_SIZE)
        sys.exit("TODO: Walk segment-table & page-table to retrieve page-frame")
        page_frame = self._get_page_frame(segment, page)
        self.tlb.add_entry(segment, page, page_frame)


def split_bits(byte_val: bytes) -> tuple[int, int]:
    assert len(byte_val) == 1, "Invalid size"
    # Create a mask for the lower bits (e.g., 4 bits -> 0b1111 or 15)
    upper = byte_val[0] >> 4
    lower = byte_val[0] & 0x0F
    return (upper, lower)

def pack_16bit(val: int) -> bytes:
    assert val < 2**16, f"Address Conversion Error: Address ({val}) exceeds 16bit"
    # '>H' means Big-Endian, 2-byte Unsigned Short (16 bits); '<H' would be Little-Endian
    return struct.pack('>H', val)

def unpack_16bit(high_byte: int, low_byte: int) -> int:
    packed = bytes([high_byte, low_byte])
    return struct.unpack('>H', packed)[0]

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
