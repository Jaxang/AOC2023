USED_CUBES = {"blue":14, "red":12, "green":13}

def test_example():
    test_text = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    test_lines = test_text.split("\n")
    valid_ids = valid_game_ids(test_lines)
    assert sum(valid_ids) == 8
    minimum_powers = get_minimum_powers(test_lines)
    assert sum(minimum_powers) == 2286

def get_answer(text):
        lines = text.split("\n")
        valid_ids = valid_game_ids(lines)
        print(sum(valid_ids))
        minimum_powers = get_minimum_powers(lines)
        print(sum(minimum_powers))

def valid_game_ids(lines):
    mapping = map(get_game_max_outcome_mapping, lines)
    return [game_id for game_id, max_outcomes in mapping if valid_game(max_outcomes)]

def valid_game(outcome):
    for key in outcome:
        if outcome[key] > USED_CUBES[key]:
            return False
    return True

def get_minimum_powers(lines):
    mapping = map(get_game_max_outcome_mapping, lines)
    return [max_outcomes["blue"]*max_outcomes["red"]*max_outcomes["green"] for _, max_outcomes in mapping]


def get_game_max_outcome_mapping(line):
    game_string, outcomes = line.split(":")
    game_id = int(game_string.lstrip("Game "))
    max_outcomes = find_max_outcomes(outcomes.split(";"))
    return game_id, max_outcomes

def find_max_outcomes(outcomes):
    max_outcomes = {"blue": 0, "red": 0, "green": 0}
    for outcome in outcomes:
        outcome_values = parse_outcome(outcome)
        for key, value in outcome_values.items():
            max_outcomes[key] = max(value, max_outcomes[key])
    return max_outcomes

def parse_outcome(outcome):
    entries = outcome.split(",")
    output={}
    for entry in entries:
        key = "blue" if "blue" in entry else "red" if "red" in entry else "green"
        output[key] = int(entry.strip(key))
    return output

        
def main(input_text):
    test_example()
    get_answer(input_text)
