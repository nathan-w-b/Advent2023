import re


class NumberLocation:
    def __init__(self, value=0, used=False):
        self.value = value
        self.used = used

    def add_digit(self, digit):
        self.value = (self.value * 10) + int(digit)


def main(input_doc):
    print("Day 3")
    print(input_doc)
    print("Solution (Part 1): " + str(get_parts_sum(input_doc)))        # 557705
    print("Solution (Part 2): " + str(get_gear_ratio_sum(input_doc)))   # 84266818


def read_map(input_doc, regex):
    schematic_map = {}
    symbols = []
    f = open(input_doc, "r")
    row = 0
    for line in f:
        curr_num = NumberLocation()
        row += 1
        if row > 140:
            break
        col = 0
        for char in line:
            col += 1
            if col > 140:
                break
            if re.match("[0-9]", char):
                curr_num.add_digit(char)
                schematic_map[coord(row, col)] = curr_num
            elif re.match(regex, char):
                curr_num = NumberLocation()
                symbols.append(coord(row, col))
                schematic_map[coord(row, col)] = False
            else:
                curr_num = NumberLocation()
                schematic_map[coord(row, col)] = False
    f.close()
    return schematic_map, symbols


def get_parts_sum(input_doc):
    schematic_map, symbols = read_map(input_doc, "[^0-9.\s]")
    parts_sum = 0
    for symbol in symbols:
        for adj in get_adj_coords(symbol):
            if schematic_map[adj] and not schematic_map[adj].used:
                parts_sum += schematic_map[adj].value
                schematic_map[adj].used = True
    return parts_sum


def get_gear_ratio_sum(input_doc):
    schematic_map, symbols = read_map(input_doc, "[*]")
    ratio_sum = 0
    for symbol in symbols:
        adj_parts = []
        for adj in get_adj_coords(symbol):
            curr_adj = schematic_map[adj]
            if curr_adj and curr_adj not in adj_parts:
                adj_parts.append(curr_adj)
        if len(adj_parts) == 2:
            ratio_sum += adj_parts[0].value * adj_parts[1].value
    return ratio_sum


def row_col(coord_string):
    parts = re.split(",", coord_string)
    return int(parts[0]), int(parts[1])


def coord(row, col):
    return str(row) + "," + str(col)


def get_adj_coords(coord_string):
    row, col = row_col(coord_string)
    adj_coords = []
    for r in range(-1, 2):
        for c in range(-1, 2):
            if not (r == 0 and c == 0):
                if valid_loc(row + r, col + c):
                    adj_coords.append(coord(row + r, col + c))
    return adj_coords


def valid_loc(row, col):
    if row < 1 or row > 140 or col < 1 or col > 140:
        return False
    return True


main("input.txt")
