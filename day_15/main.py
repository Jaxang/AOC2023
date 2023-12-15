def parse_input(text):
    return text.split(",")

def hash_instuction(instuct):
    out = 0
    for c in instuct:
        out = (out + ord(c)) % 256
        out = (out*17) % 256
    return out

def process_instruction(intruction, boxes):
    if "=" in intruction:
        add_lens(intruction, boxes)
    else:
        remove_lens(intruction, boxes)

def add_lens(intruction, boxes):
    label, lens = intruction.split("=")
    lens = int(lens)
    box_idx = hash_instuction(label)
    label_list, lens_list = boxes[box_idx]
    if label in label_list:
        label_idx = label_list.index(label)
        lens_list[label_idx] = lens
    else:
        label_list.append(label)
        lens_list.append(lens)
    

def remove_lens(intruction, boxes):
    label = intruction.rstrip("-")
    box_idx = hash_instuction(label)
    label_list, lens_list = boxes[box_idx]
    if label in label_list:
        label_idx = label_list.index(label)
        label_list.pop(label_idx)
        lens_list.pop(label_idx)
        
def focusing_power(boxes):
    power = 0
    for i, (_, focal_lengths) in enumerate(boxes, start=1):
        for j, focal_length in enumerate(focal_lengths,start =1):
            power+=(i*j*focal_length)
    return power

def solution(text):
    instuctions = parse_input(text)
    instuction_hash = sum(map(hash_instuction, instuctions))
    boxes = [(list(),list()) for _ in range(256)]
    for intruction in instuctions:
        process_instruction(intruction, boxes)
    power = focusing_power(boxes)
    return instuction_hash, power
    
    

def test_example():
    test_text = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    print(solution(test_text))
    

def get_answer(input_text):
    print(solution(input_text))


def main(input_text):
    test_example()
    get_answer(input_text)