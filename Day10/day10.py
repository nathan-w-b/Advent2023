import re
import time
import math


loc_map = {}
start_loc = None
row_size = 0
col_size = 0
inner_region = None
right_turns = 0
region_1 = []
region_2 = []


class Location:
    def __init__(self, value, row=0, col=0, last_traveled=None):
        self.value = value
        self.row = row
        self.col = col
        self.key = get_key(self.row, self.col)
        self.last_traveled = last_traveled
        self.region = None      # 0 = traversed, 1 = region A (left), 2 = region B (right)
        self.step_index = -1

    def get_next_location(self, marking=False):
        global inner_region, row_size, col_size, right_turns
        # if self.region == 1:
        #     # print("stuff")
        #     region_1.remove(self)
        # elif self.region == 2:
        #     # print("stuff 2")
        #     region_2.remove(self)
        self.region = 0
        mark_ids_1 = []
        mark_ids_2 = []
        travel_dir = None
        if self.step_index >= 0:
            return None
        elif self.value == "|":
            if self.last_traveled == "N":
                mark_ids_1 = [0, 3, 5]
                mark_ids_2 = [3, 4, 7]
                travel_dir = self.last_traveled
            elif self.last_traveled == "S":
                mark_ids_1 = [3, 4, 7]
                mark_ids_2 = [0, 3, 5]
                travel_dir = self.last_traveled
            else:
                return None
        elif self.value == "-":
            if self.last_traveled == "E":
                mark_ids_1 = [0, 1, 2]
                mark_ids_2 = [5, 6, 7]
                travel_dir = self.last_traveled
            elif self.last_traveled == "W":
                mark_ids_1 = [5, 6, 7]
                mark_ids_2 = [0, 1, 2]
                travel_dir = self.last_traveled
            else:
                return None
        elif self.value == "L":
            if self.last_traveled == "S":
                mark_ids_1 = [2]
                mark_ids_2 = [0, 3, 5, 6, 7]
                travel_dir = "E"
                right_turns -= 1
            elif self.last_traveled == "W":
                mark_ids_1 = [0, 3, 5, 6, 7]
                mark_ids_2 = [2]
                travel_dir = "N"
                right_turns += 1
        elif self.value == "J":
            if self.last_traveled == "S":
                mark_ids_1 = [2, 4, 7, 6, 5]
                mark_ids_2 = [0]
                travel_dir = "W"
                right_turns += 1
            elif self.last_traveled == "E":
                mark_ids_1 = [0]
                mark_ids_2 = [2, 4, 7, 6, 5]
                travel_dir = "N"
                right_turns -= 1
        elif self.value == "7":
            if self.last_traveled == "N":
                mark_ids_1 = [5]
                mark_ids_2 = [0, 1, 2, 4, 7]
                travel_dir = "W"
                right_turns -= 1
            elif self.last_traveled == "E":
                mark_ids_1 = [0, 1, 2, 4, 7]
                mark_ids_2 = [5]
                travel_dir = "S"
                right_turns += 1
        elif self.value == "F":
            if self.last_traveled == "N":
                mark_ids_1 = [5, 3, 0, 1, 2]
                mark_ids_2 = [7]
                travel_dir = "E"
                right_turns += 1
            elif self.last_traveled == "W":
                mark_ids_1 = [7]
                mark_ids_2 = [5, 3, 0, 1, 2]
                travel_dir = "S"
                right_turns -= 1
        elif self.value == "S":
            return None
        if travel_dir is not None:
            if marking:
                self.mark(mark_ids_1, 1)
                self.mark(mark_ids_2, 2)
            return self.travel(travel_dir)
        else:
            return None

    def travel(self, direction, mark=True):
        global loc_map
        if direction == "N":
            next_loc = loc_map[get_key(self.row - 1, self.col)]
        elif direction == "S":
            next_loc = loc_map[get_key(self.row + 1, self.col)]
        elif direction == "W":
            next_loc = loc_map[get_key(self.row, self.col - 1)]
        elif direction == "E":
            next_loc = loc_map[get_key(self.row, self.col + 1)]
        next_loc.last_traveled = direction
        # if mark:
        #     next_loc.region = 0
        return next_loc

    def mark(self, loc_ids, region_num):
        global loc_map, inner_region, region_1, region_2
        adjacent_keys = get_adjacent_keys(self.row, self.col)
        for loc_id in loc_ids:
            key = adjacent_keys[loc_id]
            if key is not None:
                loc = loc_map[key]
                if loc.region is None:
                    loc.region = region_num
                    if region_num == 1:
                        # print("appending 1")
                        region_1.append(loc)
                    elif region_num == 2:
                        # print("appending 2")
                        region_2.append(loc)


def get_key(row_num, col_num):
    return str(row_num) + ',' + str(col_num)


def get_row_col(key):
    data = re.split(",", key)
    return int(data[0]), int(data[1])


