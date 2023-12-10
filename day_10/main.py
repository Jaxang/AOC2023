import matplotlib.pyplot as plt
import numpy as np

DEFAULT_SHOW_IMAGE = False

PIPES = {
    "|": ("N", "S"),
    "-": ("E", "W"),
    "L": ("N", "E"),
    "J": ("N", "W"),
    "7": ("S", "W"),
    "F": ("S", "E"),
    ".": (".", "."),
    "S": ("N", "E", "W", "S")
}
DIRECTIONS = {
    "N": np.array((-1, 0)),
    "E": np.array((0, 1)),
    "W": np.array((0, -1)),
    "S": np.array((1, 0)),
}
OPPOSIT_DIRECTIONS = {
    "N": "S",
    "E": "W",
    "W": "E",
    "S": "N",
}
RIGHT_DIRECTIONS = {
    "N": "E",
    "E": "S",
    "W": "N",
    "S": "W",
}

def valid_bounds(position, grid_shape):
    return ((position>=np.zeros(2)) & (position < np.array(grid_shape))).all()

def flood_fill(grid, visited, position):
    # Check if the current cell is within the grid boundaries and is not part of the boundary
    row, col =position
    if not valid_bounds(position, grid.shape):
        return True
    elif visited[row,col]==0:
        # Replace the current cell with the replacement value
        grid[row,col] = 2
        visited[row,col]=1

        # Recursively call the function for the neighboring cells
        return any([flood_fill(grid, visited, position+DIRECTIONS[direction]) for direction in ["N", "E", "W", "S"]])
    else:
        return False
    

def dfs(grid, visited, position, incomming_direction, step=0):
    while True:
        row, col = position
        if not valid_bounds(position, grid.shape):
            return -1
        
        pipe = grid[row, col]
        if pipe == "S":
            visited[row, col] = 1
            break
        
        directions = PIPES[pipe]
        if incomming_direction not in directions:
            return -1
        assert len(directions)==2
        
        out_direction = directions[1-directions.index(incomming_direction)]
        opposit_incoming_dir = OPPOSIT_DIRECTIONS[incomming_direction]
        for travling_directions in set((opposit_incoming_dir, out_direction)):
            right_dir = RIGHT_DIRECTIONS[travling_directions]
            if right_dir in directions:
                continue
            right_pos = position + DIRECTIONS[right_dir]
            r, c = right_pos
            if valid_bounds(right_pos, grid.shape) and visited[r,c]==0:
                r, c = right_pos
                visited[r,c] = 2
        
        visited[row, col] = 1
        position = position + DIRECTIONS[out_direction]
        incomming_direction = OPPOSIT_DIRECTIONS[out_direction]
        step+=1
    return step
    

def solution(text, show_image=DEFAULT_SHOW_IMAGE):
    lines = text.split("\n")
    cols, rows = len(lines[0]), len(lines)
    grid = np.array(list(text.replace("\n",""))).reshape(rows, cols)
    visited = np.zeros_like(grid, dtype=int)
    start_index = text.find("S")
    start_col, start_row = start_index%(cols+1), start_index//(cols+1)
    position = np.array([start_row, start_col])
    for d in PIPES["S"]:
        new_pos = position + DIRECTIONS[d]
        opposit_d = OPPOSIT_DIRECTIONS[d]
        visited = np.zeros_like(grid, dtype=int)
        steps = dfs(grid, visited, new_pos, opposit_d, 1)
        if steps > 0:
            print("steps: ", steps//2)
            path = (visited==1)*1
            marked_right_hand_cells = (visited==2).nonzero()
            touched_edge = any([flood_fill(visited, path, np.array(position)) for position in zip(*marked_right_hand_cells)])
            if touched_edge:
                print("inside left hand: ", np.sum(visited==0))
            else:
                print("inside right hand: ", np.sum(visited==2))
            
            if show_image:
                plt.figure(figsize=grid.shape)
                plt.imshow(visited)
                inside_position = np.array(plt.ginput(1)[0])[::-1].round().astype(int)
                print("inside: ", np.sum(visited==visited[*inside_position]))
            print("inside right hand: ", np.sum(visited==2), "inside left hand: ", np.sum(visited==0))
            break
    

def test_example(show_image=DEFAULT_SHOW_IMAGE):
    test_text_1a = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
    test_text_1b = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
    test_text_2a = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    test_text_2b = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
    test_text_2c = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    solution(test_text_1a, show_image)
    solution(test_text_1b, show_image)
    solution(test_text_2a, show_image)
    solution(test_text_2b, show_image)
    solution(test_text_2c, show_image)
    

def get_answer(input_text, show_image=DEFAULT_SHOW_IMAGE):
    solution(input_text, show_image)


def main(input_text, show_image=DEFAULT_SHOW_IMAGE):
    test_example(show_image)
    get_answer(input_text, show_image)