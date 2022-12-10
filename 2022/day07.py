from dataclasses import dataclass, field
from functools import cached_property


def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()


day_number = 7
part1_test_solution = 95437
part2_test_solution = 24933642
test_input = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip(
    "\n"
)


input_raw = read_file_to_one_big_string(f"2022/data/day{day_number:02d}/input.txt")


@dataclass(frozen=True)
class Folder:
    name: str
    files: list["File"] = field(default_factory=list)
    folders: list["Folder"] = field(default_factory=list)

    @cached_property
    def children(self):
        return self.files + self.folders

    @cached_property
    def size(self):
        return sum(item.size for item in self.children)


@dataclass(frozen=True)
class File:
    name: str
    size: int


def parse_input(input_raw):
    lines = input_raw.splitlines()
    all_folders: list[Folder] = []
    stack: list[Folder] = []
    for line in lines:
        if line == "$ cd ..":
            stack.pop()
        elif line.startswith("$ cd"):
            folder_name = line.split(" ")[2]
            folder = Folder(folder_name)
            all_folders.append(folder)
            if stack:
                stack[-1].folders.append(folder)
            stack.append(folder)
            pass
        elif line == "$ ls":
            pass
        elif line.startswith("dir "):
            pass
        else:
            size, filename = line.split(" ")
            size = int(size)
            file = File(filename, size)
            stack[-1].files.append(file)
    return all_folders


def part1(input_raw: str):
    all_folders = parse_input(input_raw)
    return sum(folder.size for folder in all_folders if folder.size < 100_000)


def part2(input_raw: str):
    all_folders = parse_input(input_raw)
    sizes = [folder.size for folder in all_folders]
    used_space = sizes[0]
    free_space = 70_000_000 - used_space
    additional_space_required = max(30_000_000 - free_space, 0)
    sizes.sort()
    for size in sizes:
        if size > additional_space_required:
            return size


if part1_test_solution is None:
    print(f"Part 1 Test: {part1(test_input)}")
    quit()

assert part1(test_input) == part1_test_solution
print(f"Part 1: {part1(input_raw)}")

if part2_test_solution is None:
    print(f"Part 2 Test: {part2(test_input)}")
    quit()

assert part2(test_input) == part2_test_solution
print(f"Part 2: {part2(input_raw)}")
