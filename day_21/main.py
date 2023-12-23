from collections import deque

import numpy as np


def parse_input(text):
    cols = text.find("\n")
    arr = np.array(list(text.replace("\n", ""))).reshape(-1, cols)
    start = np.where(arr=="S")
    walk_able = arr =="."
    walk_able[start] = True
    return walk_able, (start[0],start[1])

def bfs(walkable, start_point, steps):
    queue = deque()
    queue.append((start_point, 0))
    rows, cols = walkable.shape
    visited = {0: {}, 1: {}}
    while len(queue) > 0:
        (row, col), step  = queue.popleft()
        array_row, array_col = row%rows, col%cols
        parity = step%2
        if ((not walkable[array_row,array_col]) or ((row,col) in visited[parity]) or step > steps) :
            continue
        visited[parity][(row, col)] = step
        for i,j in [(-1, 0), (1, 0), (0,-1), (0, 1)]:
            queue.append(((row+i, col+j), step+1))
    return visited

def solution(text, steps = 64):
    walk_able, start = parse_input(text)
    
    row, col = map(int, start)
    visited = bfs(walk_able, (row, col), steps)
    return len(visited[steps%2])

def solution_2(text, steps = 26501365):
    walk_able, start = parse_input(text)
    
    row, col = map(int, start)
    rows, cols = walk_able.shape
    for i in range(0,7,2):
        n = 65 + 131*i
        m = 65 + 131*(i+2)
        visited = bfs(walk_able, (row, col), n)
        visited_2 = bfs(walk_able, (row, col), m)
        visited_romb = [s for (r,c), s in visited_2[1].items() if (abs(r - row) + abs(c - col)) <= n]
        print(i, len(visited[1]), len(visited_romb))
    print("Paste into wolframalpha to get it solve the sequence ´:D")
    
    def func(i):
        return 33943 - 90754*i + 60632*i**2
    full_i = (steps-65)//(131*2)
    return func(full_i)

def test_example():
    test_text = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    print(solution(test_text, 6))
    

def get_answer(input_text):
    print(solution(input_text, 64))
    print(solution_2(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)