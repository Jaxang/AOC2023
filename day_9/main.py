import numpy as np


def get_next_value(line):
    last_diffs = [line[-1]]
    first_diffs = [line[0]]
    current = line
    while(True):
        diff = np.diff(current)
        last_diffs.append(diff[-1])
        first_diffs.append(diff[0])
        if np.all(diff==0):
            break
        current = diff
    next_value= sum(last_diffs)
    prev_value = first_diffs[-1]
    for value in first_diffs[::-1]:
        prev_value = value - prev_value
    return next_value, prev_value

def solution(text):
    lines = [
        np.array([int(value) for value in line.split() if value]) 
        for line in text.split("\n")]
    next_values, prev_values = list(zip(*[get_next_value(line) for line in lines]))
    return sum(next_values), sum(prev_values)

def test_example():
    test_text = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    print(solution(test_text))

    

def get_answer(input_text):
    print(solution(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)