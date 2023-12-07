from collections import defaultdict
from copy import deepcopy
from functools import partial

import numpy as np

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARDS_VALUE_MAPPING = dict(zip(reversed(CARDS), range(len(CARDS))))
CARDS_VALUE_MAPPING_2 = deepcopy(CARDS_VALUE_MAPPING)
CARDS_VALUE_MAPPING_2["J"]=-1
HANDS = [(5,), (1, 4), (2, 3), (1,1,3), (1, 2, 2), (1, 1, 1, 2), (1, 1, 1, 1, 1)]
HANDS_VALUE_MAPPING = dict(zip(reversed(HANDS), range(len(HANDS))))

def parse_input(text, solution=1):
    lines = [i.split(" ") for i in text.split("\n")]
    card_sets = [parse_cards(cards_text, solution) for cards_text, _ in lines]
    bids = [int(bid_text) for _, bid_text in lines]
    return card_sets, bids
    
def parse_cards(cards_text, solution=1):
    return parse_cards_1(cards_text) if solution==1 else parse_cards_2(cards_text)

def parse_cards_1(cards_text):
    return tuple(map(lambda x: CARDS_VALUE_MAPPING[x], cards_text))

def parse_cards_2(cards_text):
    return tuple(map(lambda x: CARDS_VALUE_MAPPING_2[x], cards_text))

def get_hand_value(card_set, solution=1):
    return get_hand_value_1(card_set) if solution==1 else get_hand_value_2(card_set)

def get_hand_value_1(card_set):
    counter = defaultdict(lambda: 0)
    for card in card_set:
        counter[card] += 1
    hand = tuple(sorted((counter.values())))
    value = HANDS_VALUE_MAPPING[hand]
    return value

def get_hand_value_2(card_set):
    counter = defaultdict(lambda: 0)
    for card in card_set:
        counter[card] += 1
    jokers=counter[-1]
    if jokers!=5:
        del counter[-1]
        if jokers > 0:
            best_value, best_key = sorted((v,k) for k, v in counter.items())[-1]
            counter[best_key]=best_value+jokers
        
    hand = tuple(sorted((counter.values())))
    value = HANDS_VALUE_MAPPING[hand]
    return value

def solution(text, solution=1):
    card_sets, bids = parse_input(text, solution=solution)
    hand_values = list(map(partial(get_hand_value, solution=solution), card_sets))
    score = sorted(list(zip(hand_values, card_sets, bids)))
    return sum(rank*bid for rank, (_, _, bid) in enumerate(score, start=1))

def test_example():
    test_text = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    print(solution(test_text, solution=1))
    print(solution(test_text, solution=2))
    
    

def get_answer(input_text):
    print(solution(input_text, solution=1))
    print(solution(input_text, solution=2))


def main(input_text):
    test_example()
    get_answer(input_text)