import re
import time


class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def distance(self, other_loc):
        row_dif = abs(self.row - other_loc.row)
        col_dif = abs(self.col - other_loc.col)
        return row_dif + col_dif


def read_file(input_doc, expansion_mod=2):
    locations = []
    cols_filled = []
    original_col_size = None
    f = open(input_doc, "r")
    row = 0
    for line in f:
        if original_col_size is None:
            original_col_size = len(line) - 1
        index = None
        running_index = 0
        matcher = re.search("#", line)
        while matcher is not None:
            index = matcher.start()
            running_index += index
            locations.append(Location(row, running_index))
            if running_index not in cols_filled:
                cols_filled.append(running_index)
            running_index += 1
            matcher = re.search("#", line[running_index:])
        if index is None:
            row += expansion_mod - 1
        row += 1
    locations = sorted(locations, key=lambda loc: loc.col)
    cols_filled.sort()
    next_full_col = cols_filled.pop(0)
    cols_to_add = 0
    locations_index = 0
    for original_col in range(original_col_size):
        if original_col == next_full_col:
            if len(cols_filled) > 0:
                next_full_col = cols_filled.pop(0)
        else:
            cols_to_add += expansion_mod - 1
        while locations_index < len(locations):
            if locations[locations_index].col == original_col:
                locations[locations_index].col += cols_to_add
                locations_index += 1
            else:
                break
        if locations_index >= len(locations):
            break
    f.close()
    return locations


def get_sum_distances(locations):
    sum = 0
    for x in range(len(locations) - 1):
        for y in range(x + 1, len(locations)):
           sum += locations[x].distance(locations[y])
    return sum


def main(input_doc):
    start_time = time.time()
    locations = read_file(input_doc)
    print("---------------------")
    print("Day 11 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(get_sum_distances(locations)))        # 10033566
    locations = read_file(input_doc, 1000000)
    print("Solution (Part 2): " + str(get_sum_distances(locations)))        # 560822911938
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
