import re
import time
import math


class RaceDef:
    def __init__(self, time, dist):
        self.time = time
        self.dist = dist
        self.num_solutions = self.get_num_solutions()

    def get_num_solutions(self):
        num_solutions = 0
        test_end = int(math.floor(self.time / 2))
        for x in range(1, test_end + 1):
            distance = x * (self.time - x)
            if distance > self.dist:
                num_solutions = test_end - x + 1
                break
        num_solutions *= 2
        if self.time % 2 == 0:
            num_solutions -= 1

        return num_solutions


def read_input(input_doc):
    f = open(input_doc, "r")
    time_string = re.sub(".*[:]\s*", "", f.readline())
    times = re.split("\s", time_string)
    while '' in times:
        times.remove('')
    dist_string = re.sub(".*[:]\s*", "", f.readline())
    distances = re.split("\s", dist_string)
    while '' in distances:
        distances.remove('')
    f.close()

    races = []
    for x in range(len(times)):
        races.append(RaceDef(int(times[x]), int(distances[x])))

    return races


def get_best_times_multiplied(input_doc):
    races = read_input(input_doc)
    ret_val = 1
    for race in races:
        ret_val *= race.num_solutions

    return ret_val


def get_best_time_part_two(input_doc):
    f = open(input_doc, "r")
    time_string = re.sub(".*[:]\s*", "", f.readline()).replace(" ", "")
    dist_string = re.sub(".*[:]\s*", "", f.readline()).replace(" ", "")
    f.close()

    return RaceDef(int(time_string), int(dist_string)).num_solutions


def main(input_doc):
    start_time = time.time()
    print("---------------------")
    print("Day 6 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(get_best_times_multiplied(input_doc)))    # 1624896
    print("Solution (Part 2): " + str(get_best_time_part_two(input_doc)))       # 32583852
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
