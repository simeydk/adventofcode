from time import perf_counter
from typing import List, Set, Tuple
import numpy as np
from itertools import permutations, product

DAY = 19
TEST_SOLUTION_1 = 79
TEST_SOLUTION_2 = None

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

def parse_scanner_string(string: str) -> np.ndarray:
    header, *content = string.splitlines()
    l = [line.split(',') for line in content]
    return np.array(l, dtype=np.int8)

def parse_input(data: str):
    scanners_raw = data.split('\n\n')
    return [parse_scanner_string(s) for s in scanners_raw]

def make_transforms() -> List[np.ndarray]:
    rotations = [
        [[0,1,0], [-1,0,0], [0,0,1]],
        [[1,0,0], [0,0,-1], [0,1,0]],
        [[0,0,1], [0,1,0], [-1,0,0]],
    ]
    identity = np.identity(3, dtype = np.int8)

    tuples = set()
    for rx, ry, rz in product(range(4), repeat =3):
        transform = identity
        for _ in range(rx): transform = np.matmul(transform, rotations[0])
        for _ in range(ry): transform = np.matmul(transform, rotations[1])
        for _ in range(rz): transform = np.matmul(transform, rotations[2])
        tuples.add(tuple(transform.reshape(9)))
    
    transforms = [np.array(t, dtype=np.int8).reshape([3,3]) for t in tuples]

    return transforms

transforms = make_transforms()

def equal(a, b) -> bool:
    return np.all(np.array_equal(np.sort(a,0), np.sort(b,0)))

def nd_to_set(mx: np.ndarray) -> set:
    return set(tuple(row) for row in mx)

def set_to_nd(s: Set[Tuple[int]]) -> np.ndarray:
    return np.array(list(s), dtype=np.int8)

def part1(data: str) -> int:
    start = perf_counter()
    scanners = parse_input(data)
    # for i, scanner in enumerate(scanners): scanner.number = i
    transfroms = make_transforms()
    scanners_to_process = [*scanners]
    processed_scanners = []
    scanner = scanners_to_process.pop(0)
    beacon_set = nd_to_set(scanner)
    beacon_mx = set_to_nd(beacon_set)
    assert equal(scanner, beacon_mx)
    while scanners_to_process:
        scanner = scanners_to_process.pop(0)
        found_scanner = False
        for t_num, transform in enumerate(transforms):
            if found_scanner: break
            scanner_transformed = np.matmul(scanner, transform)
            # print(scanner_transformed)
            for nb_num, new_beacon in enumerate(scanner_transformed):
                if found_scanner: break
                if new_beacon[0] == 686:
                    print("scanner686")
                for ob_num, old_beacon in enumerate(beacon_set):
                    if old_beacon[0] == -618 and new_beacon[0] == 686:
                        print("found demo")
                    offset = new_beacon - old_beacon
                    scanner_offset = scanner_transformed - offset
                    scanner_offset_set = nd_to_set(scanner_offset)
                    if len(beacon_set.intersection(scanner_offset_set)) >= 12:
                        beacon_set = beacon_set.union(scanner_offset_set)
                        processed_scanners.append((scanner, transform, offset))
                        found_scanner = True
                        print(f"Found scanner. {len(processed_scanners)} found. {len(beacon_set)} beacons. {len(scanners_to_process)} scanners left. running for {perf_counter() - start:.2f}s")
                        break
        if not found_scanner: 
            scanners_to_process.append(scanner)
    return len(beacon_set)

def part2(data: str) -> int:
    pass



test_input = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


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
    

def rotations():
    
    flips = []

