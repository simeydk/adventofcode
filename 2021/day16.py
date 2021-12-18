from typing import List
from io import StringIO
from dataclasses import dataclass, field
from inspect import signature
from math import prod

DAY = 16
TEST_SOLUTION_1 = 12
TEST_SOLUTION_2 = 46

@dataclass
class Packet:
    version: int
    type: int

    version_sum: int = field(init=False, default = 0, repr = False, compare = False)

    value: int = field(init=False, default = 0, repr = False, compare = False)

@dataclass 
class Literal(Packet):
    value: int

    @property
    def version_sum(self):
        return self.version

@dataclass 
class Operator(Packet):
    subpackets: List[Packet]

    @property
    def version_sum(self) -> int:
        return self.version + sum(packet.version_sum for packet in self.subpackets)

    @property
    def value(self) -> int:
        sub_values = [packet.value for packet in self.subpackets]
        if self.type == 0:
            return sum(sub_values)
        elif self.type == 1:
            return prod(sub_values)
        elif self.type == 2:
            return min(sub_values)
        elif self.type == 3:
            return max(sub_values)
        elif self.type == 5:
            return (sub_values[0] > sub_values[1]) * 1
        elif self.type == 6:
            return (sub_values[0] < sub_values[1]) * 1
        elif self.type == 7:
            return (sub_values[0] == sub_values[1]) * 1
        else:
            raise Exception(f"Unknown operator type: {self.type}")
        


def hex_to_bin(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

def parse_input(data: str) -> StringIO:
    return StringIO(hex_to_bin(data))

def parse_packet(stream: StringIO):
    version = int(stream.read(3), 2)
    type_id = int(stream.read(3), 2)
    if type_id == 4: # Literal
        num_bin = ''
        proceed = True
        while proceed:
            proceed = stream.read(1) == '1'
            num_bin += stream.read(4)
        return Literal(version, type_id, int(num_bin, 2))
    else:
        operator_mode = stream.read(1)
        subpackets = []
        if operator_mode == '0':
            subpackets_len = int(stream.read(15), 2)
            cursor_start = stream.tell()
            while stream.tell() - cursor_start < subpackets_len:
                subpackets.append(parse_packet(stream))
        elif operator_mode == '1':
            num_subpackets = int(stream.read(11), 2)
            for i in range(num_subpackets):
                subpackets.append(parse_packet(stream))
        else:
            raise Exception(f'Unknown operator mode: {operator_mode}')
        return Operator(version, type_id, subpackets)

def part1(data: str) -> int:
    stream = parse_input(data)
    return parse_packet(stream).version_sum
    


def part2(data: str) -> int:
    stream = parse_input(data)
    return parse_packet(stream).value

test_input = "620080001611562C8802118E34"

assert part1("8A004A801A8002F478") == 16
assert part1("620080001611562C8802118E34") == 12
assert part1("C0015000016115A2E0802F182340") == 23
assert part1("A0016C880162017C3686B18A3D4780") == 31


assert part2("C200B40A82") == 3
assert part2("04005AC33890") == 54
assert part2("880086C3E88112") == 7
assert part2("CE00C43D881120") == 9
assert part2("D8005AC2A8F0") == 1
assert part2("F600BC2D8F") == 0
assert part2("9C005AC2F8F0") == 0
assert part2("9C0141080250320F1802104A08") == 1

input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

if TEST_SOLUTION_1:
    assert part1(test_input) == TEST_SOLUTION_1
    print(f"Solution 1:\n{part1(input_raw)}")
    if TEST_SOLUTION_2:
        assert part2(test_input) == TEST_SOLUTION_2
        print(f"Solution 2:\n{part2(input_raw)}")
    else:
        print(f"Test 2:\n{part2(test_input)}")
else:
    print(f"Test 1:\n{part1(test_input)}")
    

