import re


def parse_input(text, solution=1):
    seeds, *maps = text.split("\n\n")
    seeds = parse_seeds(seeds, solution=solution)
    maps = dict(parse_map(m) for m in maps)
    return seeds, maps

def parse_seeds(seeds, solution=1):
    return parse_seeds_1(seeds) if solution==1 else parse_seeds_2(seeds)


def parse_seeds_1(seeds):
    return list(map(int, seeds.split(":")[1].strip().split(" ")))


def parse_seeds_2(seeds):
    values = list(map(int, seeds.split(":")[1].strip().split(" ")))
    value_pairs = list(zip(values[::2], values[1::2]))
    return value_pairs

def parse_map(map_text):
    mapping, *ranges = map_text.strip().split("\n")
    src, dest = mapping[:-len(" map:")].split("-to-")
    mappings = sorted([
        parse_ranges(ranges_text)
        for ranges_text in ranges
    ], key=lambda x: x[0])
    return src, {"dest": dest, "mappings": mappings}

def parse_ranges(range_text):
    dest_range, src_range, range_length = map(int, range_text.split(" "))
    mapping_offset = dest_range-src_range
    return src_range, range_length, mapping_offset

def apply_mapping(src_values, mappings):
    dest_values = []
    for src_value in src_values:
        dest_value = src_value
        for src_range, range_length, mapping_offset in mappings:
            if src_range <= src_value < (src_range+range_length):
                dest_value = src_value + mapping_offset
                break
        dest_values.append(dest_value)
    return dest_values

def apply_mapping(src_values, mappings, solution=1):
    if solution==1:
        return apply_mapping_1(src_values, mappings)
    else:
        return apply_mapping_2(src_values, mappings)


def apply_mapping_1(src_values, mappings):
    dest_values = []
    for src_value in src_values:
        dest_value = src_value
        for src_range, range_length, mapping_offset in mappings:
            if src_range <= src_value < (src_range+range_length):
                dest_value = src_value + mapping_offset
                break
        dest_values.append(dest_value)
    return dest_values

def apply_mapping_2(src_pairs, mappings):
    dest_pairs = []
    for src_start, src_length in src_pairs:
        src_end = src_start + src_length
        unmatched_start, unmatched_end = src_start, src_end
        for mapping_start, mapping_length, mapping_offset in mappings:
            mapping_end = mapping_start + mapping_length
            
            overlap = unmatched_start < mapping_end and mapping_start < unmatched_end
            if overlap:
                if unmatched_start < mapping_start:
                    # Since mapping is sorted region has no mapping
                    dest_pairs.append((src_start, mapping_start-src_start))
                
                overlap_start = max(unmatched_start, mapping_start)
                overlap_end = min(unmatched_end, mapping_end)
                
                dest_pairs.append((overlap_start+mapping_offset, overlap_end-overlap_start))
                
                unmatched_start=overlap_end
                if unmatched_start==unmatched_end:
                    break
        else: # Last part newer matched (No break)
            dest_pairs.append((unmatched_start, unmatched_end-unmatched_start))
    return dest_pairs

def solution(text, solution=1):
    seeds, mappings = parse_input(text, solution=solution)
    source, source_values = "seed", seeds
    while (source != "location"):
        mapping = mappings[source]
        source_values = apply_mapping(source_values, mapping["mappings"], solution=solution)
        source = mapping["dest"]
    return min(source_values)

def test_example():
    test_text = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
    print(solution(test_text, solution=1))
    print(solution(test_text, solution=2))
    

def get_answer(input_text):
    print(solution(input_text, solution=1))
    print(solution(input_text, solution=2))


def main(input_text):
    test_example()
    get_answer(input_text)