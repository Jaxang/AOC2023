import re
from functools import partial
from math import comb

import numpy as np


def parse_input(text, star=1):
    lines = text.split("\n")
    spots_all, conditions_all = list(zip(*list(map(partial(parse_line, star=star), lines))))
    return spots_all, conditions_all

def parse_line(line, star=1):
    spots, conditions = line.split(" ")
    re.sub(".+",".",spots)
    if star==2:
        spots = "?".join([spots for _ in range(5)])
        conditions=",".join([conditions for _ in range(5)])
    conditions = list(map(int, conditions.split(",")))
    return spots, conditions


def check_line(spots, conditions_sorted):
    spots = spots.strip(".")
    min_spots_len = sum(i for i, _ in conditions_sorted) +len(conditions_sorted) -1
    if len(spots) < min_spots_len:
        return int(len(conditions_sorted)==0), 1
    if len(conditions_sorted)==0:
        return int(spots.find("#")==-1), 1
    
    if spots == "?"*len(spots):
        extra = len(spots) - min_spots_len
        return comb(extra+len(conditions_sorted)-1, extra), 1

    spots = f".{spots}."
    condition, idx = conditions_sorted[0]
    matches = list(re.finditer(rf"(?=([#?]){{{condition}}})", spots))
    
    possibilities = 0
    depth = 1
    for match in matches:
        start_pos, _ = match.span()
        end_pos = start_pos+condition
        start_pos = max(start_pos-1, 0) #start_pos is shifted by the added "." and we also want to remove the character before
        if "#" in [spots[start_pos], spots[end_pos]]:
            continue
        end_pos += 1
        
        left, depth_l = check_line(spots=spots[:start_pos], conditions_sorted=[cond for cond in conditions_sorted if cond[1]<idx])
        if left==0:
            continue
        right, depth_r = check_line(spots=spots[end_pos:], conditions_sorted=[cond for cond in conditions_sorted if cond[1]>idx])
        possibilities += left*right
        depth = max(depth, depth_l+1, depth_r+1)
    return possibilities, depth

BASE_PATTERN = "([#?]{{{}}})"
JOIN_PATTERN=("[^#]{{1,{}}}")

def count_outcomes(spots, conditions):
    n_conditions = len(conditions)
    min_end_index = np.cumsum(conditions) + np.arange(n_conditions)
    max_wiggle = len(spots) - min_end_index[-1]
    max_end_index = min_end_index + max_wiggle +1
    join_pattern = JOIN_PATTERN.format(max_wiggle+1)
    join_pattern.join([BASE_PATTERN.format(condition) for condition in conditions])
    
    conditions_sorted=sorted(zip(conditions, range(n_conditions)), key=lambda x: (x[0], -x[1]), reverse=True)
    solutions, depth = check_line(spots, conditions_sorted)
    print(depth)
    return solutions

def solution(text, star=1):
    spots, conditions = parse_input(text, star=star)
    n_possible_outcomes = list(map(count_outcomes, spots, conditions))
    return sum(n_possible_outcomes)

def test_example():
    test_text = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    print(solution(test_text,star=1))
    print(solution(test_text,star=2))
    

def get_answer(input_text):
    print(solution(input_text,star=1))
    print(solution(input_text,star=2))


def main(input_text):
    test_example()
    get_answer(input_text)