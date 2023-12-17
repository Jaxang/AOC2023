import heapq

import numpy as np

MOVE_MAP = {
    (0,0): (0,0),
    (-1,0): (1,0), 
    (1,0): (-1,0), 
    (0,-1): (0,1), 
    (0,1): (0,-1)
}

def parse_input(text):
    cols = text.find("\n")
    grid = np.array(list(map(int, text.replace("\n", "")))).reshape(-1, cols)
    return grid

def astar(grid, start, goal, minimum_steps=1, maximum_steps=3):
    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = grid.shape
    
    open_set = []
    closed_set = set()
    
    start_state = (start, (0,0), 0)
    
    
    heapq.heappush(open_set, (0, ) + start_state)
    
    while open_set:
        current_cost, current_node, current_move, current_steps = heapq.heappop(open_set)
        current_state = (current_node, current_move, current_steps)
        
        if current_node == goal:
            return current_cost
        if current_state in closed_set:
            continue
        closed_set.add((current_state))
        
        for move in movements:
            if move == MOVE_MAP[current_move]:
                continue
            steps_to_take = 1 if move == current_move else minimum_steps
            steps = current_steps if move == current_move else 0
            
            cost_diff = 0
            neighbor = np.array(current_node)
            for _ in range(steps_to_take):
                steps += 1
                neighbor += np.array(move)
                new_state = (tuple(neighbor), tuple(move), steps)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                    cost_diff  += grid[*neighbor]
                else:
                    break

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and steps<=maximum_steps and new_state not in closed_set:
                new_cost = current_cost  + cost_diff
                heapq.heappush(open_set, (new_cost,)+ new_state)
    return None

def reconstruct_path(start, goal, came_from):
    current = goal
    path = [current[0]]
    move = [current[1]]
    while current != start:
        current = came_from[current]
        path.append(current[0])
        move.append(current[1])
    path.reverse()
    move.reverse()
    return path, move


def solution(text):
    grid = parse_input(text)
    rows, cols = grid.shape
    minimum_cost = astar(grid, (0,0), (rows-1, cols-1))
    minimum_cost_2 = astar(grid, (0,0), (rows-1, cols-1), 4, 10)
    return minimum_cost, minimum_cost_2


def test_example():
    test_text = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
    test_text_2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""
    print(solution(test_text))
    print(solution(test_text_2))
    

def get_answer(input_text):
    print(solution(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)