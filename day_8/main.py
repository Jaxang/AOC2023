from functools import partial
from queue import PriorityQueue


def parse_input(text):
    directions, nodes = text.split("\n\n")
    directions = directions.strip()
    nodes = dict(parse_node(node) for node in nodes.split("\n") if node)
    return directions, nodes

def parse_node(node):
    name, children = node.split(" = (")
    name = name.strip()
    l_child, r_child = children[:-1].split(", ")
    return name, {"L": l_child, "R": r_child}

def find_endpoint(directions, nodes, position="AAA", end_positions={"ZZZ"}, total_steps=0, chache=None):
    initial_state = (position, total_steps%len(directions))
    initial_steps = total_steps
    if chache is not None and initial_state in chache:
        chache_position, step_diff = chache[initial_state]
        return total_steps+step_diff, chache_position
    
    first_step =True
    while(position not in end_positions or first_step):
        first_step = False
        index = total_steps%len(directions)
        direction = directions[index]
        position = nodes[position][direction]
        total_steps += 1
        
    if chache is not None:
        chache[initial_state] = position, total_steps-initial_steps
        
    return total_steps, position

def solution_1(text):
    directions, nodes = parse_input(text)
    total_steps, _ = find_endpoint(directions, nodes)
    return total_steps

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_gcd(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result = gcd(result, num)
    return result

def solution_2(text):
    directions, nodes = parse_input(text)
    start_nodes = [node for node in nodes if node[-1]=="A"]
    end_nodes = set([node for node in nodes if node[-1]=="Z"])
    chache = {}
    _step = partial(find_endpoint, directions=directions, nodes=nodes, end_positions=end_nodes, chache=chache)
    
    queue = PriorityQueue()
    highest_steps = 0
    node_steps = []
    for s in start_nodes:
        steps, positon = _step(position=s)
        highest_steps = max(steps, highest_steps)
        queue.put((steps, positon))
        node_steps.append(steps)
    if all([node%len(directions)==0 for node in node_steps]):
        print("WTF....")
        divider = find_gcd(node_steps)
        prod = 1
        for step in node_steps:
            prod *= step//divider
        return prod*divider

    lowest_steps, position = queue.get()
    while (lowest_steps<highest_steps):
        steps, position =_step(position=position, total_steps=lowest_steps)
        queue.put((steps, position))
        highest_steps = max(steps, highest_steps)
        lowest_steps, position = queue.get()
    return lowest_steps
        

def test_example():
    test_text_1A = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    print(solution_1(test_text_1A))
    test_text_1B = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    print(solution_1(test_text_1B))
    test_text_2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    print(solution_2(test_text_2))

def get_answer(input_text):
    print(solution_1(input_text))
    print(solution_2(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)