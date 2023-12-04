import re


def solution(text):
    lines = text.split("\n")
    winning_numbers = [{int(number) for number in line.split(":")[1].split("|")[0].split(" ") if number} for line in lines]
    your_numbers = [[int(number) for number in line.split(":")[1].split("|")[1].split(" ") if number] for line in lines]
    matches = [[number for number in game_numbers if number in winning_numbers[i]] for i, game_numbers in enumerate(your_numbers)]
    n_matches = [len(game_matches) for game_matches in matches]
    max_matches = len(winning_numbers[0])
    points_array=[0]+[2**i for i in range(max_matches)]
    points = [points_array[point_idx] for point_idx in n_matches]
    print(sum(points))
    n_matches_reversed = reversed(n_matches)
    output = []
    for i, n in enumerate(n_matches_reversed):
        output.append(1 + sum(m for m in output[i-n:i]))
    print(output, sum(output))

def test_example(star_one=True):
    test_text = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    solution(test_text)
    

def get_answer(input_text):
    solution(input_text)


def main(input_text):
    test_example()
    get_answer(input_text)