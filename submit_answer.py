
import argparse
from utils.api import submit_answer
from utils.utils import parse_puzzle_code

  

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_code",nargs='?', default="")
    parser.add_argument("part", choices=['1','2'])
    parser.add_argument("answer")
    # parser.add_argument("-s", "--session", default="")
    args = parser.parse_args()
    
    print(f"{args=}")

    

    puzzle_code = args.puzzle_code
    year, day = parse_puzzle_code(puzzle_code)
    res = submit_answer(year,day, args.part, args.answer)
    print(res.text)
    