# FIFO queue to handle communications
# Flip-Flop class
from collections import defaultdict, deque

import numpy as np


def nested_defaultdict():
    return defaultdict(nested_defaultdict)

class BaseComponent:
    def __init__(self, name):
        self.name = name
        self._done = False

    def __call__(self, input_name, pulse):
        self._done = self._done or (pulse==0)
        return self.name, None
    
    @property
    def done(self):
        return self._done

    @property
    def state(self):
        return 0


class FlipFlop(BaseComponent):
    def __init__(self, name):
        super().__init__(name)
        self._state = 0
    
    def __call__(self, input_name, pulse):
        super().__call__(input_name, pulse)
        if pulse == 1:
            return None
        self._state = 1-self._state
        return self.name, self._state
    
    @property
    def state(self):
        return self._state
    
    def reset(self):
        self._state = 0
                        
# Conjunction class
class Conjunction(BaseComponent):
    def __init__(self, name):
        super().__init__(name)
        self.stored_pulse = {}
    
    def __call__(self, input_name, pulse):
        super().__call__(input_name, pulse)
        self.stored_pulse[input_name] = pulse
        return self.name, self._pulse()
    
    @property
    def state(self):
        _state = 0
        for i, v in enumerate(self.stored_pulse.values()):
            _state += v*(2**i)
        return _state
    
    def add_input_node(self, input_name):
        self.stored_pulse[input_name] = 0
    
    def reset(self):
        for key in self.stored_pulse:
            self.stored_pulse[key] = 0
        
    def _pulse(self):
        return 1 - all(v==1 for v in self.stored_pulse.values())

class Broadcaster(BaseComponent):
    def __call__(self, input_name, pulse):
        super().__call__(input_name, pulse)
        return self.name, pulse

def parse_input(text):
    input_to_outputs = {}
    output_to_inputs = defaultdict(list)
    for line in text.split("\n"):
        node_name, node, targets = parse_line(line)
        input_to_outputs[node_name] = (node, targets)
        for target in targets:
            output_to_inputs[target].append(node_name)
    if "rx" in output_to_inputs:
        input_to_outputs["rx"] = (BaseComponent("rx"), [])
    for node_name, inputs in output_to_inputs.items():
        if node_name not in input_to_outputs:
            continue
        node, _ = input_to_outputs[node_name]
        if isinstance(node, Conjunction):
            for i in inputs:
                node.add_input_node(i)
    return input_to_outputs

def parse_line(line):
    node_name, targets = line.split(" -> ")
    if node_name[0] == "%":
        node_name = node_name[1:]
        node = FlipFlop(node_name)
    elif node_name[0] == "&":
        node_name = node_name[1:]
        node = Conjunction(node_name)
    else:
        node = Broadcaster(node_name)
    
    targets = targets.split(", ")
    return node_name, node, targets

def component_states(input_to_outputs):
    states = tuple([node.state for node, _ in input_to_outputs.values()])
    return states

def reset(input_to_outputs):
    for node, _ in input_to_outputs.values():
        node.reset()

def get_subgraph(input_to_outputs, input_node_name, end_node_name):
    subgraph = {input_node_name: input_to_outputs[input_node_name]}
    internal_nodes = []
    tmp_node_name = input_node_name
    while len(internal_nodes) < 11:
        targets = [t for t in input_to_outputs[tmp_node_name][1] if t!=end_node_name]
        assert len(targets) == 1
        target = targets[0]
        internal_nodes.append(target)
        subgraph[target] = input_to_outputs[target]
        tmp_node_name = target
    subgraph[end_node_name] = input_to_outputs[input_node_name]
    return subgraph

def analyse_subgraph(subgraph, input_node_name, end_node_name):
    reset(subgraph)
    press=0
    start_state = {}
    current_state=component_states(subgraph)
    outputs = nested_defaultdict()
    while current_state not in start_state:
        start_state[component_states(subgraph)] = press
        press += 1
        tick = 0
        queue = deque()
        queue.append(("broadcaster", 0, input_node_name, tick))
        while len(queue)!=0:
            node_name, pulse, target, tick = queue.popleft()
            if target not in subgraph:
                continue
            if node_name==end_node_name:
                outputs[press][tick]=1
                
            node, new_targets = subgraph[target]
            output = node(node_name, pulse)
            if output is None:
                continue
            _, pulse = output
            
            for new_target in new_targets:
                queue.append((target, pulse, new_target, tick+1))
        current_state = component_states(subgraph)
    reset(subgraph)
    return start_state, outputs
        

def press_button(input_to_outputs, pulse=0):
    start_state = component_states(input_to_outputs)
    pulses = [0, 0]
    input_name = "buttom"
    queue = deque()
    queue.append((input_name, pulse, "broadcaster"))
    while len(queue)!=0:
        node_name, pulse, target = queue.popleft()
        pulses[pulse] += 1
        
        if target not in input_to_outputs:
            continue
        node, new_targets = input_to_outputs[target]
        
        output = node(node_name, pulse)
        if output is None:
            continue
        _, pulse = output
        
        for new_target in new_targets:
            queue.append((target, pulse, new_target))
    end_state = component_states(input_to_outputs)
    done = input_to_outputs["rx"][0].done if "rx" in input_to_outputs else False
    return start_state, end_state, pulses, done

def repeated_presses(input_to_outputs, presses=1000):
    chache = {}
    parent = {}
    total_pulses = np.array([0, 0])
    for i in range(1, presses+1):
        start_state, end_state, pulses, done = press_button(input_to_outputs)
        if done:
            return i
        chache[start_state] = end_state, pulses
        parent[end_state] = start_state
        total_pulses += pulses
        if end_state in chache:
            break
        if i%10000 == 0:
            print(i)

    if i == presses:
        return total_pulses[0]*total_pulses[1]

    steps_left = presses -i
    pulses_in_cycle = np.array(pulses)
    steps_in_cycle = 1
    tmp_state = start_state
    while (tmp_state!=end_state):
        tmp_state = parent[tmp_state]
        _, pulses = chache[tmp_state]
        pulses_in_cycle += pulses
        steps_in_cycle += 1

    cycles = steps_left // steps_in_cycle
    total_pulses += cycles * pulses_in_cycle
    for i in range(steps_left-cycles*steps_in_cycle):
        end_state, pulses = chache[end_state]
        total_pulses += pulses
    return total_pulses[0]*total_pulses[1]
    

def solution(text, presses=1000):
    input_to_outputs = parse_input(text)
    input_nodes = ["hh", "lr", "bp", "lf"]
    end_nodes = ["qs", "mj", "cs", "rd"]
    subgraph_data = {}
    for input_node, end_node in zip(input_nodes, end_nodes):
        subgraph = get_subgraph(input_to_outputs, input_node, end_node)
        start_state, outputs = analyse_subgraph(subgraph, input_node, end_node)
        subgraph_data[(input_node, end_node)] = start_state, outputs
    output = repeated_presses(input_to_outputs, presses)
    return output

def test_example():
    test_text = r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
    test_text_1 = r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    #print(solution(test_text), (8000, 4000, 32000000))
    #print(solution(test_text_1), (4250, 4000, 32000000))
    

def get_answer(input_text):
    #print(solution(input_text))
    print(solution(input_text, 1000000000000000000000))


def main(input_text):
    test_example()
    get_answer(input_text)