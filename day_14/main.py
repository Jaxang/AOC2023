import bisect
from collections import defaultdict

import numpy as np

DIRECTIONS = ["N", "W", "S", "E"]
DIRECTION_MAPPING = dict(zip(DIRECTIONS, [(-1,0), (0,-1), (1,0), (0,1)]))
MAPPED_ROWS = "mapped_rows"
MAPPED_COLS = "mapped_cols"

def parse_input(text):
    cols = text.find("\n")
    arr = np.array(list(text.replace("\n", ""))).reshape(-1, cols)
    return arr

def count_from_top(arr):
    rows, cols = arr.shape
    trackers = [[[rows, 0]] for _ in range(cols)]
    for i, row in enumerate(arr):
        for j, value in enumerate(row):
            if value == "#":
                trackers[j].append([rows-(i+1), 0])
            if value == "O":
                trackers[j][-1][1] += 1
    weights = [int((r - (n-1)/2)*n) for col_trackers in trackers for r, n in col_trackers]
    return trackers, sum(weights)

def map_to_closest_fixed(rolling_coords, fixed_mapping, direction, shape):
    mapping = defaultdict(lambda: 0)
    output = []
    major_idx = (direction[0]==0)*1
    d, max_major, map_key = direction[major_idx], shape[major_idx], [MAPPED_ROWS, MAPPED_COLS][major_idx]
    rolling_coords = sorted(rolling_coords, key=lambda x: x[major_idx], reverse=d>0)
    for i, j in rolling_coords:
        major, minor = [i,j][::((1-major_idx)*2-1)]
        blocking_rocks = fixed_mapping[minor][map_key]
        lower_idx = bisect.bisect_left(blocking_rocks, major) - (d<0)
        new_major = 0 if (lower_idx == -1) else (max_major-1) if (lower_idx==len(blocking_rocks)) else (blocking_rocks[lower_idx] - d)
        
        offset = mapping[(new_major, minor)]
        mapping[(new_major, minor)] += 1
        new_major -= d*offset
        new_coord = (new_major, minor) if direction[1]==0 else (minor, new_major)
        output.append(new_coord)
    return output
        
def fixed_map(fixed):
    fixed_rows_1, fixed_cols_1 = fixed.nonzero()
    sort_idx = [i for _, _, i in sorted(zip(fixed_cols_1,fixed_rows_1, np.arange(len(fixed_cols_1))))]
    fixed_rows_2, fixed_cols_2 = fixed_rows_1[sort_idx], fixed_cols_1[sort_idx]
    mapping = defaultdict(lambda: {MAPPED_ROWS: [], MAPPED_COLS:[]})
    for i in range(len(fixed_rows_2)):
        mapping[fixed_rows_1[i]][MAPPED_COLS].append(fixed_cols_1[i])
        mapping[fixed_cols_2[i]][MAPPED_ROWS].append(fixed_rows_2[i])
    return mapping

def calculate_load(rolling_coords, max_value): 
    return sum([max_value-r for r, _ in rolling_coords])

def hash_coords(rolling_coords, shape):
    coord_value = np.arange(shape[0]*shape[1]).reshape(shape)
    rows, cols = list(zip(*rolling_coords))
    return tuple(sorted(coord_value[rows, cols]))

def run_cycle(rolling_coords, fixed_mapping, shape):
    load = 0
    for label, direction in DIRECTION_MAPPING.items():
        rolling_coords = map_to_closest_fixed(rolling_coords, fixed_mapping, direction, shape)
        if label == "N":
            load = calculate_load(rolling_coords, max_value=shape[0])
    return load, rolling_coords

def solution(text):
    arr = parse_input(text)
    first_top = count_from_top(arr)
    rolling = (arr == "O")*1
    fixed = (arr=="#")*1
    fixed_mapping = fixed_map(fixed)
    loads = []
    rolling_coords = list(zip(*rolling.nonzero()))
    cache = {}
    TOTAL_STEPS = 1000000000
    for i in range(TOTAL_STEPS):
        if (start_hash:=hash_coords(rolling_coords, arr.shape)) in cache:
            break
        load, rolling_coords_ = run_cycle(rolling_coords, fixed_mapping, arr.shape)
        tmp_hash = hash_coords(rolling_coords_, arr.shape)
        cache[start_hash] = load, tmp_hash, rolling_coords_
        rolling_coords = rolling_coords_
        loads.append(load)
    steps_left = TOTAL_STEPS - (i+1)    
        
    load_cycle, next_hash, rolling_coords = cache[start_hash]
    steps = 1
    while (next_hash != start_hash):
        tmp_load, next_hash, rolling_coords = cache[next_hash]
        load_cycle += tmp_load
        steps += 1
    cycles = steps_left//steps
    total_load = load + load_cycle*cycles
    
    steps = i + cycles*steps
    while steps < TOTAL_STEPS:
        tmp_load, next_hash, rolling_coords = cache[next_hash]
        total_load += tmp_load
        steps += 1
    load = calculate_load(rolling_coords, max_value=arr.shape[0])
    return first_top, load

def test_example():
    test_text = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    print(solution(test_text))
    

def get_answer(input_text):
    print(solution(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)