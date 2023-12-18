import functools
import re
import time
import fractions


class Location:
    def __init__(self, key, left_key, right_key):
        self.key = key
        self.left_key = left_key
        self.right_key = right_key

    def print_location(self):
        print(self.key + " = (" + self.left_key + ", " + self.right_key + ")")


def num_steps_to_exit(directions, node_network):
    num_steps = 0
    dir_index = -1
    current_loc = node_network["AAA"]
    while current_loc.key != "ZZZ":
        num_steps += 1
        dir_index += 1
        if dir_index >= len(directions):
            dir_index = 0

        if directions[dir_index] == 'R':
            current_loc = node_network[current_loc.right_key]
        elif directions[dir_index] == 'L':
            current_loc = node_network[current_loc.left_key]
        else:
            print("error in directions, unexpected char found... " + directions[dir_index])

    return num_steps


def num_steps_to_exit_2(directions, node_network):
    current_locs = []
    for key in node_network:
        if key[-1] == 'A':
            current_locs.append(node_network[key])

    cycle_size = len(directions)
    cycle_counts = []
    for loc in current_locs:
        current_loc = loc
        num_cycles = 0
        dir_index = -1
        while True:
            dir_index += 1
            
            if directions[dir_index] == 'R':
                current_loc = node_network[current_loc.right_key]
            elif directions[dir_index] == 'L':
                current_loc = node_network[current_loc.left_key]

            if dir_index == cycle_size - 1:
                dir_index = -1
                num_cycles += 1
                if current_loc.key[-1] == 'Z':
                    cycle_counts.append(num_cycles)
                    break

    return functools.reduce(lambda x, y: lcm(x, y), cycle_counts) * cycle_size


def lcm(a, b):
    return a*b // fractions.gcd(a, b)


def read_file(input_doc):
    f = open(input_doc, "r")
    # read directions string
    directions = f.readline()[:-1]
    # store node network in a dictionary
    node_network = {}
    for line in f:
        if line.strip() != '':
            keys = re.findall("[A-Z]+", line)
            if len(keys) > 0:
                node_network[keys[0]] = Location(keys[0], keys[1], keys[2])
    f.close()

    return directions, node_network


def main(input_doc):
    start_time = time.time()
    directions, node_network = read_file(input_doc)
    print("---------------------")
    print("Day 8 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(num_steps_to_exit(directions, node_network)))     # 22357
    print("Solution (Part 2): " + str(num_steps_to_exit_2(directions, node_network)))   # 10371555451871
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
