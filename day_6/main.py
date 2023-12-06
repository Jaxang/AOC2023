import math


def solution(text, solution=1):
    prod = 1
    margins = map(get_number_of_solutions, *parse_input(text, solution=solution))
    for margin in margins:
        prod *= margin
    return prod

def parse_input(text, solution=1):
    return parse_input_1(text) if solution==1 else parse_input_2(text)

def parse_input_1(text):
    times, distance = text.split("\n")
    times = list(map(int, times.split(":")[1].strip().split()))
    distance = list(map(int, distance.split(":")[1].strip().split()))
    return times, distance

def parse_input_2(text):
    times, distance = text.split("\n")
    times = int("".join(times.split(":")[1].strip().split()))
    distance = int("".join(distance.split(":")[1].strip().split()))
    return [times], [distance]

def get_number_of_solutions(time, distance):
    # x*(T-x) = distance+1
    # x^2 - Tx + distance = 0
    # (x-T/2)^2 = T^2/4 - distance
    # x = T/2 +- sqrt(T^2/4 - distance)
    # optimal solution is time/2
    min_required_distance = distance
    x_opt = time/2
    if math.ceil(x_opt)*math.floor(x_opt) < min_required_distance:
        return 0
    x_plus = time/2 + math.sqrt(time**2/4 - (min_required_distance+1))
    x_plus_discrete = math.floor(x_plus)
    margin = 2*math.ceil(x_plus_discrete-x_opt) + (1-time%2)
    return margin



def test_example():
    test_text = """Time:      7  15   30
Distance:  9  40  200"""
    print(solution(test_text, 1))
    print(solution(test_text, 2))
    

def get_answer(input_text):
    print(solution(input_text, 1))
    print(solution(input_text, 2))


def main(input_text):
    test_example()
    get_answer(input_text)