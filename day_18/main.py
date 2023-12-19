from collections import defaultdict
from functools import partial

import numpy as np

DIRECTION_MAP = {
    "D": np.array((1,0)),
    "U": np.array((-1,0)),
    "L": np.array((0,-1)),
    "R": np.array((0,1)),
}


def parse_input(text, star=1):
    return list(map(partial(parse_line, star=star), text.split("\n")))

def parse_line(line, star=1):
    direction, steps, color = line.split(" ")
    if star==2:
        hex_encoding = {c: i for i, c in enumerate(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"])}
        hex_exponens = 16**np.arange(5)[::-1]
        direction = ["R", "D", "L", "U"][int(color[-2])]
        steps = (list(map(lambda x: hex_encoding[x], color[2:-2]))*hex_exponens).sum()
    return direction, int(steps)

def solution(text, star=1):
    instructions = parse_input(text, star=star)
    row_wall_map = defaultdict(lambda : defaultdict(str))
    
    filled = 0
    current_position = np.array((0,0))
    for direction, steps in instructions:
        d = DIRECTION_MAP[direction]
        filled += steps
        row_wall_map[current_position[0]][current_position[1]] += direction
        for i in range(steps):
            current_position = tuple(np.array(current_position) + d)
            if direction in ["U", "D"] and i<steps-1:
                row_wall_map[current_position[0]][current_position[1]] = "|"
        row_wall_map[current_position[0]][current_position[1]] += direction

    for _, col_data in row_wall_map.items():
        state = 0
        col_data = sorted(col_data.items())
        for (col_s, d_s), (col_e, _) in zip(col_data[:-1], col_data[1:]):
            if sorted(d_s) == ["R","U"]:
                state += 0.5
            elif sorted(d_s) == ["D","R"]:
                state -= 0.5
            elif sorted(d_s) == ["L","U"]:
                state += 0.5
            elif sorted(d_s) == ["D","L"]:
                state -= 0.5
            else:
                state = (state + 1)%2
            if state==1:
                filled += col_e-col_s-1

    return filled
        

def test_example():
    test_text = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    test_text_2 = """R 3 (#70c710)
D 1 (#0dc571)
R 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
U 3 (#411b91)
R 2 (#8ceee2)
U 1 (#caa173)
R 2 (#1b58a2)
D 5 (#caa171)
L 11 (#7807d2)
U 4 (#a77fa3)"""
    print(solution(test_text))
    print(solution(test_text_2))
    print(solution(test_text, star=2))
    

def get_answer(input_text):
    print(solution(input_text))
    print(solution(input_text, star=2))


def main(input_text):
    test_example()
    get_answer(input_text)