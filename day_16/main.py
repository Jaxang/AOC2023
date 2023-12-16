import bisect
from collections import defaultdict

import numpy as np

MAPPED_ROWS = "mapped_rows"
MAPPED_COLS = "mapped_cols"
START_POSITION = np.array([0,0])
START_DIRECTION = np.array([0,1])

def parse_input(text):
    cols = text.find("\n")
    grid = np.array(list(text.replace("\n", ""))).reshape(-1, cols)
    object_coords = fixed_map(grid!=".")
    return grid, object_coords

def fixed_map(fixed):
    fixed_rows_1, fixed_cols_1 = fixed.nonzero()
    sort_idx = [i for _, _, i in sorted(zip(fixed_cols_1,fixed_rows_1, np.arange(len(fixed_cols_1))))]
    fixed_rows_2, fixed_cols_2 = fixed_rows_1[sort_idx], fixed_cols_1[sort_idx]
    mapping = defaultdict(lambda: {MAPPED_ROWS: [], MAPPED_COLS:[]})
    for i in range(len(fixed_rows_2)):
        mapping[fixed_rows_1[i]][MAPPED_COLS].append(fixed_cols_1[i])
        mapping[fixed_cols_2[i]][MAPPED_ROWS].append(fixed_rows_2[i])
    return mapping

def map_directions(grid_object, direction):
    if grid_object == "\\":
        return [direction[::-1]]
    if grid_object == "/":
        return [-direction[::-1]]
    if (direction[1]==0 and grid_object=="|") or (direction[0]==0 and grid_object=="-"):
        return [direction]
    if grid_object == "|":
        return [np.array([-1,0]), np.array([1,0])]
    if grid_object == "-":
        return [np.array([0,-1]), np.array([0,1])]
    raise ValueError("Error")

def check_bounds(position, shape):
    return ((position >= 0) & (position < shape)).all()

def step(grid, object_coords, energised, visited, position=START_POSITION, direction=START_DIRECTION, first=True):
    if not check_bounds(position, grid.shape):
        return
    if (tuple(position)+tuple(direction)) in visited:
        return
    major_axis = (direction[0]==0)*1
    major, minor = position[major_axis], position[1-major_axis]
    d = direction[major_axis]
    mapping_label = [MAPPED_ROWS, MAPPED_COLS][major_axis]
    objects = object_coords[minor][mapping_label]
    new_major_idx = bisect.bisect_left(objects, major)
    if first:
        new_major_idx -= d<0
    else: 
        new_major_idx += d
    
    out = True
    if new_major_idx == -1:
        new_major = 0
    elif new_major_idx == len(objects):
        new_major = grid.shape[major_axis] -1
    else:
        out = False
        new_major = objects[new_major_idx]
    
    if major_axis == 0:
        if d==1:
            energised[major:new_major+1, minor]=1
        else:
            energised[new_major:major+1, minor]=1
    else:
        if d==1:
            energised[minor, major:new_major+1]=1
        else:
            energised[minor, new_major:major+1]=1
    visited.add(tuple(position)+tuple(direction))
    
    if out:
        return
    new_poistion = np.array((new_major, minor) if major_axis==0 else (minor, new_major))
    grid_object = grid[new_poistion[0], new_poistion[1]]
    new_directions = map_directions(grid_object, direction)
    for direction in new_directions:
        step(grid, object_coords, energised, visited, new_poistion, direction, False)


def solution(text):
    grid, object_coords = parse_input(text)
    size = grid.shape[0]
    best = -1
    for i in range(size):
        for position, direction in zip(
            [(0, i), (size-1, i), (i, 0), (i, size-1)],
            [(1, 0), (-1, 0), (0, 1), (0, -1)]
            ):
            energised = np.zeros_like(grid, dtype=int)
            visited = set()
            step(grid, object_coords, energised, visited, position=np.array(position), direction=np.array(direction))
            tmp = energised.sum()
            if tmp > best:
                best=tmp
    return best

def test_example():
    test_text = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    print(solution(test_text))
    

def get_answer(input_text):
    print(solution(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)