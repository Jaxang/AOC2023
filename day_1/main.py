import re

NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
NUMBERS_MAP = {n: str(i) for i, n in enumerate(NUMBERS, start=1)}
REVERSE_NUMBERS = list(map(lambda x:x[::-1], NUMBERS))
REVERSE_NUMBERS_MAP = {n: str(i) for i, n in enumerate(REVERSE_NUMBERS, start=1)}
FIRST_DIGIT_PATTERN=re.compile(r"^\D*\d")
LAST_DIGIT_PATTERN=re.compile(r"\d\D*$")
FIRST_DIGIT_PATTERN_COMPLEX=re.compile(r"("+r")|(".join([r"\d"]+NUMBERS) + ")")
LAST_DIGIT_PATTERN_COMPLEX=re.compile(r"("+r")|(".join([r"\d"]+REVERSE_NUMBERS) + ")")

def get_calibration_sum(text, star_one=True):
    if star_one:
        return sum(map(get_calibration_number, text.split("\n")))
    return sum(map(get_complex_calibration_matches, text.split("\n")))

def get_calibration_number(line):
    return int(get_first_digit(line) + get_last_digit(line))

def get_first_digit(line):
    return FIRST_DIGIT_PATTERN.search(line).group(0)[-1]

def get_last_digit(line):
    return LAST_DIGIT_PATTERN.search(line).group(0)[0]

def get_complex_calibration_matches(line):
    first = FIRST_DIGIT_PATTERN_COMPLEX.search(line).group(0)
    first_digit = NUMBERS_MAP.get(first, first)
    last = LAST_DIGIT_PATTERN_COMPLEX.search(line[::-1]).group(0)
    last_digit = REVERSE_NUMBERS_MAP.get(last, last)
    return int(first_digit+last_digit)

def test_example(star_one=True):
    test_text = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
    test_lines = test_text.split("\n")
    test_first_digits = list(map(get_first_digit, test_lines))
    test_last_digits = list(map(get_last_digit, test_lines))
    assert test_first_digits == ["1", "3", "1", "7"]
    assert test_last_digits == ["2", "8", "5", "7"]
    assert get_calibration_sum(test_text, star_one) == 142

def test_example_2():
    test_text = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    test_lines = test_text.split("\n")
    test_digits = list(map(get_complex_calibration_matches, test_lines))
    assert test_digits == [29, 83, 13, 24, 42, 14, 76]
    assert get_calibration_sum(test_text, star_one=False) == 281

def get_answer(text, star_one=True):
    print(get_calibration_sum(text, star_one=star_one))
    
def main(input_text):
    test_example()
    test_example(star_one=False)
    test_example_2()
    get_answer(input_text, star_one=True)
    get_answer(input_text, star_one=False)
