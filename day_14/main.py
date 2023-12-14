import numpy as np

DIRECTIONS = ["N", "W", "S", "E"]

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

def solution(text):
    arr = parse_input(text)
    return count_from_top(arr)

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