import copy
import re
import time


class Locs:
    def __init__(self):
        self.loc_map = {}
        self.num_rows = 0
        self.num_cols = 0

    def add_line(self, a_line, row_num):
        for i in range(len(a_line)):
            if a_line[i] in ["#", ".", "O"]:
                self.loc_map[get_pos(row_num, i)] = a_line[i]

    def roll(self, dir):
        index = 0
        first_pos = self.first_pos(index, dir)

        while first_pos is not None:
            pos = first_pos
            roll_to_key = first_pos
            next_pos = self.get_next_pos(first_pos, dir)
            while pos is not None:
                current_char = self.loc_map[pos]
                if current_char == "#":
                    roll_to_key = next_pos
                elif current_char == "O":
                    if pos != roll_to_key:
                        self.loc_map[roll_to_key] = "O"
                        self.loc_map[pos] = "."
                        roll_to_key = self.get_next_pos(roll_to_key, dir)
                    else:
                        roll_to_key = next_pos
                pos = next_pos
                if next_pos is not None:
                    next_pos = self.get_next_pos(next_pos, dir)
            index += 1
            first_pos = self.first_pos(index, dir)

    def cycle(self, num_cycles):
        while num_cycles > 0:
            self.roll("N")
            self.roll("W")
            self.roll("S")
            self.roll("E")
            num_cycles -= 1
        return sum_all_weights(self)

    def first_pos(self, index, dir):
        if dir == "N" and index < self.num_cols:
            return get_pos(0, index)
        elif dir == "S" and index < self.num_cols:
            return get_pos(self.num_rows - 1, index)
        elif dir == "E" and index < self.num_rows:
            return get_pos(index, self.num_cols - 1)
        elif dir == "W" and index < self.num_rows:
            return get_pos(index, 0)
        else:
            return None

    def get_next_pos(self, key, dir):
        row, col = get_row_col(key)
        if dir == "N" and row + 1 < self.num_rows:
            return get_pos(row+1, col)
        elif dir == "S" and row - 1 >= 0:
            return get_pos(row-1, col)
        elif dir == "E" and col - 1 >= 0:
            return get_pos(row, col-1)
        elif dir == "W" and col + 1 < self.num_cols:
            return get_pos(row, col+1)
        else:
            return None

    def get_weight(self, key):
        row, col = get_row_col(key)
        return self.num_rows - row


def get_pos(row, col):
    return str(row) + "," + str(col)


def get_row_col(pos):
    ret_val = re.split(",", pos)
    return int(ret_val[0]), int(ret_val[1])


def read_file(input_doc):
    loc_map = Locs()
    row = 0
    f = open(input_doc, "r")
    first_line = f.readline()
    loc_map.num_cols = len(first_line) - 1
    loc_map.add_line(first_line, row)
    for line in f:
        row += 1
        loc_map.add_line(line, row)
    f.close()
    loc_map.num_rows = row + 1

    return loc_map


def sum_all_weights(loc_map):
    sum = 0
    for key in loc_map.loc_map:
        if loc_map.loc_map[key] == "O":
            weight = loc_map.get_weight(key)
            sum += weight
    return sum


def run_cycles(loc_map, run_count):
    weight_history = []
    pattern_size = None
    run = 0
    while run < run_count:
        latest_weight = loc_map.cycle(1)
        weight_history.append(latest_weight)
        if len(weight_history) > 20:
            pattern_size = find_pattern_size(weight_history)
        if pattern_size is not None:
            runs_left = run_count - run - 1
            cycle_index = runs_left % pattern_size
            return weight_history[len(weight_history) - 1 - pattern_size + cycle_index]
        if len(weight_history) > 1000:
            weight_history.pop(0)
        run += 1
    return 0


def find_pattern_size(history):
    match_to = history[-1]
    latest_match = None
    i = len(history) - 2
    while i >= 0:
        current = history[i]
        if current == match_to:
            if latest_match is not None and latest_match - i > 1:
                return len(history) - latest_match - 1
            else:
                latest_match = i
        elif latest_match is not None:
            match_offset = latest_match - i
            if history[len(history) - match_offset - 1] != history[i]:
                latest_match = None
        i -= 1
    return None


def main(input_doc):
    start_time = time.time()
    loc_map = read_file(input_doc)
    loc_map_2 = copy.deepcopy(loc_map)
    print("---------------------")
    print("Day 14 " + '"' + input_doc + '"')
    loc_map.roll("N")
    print("Solution (Part 1): " + str(sum_all_weights(loc_map)))            # 109833
    print("Solution (Part 2): " + str(run_cycles(loc_map_2, 1000000000)))   # 99875
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
