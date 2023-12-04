import re


def test_example(star_one=True):
    test_text = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    row_length = test_text.find("\n")+1
    flatten_text = test_text.replace("\n", ".")
    valid_idxs = {i+offset_x+offset_y for i, s in enumerate(flatten_text) if s not in r"0123456789." for offset_x in [-1, 0, 1] for offset_y in [-row_length, 0, row_length]}
    valid_parts = [int(number_match.group(0)) for number_match in re.finditer("\d+", flatten_text) if any(i in valid_idxs for i in range(*number_match.span()))]
    print(sum(valid_parts))
    gear_position = {(i//row_length, i%row_length) for i, s in enumerate(flatten_text) if s == "*"}
    print(sum([matches[0]*matches[1] for row, col in gear_position if len(matches:=[int(number_match.group(0)) for number_match in re.finditer("\d+", flatten_text[max(0, (row-1))*row_length:(row+2)*row_length]) if any(i+max(0, (row-1))*row_length in [row*row_length+col+offset_x+offset_y for offset_x in [-1, 0, 1] for offset_y in [-row_length, 0, row_length]] for i in range(*number_match.span()))])==2]))
    

def get_answer(star_one=True):
    with open("day_3/input.txt") as f:
        text = f.read()
        row_length = text.find("\n")+1
        flatten_text = text.replace("\n", ".")
        valid_idxs = {i+offset_x+offset_y for i, s in enumerate(flatten_text) if s not in r"0123456789." for offset_x in [-1, 0, 1] for offset_y in [-row_length, 0, row_length]}
        valid_parts = [int(number_match.group(0)) for number_match in re.finditer("\d+", flatten_text) if any(i in valid_idxs for i in range(*number_match.span()))]
        print(sum(valid_parts))
        gear_position = {(i//row_length, i%row_length) for i, s in enumerate(flatten_text) if s == "*"}
        print(sum([matches[0]*matches[1] for row, col in gear_position if len(matches:=[int(number_match.group(0)) for number_match in re.finditer("\d+", flatten_text[max(0, (row-1))*row_length:(row+2)*row_length]) if any(i+max(0, (row-1))*row_length in [row*row_length+col+offset_x+offset_y for offset_x in [-1, 0, 1] for offset_y in [-row_length, 0, row_length]] for i in range(*number_match.span()))])==2]))

if __name__ == "__main__":
    test_example()
    get_answer(star_one=True)