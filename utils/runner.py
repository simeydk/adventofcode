from typing import Callable


Solution = int|str|None
Part_Solver = Callable[[str], Solution]

def runner(part1: Part_Solver, part2: Part_Solver, 
           test_input: str, puzzle_input: str, 
           test_solution_1: Solution = None, 
           test_solution_2: Solution = None):
    
    part1_test_result = part1(test_input)
    if type(part1_test_result) == str and len(part1_test_result.splitlines()) > 1:
        sep = '\n'
    else:
        sep = " "
    print(f"Part 1 test result: {part1_test_result}")
    if test_solution_1 == None:
        print('No test solution for Part 1 provided. Please specify a test solution for part 1')
        return
    elif test_solution_1 == part1_test_result:
        print('PASS: Test result matches expected result.\nRunning Part 1 on puzzle input')
    else: 
        print(f'FAIL: Part 1 test result did not match expected result. Expected Result was \n{test_solution_1}')
        return
    
    part1_result = part1(puzzle_input)
    print('')
    print(f"Part 1 result: {part1_result}")
    print('')

    part2_test_result = part2(test_input)
    if type(part2_test_result) == str and len(part2_test_result.splitlines()) > 1:
        sep = '\n'
    else:
        sep = " "
    print(f"Part 2 test result: {part2_test_result}")
    if test_solution_2 == None:
        print('No test solution for Part 2 provided. Please specify a test solution for part 2')
        return
    elif test_solution_2 == part2_test_result:
        print('PASS: Test result matches expected result.\nRunning Part 2 on puzzle input')
    else: 
        print(f'FAIL: Part 2 test result did not match expected result. Expected Result was \n{test_solution_1}')
        return
    
    part2_result = part2(puzzle_input)
    print('')
    print(f"Part 2 result: {part2_result}")
    print('')