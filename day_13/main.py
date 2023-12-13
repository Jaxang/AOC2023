import numpy as np


def parse_input(text):
    patterns = text.split("\n\n")
    return list(map(parse_pattern, patterns))
    
def parse_pattern(pattern):
    cols = pattern.find("\n")
    return np.array(list(map(int, pattern.replace("\n", "").replace(".", "0").replace("#", "1")))).reshape(-1, cols)

def solution(text):
    patterns = parse_input(text)
    output = list(map(check_pattern, patterns))
    return sum(output)

def check_pattern(pattern):
    horizontal = check_horisontal_2(pattern)
    if horizontal >-1:
        return horizontal*100
    vertical = check_horisontal_2(pattern.T)
    return vertical

def check_horisontal_2(pattern):
    diff = np.abs(np.diff(pattern, axis=0)).sum(1)
    match = (diff == 0) | (diff == 1)
    start_points = (match).nonzero()[0]
    for start_point in start_points:
        right_start = start_point+1
        if start_point < len(pattern)//2:
            left_start=0
            right_end = right_start*2
        else:
            right_end = len(pattern)
            left_start = right_start-(right_end - right_start)
        left = pattern[left_start:right_start][::-1]
        right = pattern[right_start:right_end]
        if np.abs(right-left).sum()==1:
            return right_start
    return -1
    
def check_horisontal_1(pattern):
    horizontal = np.array(list(map(hash_vector, pattern)))
    start_points = (np.diff(horizontal)==0).nonzero()[0]
    for start_point in start_points:
        right_start = start_point+1
        if start_point < len(horizontal)//2:
            left_start=0
            right_end = right_start*2
        else:
            right_end = len(horizontal)
            left_start = right_start-(right_end - right_start)
        left = horizontal[left_start:right_start][::-1]
        right = horizontal[right_start:right_end]
        if (left==right).all():
            return right_start
    return -1
    
def hash_vector(vector):
    return np.dot(vector, 2**np.arange(len(vector)))

def test_example():
    test_text = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    print(solution(test_text))
    

def get_answer(input_text):
    print(solution(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)