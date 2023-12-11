import numpy as np


def parse_text(text):
    cols = text.find("\n")
    img = np.array(list(map(int, text.replace("\n", "").replace(".", "0").replace("#", "1")))).reshape(-1, cols)
    return img

def solution(text, replacement=2):
    img = parse_text(text)
    galaxy_row, galaxy_col= img.nonzero()
    row_idx_mapping = np.cumsum([1 if i in galaxy_row else replacement for i in range(img.shape[0])])
    col_idx_mapping = np.cumsum([1 if i in galaxy_col else replacement for i in range(img.shape[1])])
    galaxy_coord = np.array([(row_idx_mapping[r], col_idx_mapping[c]) for r, c in zip(galaxy_row,galaxy_col) ])
    distances = np.abs((np.expand_dims(galaxy_coord, axis=0) - np.expand_dims(galaxy_coord, axis=1))).sum(-1)
    return distances.sum()//2

def test_example():
    test_text = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    print(solution(test_text, 2))
    print(solution(test_text, 10))

    

def get_answer(input_text):
    print(solution(input_text, 2))
    print(solution(input_text, 1000000))


def main(input_text):
    test_example()
    get_answer(input_text)