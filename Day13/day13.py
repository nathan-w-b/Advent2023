import re
import time


class Terrain:
    def __init__(self):
        self.rock_rows = []
        self.rock_cols = []

    def append_row(self, a_string):
        self.rock_rows.append(Lane(a_string))
        if len(self.rock_cols) == 0:
            for char in a_string:
                if char == "#" or char == ".":
                    self.rock_cols.append(Lane(char))
        else:
            for i in range(len(a_string) - 1):
                self.rock_cols[i].add_char(a_string[i])

    def find_mirror_lane_value(self, smudge_count):
        ret_val = self.find_mirrored_lane(self.rock_rows, smudge_count)
        if ret_val is not None:
            return ret_val * 100
        else:
            return self.find_mirrored_lane(self.rock_cols, smudge_count)

    def find_mirrored_lane(self, rock_lanes, smudge_count):
        smudges_left = smudge_count
        for i in range(len(rock_lanes) - 1):
            differences = rock_lanes[i].lane_differences(rock_lanes[i+1])
            smudges_left -= differences
            if smudges_left >= 0:
                if self.check_proper_mirror(rock_lanes, i, smudges_left):
                    return i + 1
            smudges_left = smudge_count
        return None

    @staticmethod
    def check_proper_mirror(rock_lanes, index, smudges_left):
        offset = 1
        while index - offset >= 0 and index + offset + 1 < len(rock_lanes):
            differences = rock_lanes[index-offset].lane_differences(rock_lanes[index+offset+1])
            smudges_left -= differences
            if smudges_left < 0:
                return False
            offset += 1
        if smudges_left != 0:
            return False
        else:
            return True


class Lane:
    def __init__(self, string=""):
        if string == "":
            self.rocks = []
        else:
            self.rocks = find_rocks(string)

    def add_char(self, new_char):
        if new_char == "#":
            self.rocks.append(True)
        elif new_char == ".":
            self.rocks.append(False)

    def lane_differences(self, other_lane):
        differences = 0
        for i in range(len(self.rocks)):
            if self.rocks[i] != other_lane.rocks[i]:
                differences += 1
        return differences


def find_rocks(a_string):
    ret_val = []
    for char in a_string:
        if char == "#":
            ret_val.append(True)
        elif char == ".":
            ret_val.append(False)
    return ret_val


def read_file(input_doc):
    f = open(input_doc, "r")
    terrains = []
    next_terrain = Terrain()
    for line in f:
        if line != "\n":
            next_terrain.append_row(line)
        else:
            terrains.append(next_terrain)
            next_terrain = Terrain()
    f.close()
    terrains.append(next_terrain)
    return terrains


def sum_mirror_lane_values(terrains, smudge_count=0):
    sum_values = 0
    for terrain in terrains:
        mirror_lane_value = terrain.find_mirror_lane_value(smudge_count)
        sum_values += mirror_lane_value
    return sum_values


def main(input_doc):
    start_time = time.time()
    terrains = read_file(input_doc)
    print("---------------------")
    print("Day 13 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(sum_mirror_lane_values(terrains)))        # 28651
    print("Solution (Part 2): " + str(sum_mirror_lane_values(terrains, 1)))     # 25450
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