def get_adjacent_keys(row, col):
    global row_size, col_size
    ret_val = []
    if row > 0:
        if col > 0:
            ret_val.append(get_key(row - 1, col - 1))
        else:
            ret_val.append(None)
        ret_val.append(get_key(row - 1, col))
        if col < col_size:
            ret_val.append(get_key(row - 1, col + 1))
        else:
            ret_val.append(None)
    else:
        ret_val.append(None)
        ret_val.append(None)
        ret_val.append(None)

    if col > 0:
        ret_val.append(get_key(row, col - 1))
    else:
        ret_val.append(None)
    if col < col_size - 1:
        ret_val.append(get_key(row, col + 1))
    else:
        ret_val.append(None)

    if row < row_size - 1:
        if col > 0:
            ret_val.append(get_key(row + 1, col - 1))
        else:
            ret_val.append(None)
        ret_val.append(get_key(row + 1, col))
        if col < col_size - 1:
            ret_val.append(get_key(row + 1, col + 1))
        else:
            ret_val.append(None)
    else:
        ret_val.append(None)
        ret_val.append(None)
        ret_val.append(None)

    return ret_val


def read_file(input_doc):
    global loc_map, start_loc, row_size, col_size
    f = open(input_doc, "r")
    row = -1
    for line in f:
        if len(line) > 1:
            row += 1
            if row == 0:
                col_size = (len(line) - 1)
            for x in range(col_size):
                key = get_key(row, x)
                loc_map[key] = Location(line[x], row, x)
                if line[x] == 'S':
                    start_loc = loc_map[key]
                    start_loc.step_index = 0
                    start_loc.region = 0
    row_size = row + 1
    print(row_size)
    f.close()


def init_start_location():
    global loc_map, start_loc
    locations = [
        start_loc.travel("N", False),
        start_loc.travel("E", False),
        start_loc.travel("S", False),
        start_loc.travel("W", False)
    ]
    checking = []
    index_value = locations[0].value
    if index_value == "F" or index_value == "|" or index_value == "7":
        checking.append(0)
    index_value = locations[1].value
    if index_value == "J" or index_value == "-" or index_value == "7":
        checking.append(1)
    index_value = locations[2].value
    if index_value == "J" or index_value == "|" or index_value == "L":
        checking.append(2)
    index_value = locations[3].value
    if index_value == "L" or index_value == "-" or index_value == "F":
        checking.append(3)
    if 0 in checking and 1 in checking:
        start_loc.value = "L"
        start_loc.last_traveled = "W"
    if 0 in checking and 2 in checking:
        start_loc.value = "|"
        start_loc.last_traveled = "N"
    if 0 in checking and 3 in checking:
        start_loc.value = "J"
        start_loc.last_traveled = "E"
    if 1 in checking and 2 in checking:
        start_loc.value = "F"
        start_loc.last_traveled = "N"
    if 1 in checking and 3 in checking:
        start_loc.value = "-"
        start_loc.last_traveled = "E"
    if 2 in checking and 3 in checking:
        start_loc.value = "7"
        start_loc.last_traveled = "N"

    return locations[checking[0]]

def find_longest_num_steps():
    global loc_map, start_loc
    first_step = init_start_location()

    # locations = [
    #     start_loc.travel("N", False),
    #     start_loc.travel("S", False),
    #     start_loc.travel("W", False),
    #     start_loc.travel("E", False)
    # ]

    steps = 1
    # next_locations = []
    # while True:
    #     for location in locations:
    #         next_loc = location.get_next_location(True)
    #         if next_loc:
    #             next_locations.append(next_loc)
    #             location.step_index = steps
    #             location.region = 0
    #     locations = next_locations
    #     next_locations = []
    #     if len(locations) <= 0:
    #         return steps - 1
    #     steps += 1
    current_loc = first_step
    while True:
        next_loc = current_loc.get_next_location(True)
        if next_loc:
            current_loc.step_index = steps
            current_loc = next_loc
        if next_loc == start_loc:
            return int(math.ceil((steps + 1) / 2))
        steps += 1


def find_area_enclosed_by_loop():
    global loc_map, start_loc, row_size, col_size, inner_region, right_turns, region_1, region_2


    # current_loc = None
    # for location in locations:
    #     current_loc = location
    #     next_loc = location.get_next_location(True)
    #
    #     if next_loc is not None:
    #         current_loc = next_loc
    #         location.region = 0
    #         break

    # while True:
    #     next_loc = current_loc.get_next_location(True)
    #     if current_loc == start_loc:
    #         break
    #     current_loc = next_loc

    # for row in range(row_size):
    #     for col in range(col_size):
    #         loc = loc_map[get_key(row, col)]
    #         print(loc.key + ": " + str(loc.region))
    #

    num_enclosed = 0
    if right_turns > 0:
        working_region = region_2
        inner_region = 2
    else:
        working_region = region_1
        inner_region = 1
    # print(inner_region)
    # print(len(working_region))
    while len(working_region) > 0:
        working_loc = working_region.pop(0)
        if working_loc.region > 0:
            row = working_loc.row
            col = working_loc.col
            # print(str(row) + "," + str(col))
            next_locs = [
                loc_map[get_key(row, col + 1)],
                loc_map[get_key(row + 1, col)],
                loc_map[get_key(row + 1, col + 1)]
            ]
            for next_loc in next_locs:
                if next_loc.region is None:
                    next_loc.region = inner_region
                    working_region.append(next_loc)

            num_enclosed += 1
    return num_enclosed


def main(input_doc):
    start_time = time.time()
    read_file(input_doc)
    print("---------------------")
    print("Day 10 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(find_longest_num_steps()))            # 6733
    print("Solution (Part 2): " + str(find_area_enclosed_by_loop()))        # 435
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
