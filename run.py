import argparse
import contextlib
import importlib
import os
from time import time


def get_input_text(folder, as_lines=False):
    with open(f"{folder}/input.txt") as f:
        text = f.read()
    return text.split("\n") if as_lines else text


def get_args():
    parser = argparse.ArgumentParser(
                    prog='AoC',
                    description='Advent of Code 2023')
    parser.add_argument("day")
    return parser.parse_args()

def run_day(day):
    input_text = get_input_text(day)
    day_code = importlib.import_module(f"{day}.main")
    day_code.main(input_text)
    return day_code

def check_all_days():
    durations = {}

    for i in range(1, 25):
        day = f"day_{i}"
        try:
            with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stdout(devnull):
                    start = time()
                    run_day(day)
                    end = time()
                    durations[day] = end-start
        except NotImplementedError:
            print(f"{pretty_day(day)} not implemented yet")
            break
    else:
        print(f"Yaay! You are done with everything!") 
    print("Durations:")
    for day, duration in durations.items():
        print(f"{pretty_day(day)}: {duration} s")

def pretty_day(day):
    return day.capitalize().replace("_", " ")

if __name__ == "__main__":
    args = get_args()
    if args.day == "All days":
        print("Checking Progress")
        check_all_days()
    else:
        print(pretty_day(args.day))
        day_code = run_day(args.day)

