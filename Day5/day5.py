import re


class location:
    def __init__(self, loc=0, translated=False):
        self.loc = loc
        self.translated = translated

    def translate(self, dst_start, src_start, length):
        dist = self.loc - src_start
        if (dist >= 0) and (dist < length):
            movement = dst_start - src_start
            self.loc += movement
            self.translated = True


class loc_range:
    def __init__(self, start=0, range=0, translated=False):
        self.start = start
        self.range = 0
        self.last = 0
        self.update_range(range)
        self.translated = translated

    def move(self, dist):
        self.start += dist
        self.last += dist

    def update_range(self, new_range):
        self.range = new_range
        self.last = self.start + self.range - 1

    def print_range(self):
        print(str(self.start) + "..." + str(self.last) + ": " + str(self.range) + " -> " + str(self.translated))

    def translate(self, dst_start, src_start, length):
        src_last = src_start + length - 1

        # completely outside range
        if (self.start > src_last) or (self.last < src_start):
            return [self]
        # completely inside range
        elif (self.start >= src_start) and (self.range <= length):
            self.translated = True
            self.move(dst_start - src_start)
            return [self]

        ret_val = []
        if self.start < src_start:
            ret_val.append(loc_range(self.start, src_start - self.start, False))
        if self.last > src_last:
            ret_val.append(loc_range(src_last + 1, self.last - src_last + 1, False))
        movement = dst_start - src_start
        new_range_start = src_start
        if self.start > src_start:
            new_range_start = self.start
        new_range_last = src_last
        if self.last < new_range_last:
            new_range_last = self.last
        ret_val.append(loc_range(new_range_start + movement, new_range_last - new_range_start + 1, True))

        return ret_val


def get_closest_seed_loc(input_doc):
    f = open(input_doc, "r")
    seed_line = f.readline()
    seed_line = re.sub("seeds:\s", "", seed_line)
    seeds = re.split("\s", seed_line)
    seeds.pop()
    for x in range(len(seeds)):
        seeds[x] = location(int(seeds[x]))

    for line in f:
        if not line == "\n" and not re.match(".*map", line):
            data = re.split("\s", line)
            for x in range(3):
                data[x] = int(data[x])
            for seed in seeds:
                if not seed.translated:
                    seed.translate(data[0], data[1], data[2])
        elif re.match(".*map", line):
            for seed in seeds:
                seed.translated = False
    f.close()
    closest = seeds[0].loc
    for seed in seeds:
        if seed.loc < closest:
            closest = seed.loc
    return closest


def get_closest_seed_loc_from_ranges(input_doc):
    f = open(input_doc, "r")
    seed_line = f.readline()
    seed_line = re.sub("seeds:\s", "", seed_line)
    seeds = re.split("\s", seed_line)
    seeds.pop()
    seed_ranges = []
    working_range = loc_range()
    for x in range(len(seeds)):
        if x % 2 == 0:
            working_range = loc_range(int(seeds[x]))
        else:
            working_range.update_range(int(seeds[x]))
            seed_ranges.append(working_range)
    seed_ranges.sort(key=lambda x: x.start, reverse=False)
    for line in f:
        if not line == "\n" and not re.match(".*map", line):
            data = re.split("\s", line)
            for x in range(3):
                data[x] = int(data[x])
            working_index = 0
            for x in range(len(seed_ranges)):
                if not seed_ranges[working_index].translated:
                    seed_ranges.extend(seed_ranges.pop(working_index).translate(data[0], data[1], data[2]))
                else:
                    working_index += 1
        elif re.match(".*map", line):
            seed_ranges.sort(key=lambda x: x.start, reverse=False)
            for seed_range in seed_ranges:
                seed_range.translated = False
    f.close()
    seed_ranges.sort(key=lambda x: x.start, reverse=False)
    return seed_ranges[0].start


def main(input_doc):
    print("---------------------")
    print("Day 5 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(get_closest_seed_loc(input_doc)))             # 486613012
    print("Solution (Part 2): " + str(get_closest_seed_loc_from_ranges(input_doc))) # 56931769
    print("---------------------")


main("input.txt")
