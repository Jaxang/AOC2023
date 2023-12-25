from collections import defaultdict, deque

import numpy as np


def parse_input(text):
    first_coords, second_coords, axis_of_change, extent = list(map(np.array,list(zip(*list(map(parse_line, text.split("\n")))))))
    sorted_z_idx = np.argsort(first_coords[:,2])
    return first_coords[sorted_z_idx], second_coords[sorted_z_idx], axis_of_change[sorted_z_idx], extent[sorted_z_idx]

def parse_line(line):
    first_coord, second_coord = list(map(parse_coord, line.split("~")))
    diff = second_coord - first_coord
    axis_of_change = np.where(diff)[0]
    if len(axis_of_change) == 0:
        axis_of_change = np.array([2])
        extent = np.array([0])
    else:
        extent = diff[axis_of_change]
        if extent < 0:
            first_coord, second_coord = second_coord, first_coord
            extent = -extent
    return first_coord, second_coord, axis_of_change, extent
    
def parse_coord(coord_str):
    return np.array(list(map(int, coord_str.split(","))))

def find_all_supported_by_base(base, supports_one_step):
    queue = deque()
    queue.append(base)
    supports = set()
    while len(queue) > 0:
        current = queue.popleft()
        for tmp in supports_one_step[current]:
            supports.add(tmp)
            queue.append(tmp)
    return supports

def count_from_top(current, supports_one_step, supported_by, cache, visited):
    if len(cache[current])!=0:
        visited |= cache[current][0]
        return cache[current][-1]
    single_support = len(supported_by[current]) <= 1
    current_visited = set()    
    for i in supports_one_step[current]:
        tmp_visited = set()
        add_to_current = count_from_top(i, supports_one_step, supported_by, cache, tmp_visited)
        visited |= tmp_visited
        if add_to_current:
            current_visited |= tmp_visited
    current_count = len(current_visited)
    current_visited.add(current)
    visited |= current_visited
    cache[current] = visited, current_count, single_support
    return single_support

def count_from_top_2(current, supports_one_step, supported_by, cache, branch):
    if current in cache:
        _, current_visited, _, _= cache[current]
        return set(), current_visited
    branch=set([current])
    current_visited=set([current])
    for i in supports_one_step[current]:
        tmp_branch, tmp_visited = count_from_top_2(i,supports_one_step, supported_by, cache, branch)
        branch |= tmp_branch
        current_visited |= tmp_visited

    if len(supported_by[current]) != 1 or len(supports_one_step[supported_by[current][0]])!=1:
        dropped_supports = set() | branch
        for i ,(supports, _, tmp_branch, _) in sorted(cache.items(), key=lambda x:x[0]):
            if supports.issubset(dropped_supports):
                dropped_supports |= tmp_branch
        current_count = len(dropped_supports) -1
        if len(branch)>1:
            dropping_block_not_in_branch = current_count-(len(branch)-1)
            score_from_branch = len(branch)*(len(branch)-1)//2
            current_count = score_from_branch + dropping_block_not_in_branch*len(branch)
        
        cache[current] = set(supported_by[current]), current_visited, branch, current_count
        return set(), current_visited
    return branch, current_visited

def solution(text):
    first_coords, second_coords, axis_of_change, extents = parse_input(text)
    grid_shape = np.max(second_coords, axis=0)+1
    height = np.zeros(grid_shape[:2], dtype=int)
    block_id = -np.ones(grid_shape, dtype=int)
    supported_by = [[] for _ in range(len(first_coords))]
    only_support = np.zeros(len(first_coords), dtype=bool)
    for i, (first_coord, second_coord, axis, extent) in enumerate(zip(first_coords, second_coords, axis_of_change, extents)):
        x1,y1 = first_coord[:2]
        axis = axis[0]
        extent = extent[0]
        if axis == 2:
            new_height = height[x1, y1]+1
            height[x1, y1]+=extent+1
            assert new_height==1 or block_id[x1, y1, new_height-1]!=-1
            assert np.all(block_id[x1, y1, new_height:new_height+extent+1] == -1)
            block_id[x1, y1, new_height:new_height+extent+1] = i
            support = block_id[x1, y1, new_height-1]
            if support > -1:
                supported_by[i] = [support]
                only_support[support] = True
        else:
            x2,y2 = (x1+extent*(axis==0)) + 1, (y1+extent*(axis==1)) + 1
            new_height = np.max(height[x1:x2,y1:y2]) +1
            height[x1:x2,y1:y2] = new_height
            assert np.all(block_id[x1:x2,y1:y2, new_height] == -1)
            block_id[x1:x2,y1:y2, new_height] = i
            support = np.unique(block_id[x1:x2,y1:y2, new_height-1])
            support = list(support[support>-1])
            supported_by[i] = support
            if len(support) == 1:
                only_support[support[0]] = True
    
    base_blocks = [i for i, s in enumerate(supported_by) if len(s)==0]
    supports_one_step = [[] for _ in range(len(first_coords))]
    for i, supported in enumerate(supported_by):
        for s in supported:
            supports_one_step[s].append(i)

    base_supports = {i: find_all_supported_by_base(i, supports_one_step) for i in base_blocks}
    pruned = {}
    for i, supports in base_supports.items():
        base = supports
        for j, supports_2 in base_supports.items():
            if i==j:
                continue
            base = base - supports_2
        pruned[i] = supports
    assert base_supports == pruned, "All towers are connected to a single base"
    
    cache = [[] for _ in range(len(first_coords))]
    visited = set()
    count_per_tree = [count_from_top(base, supports_one_step, supported_by, cache, visited) for base in base_blocks]
    
    cache2 = {}
    branch = {}
    count_per_tree = [count_from_top_2(base, supports_one_step, supported_by, cache2, branch) for base in base_blocks]
    return np.sum(~only_support), sum([c for _, c, _ in cache]), sum(c for _, _, _, c in cache2.values())

def test_example():
    test_text = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
    print(solution(test_text))
    

def get_answer(input_text):
    print(solution(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)