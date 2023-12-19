from copy import deepcopy
from operator import gt, lt

import numpy as np

METRIC_TO_INDEX = {
    "x": 0,
    "m": 1,
    "a": 2,
    "s": 3
}
MINIMUM_VALUE = 1
MAXIMUM_VALUE = 4000

def parse_input(text):
    instructions, items_txt = text.split("\n\n")
    instructions = dict(map(parse_instruction, instructions.split("\n")))
    items = np.array(list(map(parse_items, items_txt.split("\n"))))
    return instructions, items

def parse_instruction(text):
    key, conditions = text.split("{")
    *conditions, default = conditions[:-1].split(",")
    mappings = list(map(parse_condition, conditions))
    return key, (mappings, default)
    
def parse_condition(text):
    cond, mapping = text.split(":")
    if "<" in cond:
        metric, value = cond.split("<")
        op_char = "<"
        op = lt
    elif ">" in cond:
        metric, value = cond.split(">")
        op_char = ">"
        op = gt
    else:
        raise ValueError()
    return {"metric": metric, "op_char": op_char, "op": op, "value": int(value), "mapping": mapping}

def parse_items(text):
    return [int(t.split("=")[-1]) for t in text[1:-1].split(",")]

def traverse_tree(intructions, item_range, key):
    if key in "A":
        combinations = 1
        for lower, upper in item_range.values():
            combinations *= (upper-(lower+1))
        return combinations
    elif key == "R":
        return 0
    conditions, default = intructions[key]
    combinations = 0
    for condition in conditions:
        op_char = condition["op_char"]
        metric = condition["metric"]
        boundry = condition["value"]
        
        current_item_range = deepcopy(item_range)
        current_lower, current_upper = current_item_range[metric]
        other_lower, other_upper = item_range[metric]
        
        if op_char=="<":
            current_item_range[metric][1] = min(boundry, current_upper) 
            item_range[metric][0] = max(boundry-1, other_lower)
        else:
            current_item_range[metric][0] = max(boundry, current_lower)
            item_range[metric][1] = min(boundry+1, other_upper)
        if current_item_range[metric][0] < current_item_range[metric][1]:
            combinations += traverse_tree(intructions, current_item_range, condition["mapping"])
        if item_range[metric][0] >= item_range[metric][1]:
            return combinations
    
    if item_range[metric][0] < item_range[metric][1]:
        combinations+=traverse_tree(intructions, deepcopy(item_range), default)
    return combinations

def follow_instuctions(instructions, items, key):
    n_items = len(items)
    if key == "R":
        return np.zeros(n_items, dtype=int)
    if key == "A":
        return np.ones(n_items, dtype=int)
    conditions, default = instructions[key]
    
    output = np.ones(n_items, dtype=int) * -1
    full_filled = np.ones(n_items, dtype=bool)
    for condition in conditions:
        metric_idx = METRIC_TO_INDEX[condition["metric"]]
        op = condition["op"]
        boundry = condition["value"]
        mask = op(items[:,metric_idx], boundry)
        cond_full_filled = full_filled & mask
        output[cond_full_filled] = follow_instuctions(instructions, items[cond_full_filled], condition["mapping"])
        full_filled = full_filled & (~mask)
    output[full_filled] = follow_instuctions(instructions, items[full_filled], default)
    return output

def solution(text):
    instructions, items = parse_input(text)
    current="in"
    accepted = follow_instuctions(instructions, items, current).astype(bool)
    accepted_value = items[accepted].sum()
    condition = {"x": [MINIMUM_VALUE-1, MAXIMUM_VALUE+1], "m": [MINIMUM_VALUE-1, MAXIMUM_VALUE+1], "a": [MINIMUM_VALUE-1, MAXIMUM_VALUE+1], "s": [MINIMUM_VALUE-1, MAXIMUM_VALUE+1]}
    combinations = traverse_tree(instructions, condition, current)
    return accepted_value, combinations


def test_example():
    test_text = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
    print(solution(test_text))
    

def get_answer(input_text):
    print(solution(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)