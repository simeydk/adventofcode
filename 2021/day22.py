from functools import cached_property
from typing import Iterable, List, NamedTuple, Tuple, Union
import re
import numpy as np
from math import prod
from itertools import product
from dataclasses import dataclass

DAY = 22
TEST_SOLUTION_1 = 590784
TEST_SOLUTION_2 = None # 2758514936282235

x = 1_000_000_000_000_000_000_000_000_000_000
y = 10 ** 100
print(y)
print(y * y)

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

def parse_line(line: str):
    result = re.findall('(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line)[0]
    on = result[0] == 'on'
    x_min, x_max, y_min, y_max, z_min, z_max = [int(x) for x in result[1:]]
    x_max = x_max + 1
    y_max = y_max + 1
    z_max = z_max + 1
    return on, np.array([x_min, x_max]), np.array([y_min, y_max]), np.array([z_min, z_max])

def parse_input(data: str):
    return [parse_line(line) for line in data.splitlines()]


def clamp_instruction(instruction, grid_ranges):
    on, x_range, y_range, z_range = instruction
    x_range = x_range.clip(*grid_ranges[0])
    y_range = y_range.clip(*grid_ranges[1])
    z_range = z_range.clip(*grid_ranges[2])
    new_instruction = on, x_range, y_range, z_range
    return new_instruction

def process_subgrid(grid_ranges, instructions):
    clamped_instructions = [clamp_instruction(instruction, grid_ranges) for instruction in instructions]
    grid = np.zeros([hi - low for low, hi in grid_ranges], dtype=bool)
    for on, x_range, y_range, z_range in clamped_instructions:
        x_range -= grid_ranges[0][0]
        y_range -= grid_ranges[1][0]
        z_range -= grid_ranges[2][0]
        grid[x_range[0]:x_range[1], y_range[0]:y_range[1], z_range[0]:z_range[1]] = on
    return np.sum(grid)

def part1(data: str) -> int:
    instructions = parse_input(data)
    grid_ranges = [(-50,51), (-50,51), (-50,51)]
    return process_subgrid(grid_ranges, instructions)

def biggest_ranges(instructions):
    min_x = min(x_range[0] for on, x_range, y_range, z_range in instructions)
    max_x = max(x_range[1] for on, x_range, y_range, z_range in instructions)
    min_y = min(y_range[0] for on, x_range, y_range, z_range in instructions)
    max_y = max(y_range[1] for on, x_range, y_range, z_range in instructions)
    min_z = min(z_range[0] for on, x_range, y_range, z_range in instructions)
    max_z = max(z_range[1] for on, x_range, y_range, z_range in instructions)
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)

def split_range(the_range: Tuple[int], chunk_size = 1000) -> List[Tuple[int]]:
    low, hi = the_range
    return [(start, min(start + chunk_size, hi)) for start in range(low, hi,chunk_size)]

def split_ranges(ranges, chunk_sizes):
    splits = [split_range(r, c) for r, c in zip(ranges, chunk_sizes)]
    return product(*splits)
@dataclass(frozen=True)
class Side:
    start: int
    end: int = None

    def __post_init__(self, *args):
        if self.end is not None: return
        
        args = self.start
        _set = lambda key, value: object.__setattr__(self, key, value)
        if type(args) == int:
            _set("start", 0)
            _set("end", args)
        else:
            _set("start", args[0])
            _set("end", args[1])

        if self.end < self.start:
            raise ValueError("End must be greater than start")

    @cached_property
    def size(self) -> int:
        size = self.end - self.start
        if size < 0: raise ValueError(f"Negative Side size: {size}")
        return size

    def intersect(self, other: 'Side') -> 'Side':
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start < end:
            return Side(start, end)
        else:
            return None

    def split(self, split_points: Union[int, Iterable[int]]) -> List['Side']:
        if type(split_points) == int: split_points = [split_points]
        split_points = sorted(point for point in split_points if point > self.start and point < self.end)
        split_points = [self.start, *split_points, self.end]
        return [Side(split_points[i], split_points[i+1]) for i in range(len(split_points)-1)]

s = Side(0, 10)
t = Side(0,10)
print(Side(10), Side(0, 10), Side((0,10)))
assert Side(10) == Side(0, 10) 
assert Side(10) == Side((0,10))
assert Side(0,1) == Side(0,1)
assert Side(0,10).split(5) == [Side(0,5), Side(5,10)]
assert Side(0,10).split([2,5]) == [Side(0,2), Side(2,5), Side(5,10)]
assert Side(0,10).split([2,5, -7, 15]) == [Side(0,2), Side(2,5), Side(5,10)]
assert Side(0,10).split(-1) == [Side(0,10)]

@dataclass(frozen=True)
class Cube:
    x: Side
    y: Side
    z: Side

    def __post_init__(self):
        _set = lambda key, value: object.__setattr__(self, key, value)
        if type(self.x) != Side: _set('x', Side(self.x))
        if type(self.y) != Side: _set('y', Side(self.y))
        if type(self.z) != Side: _set('z', Side(self.z))

    def intersect(self, other: 'Cube') -> 'Cube':
        x = self.x.intersect(other.x)
        y = self.y.intersect(other.y)
        z = self.z.intersect(other.z)
        if x and y and z:
            return Cube(x, y, z)

    @cached_property
    def size(self) -> int:
        return np.prod(np.array([self.x.size, self.y.size, self.z.size]))
    
    def split(self, x_splits: Union[int, Iterable[int]] = [], y_splits: Union[int, Iterable[int]] = [], z_splits: Union[int, Iterable[int]] = []) -> List['Cube']:
        x_sides = self.x.split(x_splits)
        y_sides = self.y.split(y_splits)
        z_sides = self.z.split(z_splits)
        return [Cube(x, y, z) for x, y, z in product(x_sides, y_sides, z_sides)]

    def __repr__(self):
        return f"Cube(({self.x.start}, {self.x.end}), ({self.y.start}, {self.y.end}), ({self.z.start}, {self.z.end}))"

c = lambda x: Cube(x, x, x)

assert Cube((0,10), (0,10), (0,10)) == Cube(Side(0,10), Side(0,10), Side(0,10))
assert c(10) == Cube((0,10), (0,10), (0,10))

assert c(10).split() == [c(10)]
assert Cube(10, 10, 10).split(5) == [Cube(5, 10, 10), Cube((5,10), 10, 10)]

assert Cube(10, 10, 10).split(5,3) == [Cube((0, 5), (0, 3), (0, 10)), Cube((0, 5), (3, 10), (0, 10)), Cube((5, 10), (0, 3), (0, 10)), Cube((5, 10), (3, 10), (0, 10))]

def total_area(cubes: List[Tuple[bool, Cube]]) -> int:
    positives: List[Cube] = []
    negatives: List[Cube] = []
    for on, cube in cubes:
        pos_intersects = filter(lambda x: x, [cube.intersect(pos_cube) for pos_cube in positives])
        neg_intersects = filter(lambda x: x, [cube.intersect(neg_cube) for neg_cube in negatives])
        if on: positives.append(cube)
        negatives.extend(pos_intersects)
        positives.extend(neg_intersects)
    total = 0
    for cube in positives:
        # print (f"{total:,d} + {cube.size:,d}")
        total += cube.size 
    for cube in negatives: 
        # print (f"{total:,d} - {cube.size:,d}")
        total -= cube.size
    return total
    # return sum(cube.size for cube in positives) - sum(cube.size for cube in negatives)



assert total_area([(True, c(10)), (False, c(5))]) == 10 ** 3 - 5 ** 3

def part2(data: str) -> int:
    lines = parse_input(data)
    cubes = [(on, Cube(x, y, z)) for on, x, y, z in lines]
    return total_area(cubes)



test_input = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""

# test_input = """on x=10..12,y=10..12,z=10..12
# on x=11..13,y=11..13,z=11..13
# off x=9..11,y=9..11,z=9..11
# on x=10..10,y=10..10,z=10..10"""

test_input_2 = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""

assert part1(test_input_2) == 474140

input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

if TEST_SOLUTION_1:
    assert part1(test_input) == TEST_SOLUTION_1
    print(f"Solution 1:\n{part1(input_raw)}")
    if TEST_SOLUTION_2:
        assert part2(test_input_2) == TEST_SOLUTION_2
        print(f"Solution 2:\n{part2(input_raw)}")
    else:
        print(f"Test 2:\n{part2(test_input_2)}")
else:
    print(f"Test 1:\n{part1(test_input)}")
    
