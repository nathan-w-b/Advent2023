import re
import time


class RowOrigin:
    def __init__(self, springs_string, bad_series_counts):
        self.springs_string = springs_string
        self.bad_springs_series = re.findall("[#?]+", springs_string)
        self.bad_springs_total = len(re.findall("[#]", springs_string))
        self.bad_series_counts = bad_series_counts
        self.converts_left = sum(bad_series_counts) - self.bad_springs_total

    def find_combinations_brute_force(self):
        sum_combinations = 0
        unknown_indices = []
        for x in range(len(self.springs_string)):
            if self.springs_string[x] == "?":
                unknown_indices.append(x)

        row_converts = RowConverts(self.springs_string, unknown_indices, 0, self.converts_left).iterate_converts()
        for row_convert in row_converts:
            if row_convert.is_valid(self.bad_series_counts):
                sum_combinations += 1

        return sum_combinations

    def convert_to_part_two(self):
        new_springs_string = self.springs_string
        new_bad_series_count = self.bad_series_counts[:]
        for x in range(4):
            new_springs_string += "?" + self.springs_string
            new_bad_series_count.extend(self.bad_series_counts)

        self.springs_string = new_springs_string
        self.bad_springs_series = re.findall("[#?]+", new_springs_string)
        self.bad_springs_total = len(re.findall("[#]", new_springs_string))
        self.bad_series_counts = new_bad_series_count
        self.converts_left = sum(new_bad_series_count) - self.bad_springs_total

    def find_sum_valid_combinations(self):
        sum_combinations = 0

    # def sequence_is_valid(self, sequence_counts):
    #     if len(sequence_counts) != len(self.bad_series_counts):
    #         return False
    #     for x in range(len(sequence_counts)):
    #         if sequence_counts[x] != self.bad_series_counts[x]:
    #             return False
    #     return True

    def print_row(self):
        print(self.bad_springs_series)
        print(self.bad_series_counts)
        print("---------")


class RowConverts:
    def __init__(self, curr_string, rem_converts, rem_converts_index, converts_left):
        self.curr_string = curr_string
        self.rem_converts = rem_converts
        self.rem_converts_index = rem_converts_index
        self.converts_left = converts_left

    def iterate_converts(self):
        if self.converts_left == 0:
            return [self]
        else:
            ret_val = []
            new_converts_left = self.converts_left - 1
            for x in range(self.rem_converts_index, len(self.rem_converts) - self.converts_left + 1):
                curr_convert = self.rem_converts[x]
                new_curr_string = self.curr_string[:curr_convert] + "#" + self.curr_string[curr_convert+1:]
                new_row_convert = RowConverts(new_curr_string, self.rem_converts, x+1, new_converts_left)
                valid_converts = new_row_convert.iterate_converts()
                if valid_converts is not None:
                    ret_val.extend(valid_converts)
            return ret_val

    def is_valid(self, valid_counts):
        series = re.findall("[#]+", self.curr_string)

        if len(valid_counts) != len(series):
            return False
        for x in range(len(valid_counts)):
            if valid_counts[x] != len(series[x]):
                return False
        return True


class BadSeries:
    def __init__(self, string, converts_left):
        self.string = string
        self.converts_left = converts_left
        self.counts = self.find_bad_series_counts(string)

    def valid_possibilities(self, counts):
        if len(self.counts) == 0 or \
                self.counts[0] > counts[0] or \
                self.find_max_first_series_count(self.string, self.converts_left) < counts[0] or \
                len(self.string) < sum(counts):
            return []
        else:
            ret_val = []

    def finished(self, counts):
        if len(self.counts) != len(counts):
            return False
        for x in range(len(self.counts)):
            if self.counts[x] != counts[x]:
                return False
        return True

    def find_max_first_series_count(self, a_string, converts_left):
        first_bad_search = re.search("[#]", a_string)
        string_index = first_bad_search.start()
        while string_index < len(a_string):
            if a_string[string_index] == "?":
                a_string[string_index] = "#"
                if converts_left > 0:
                    converts_left -= 1
                else:
                    break
            string_index += 1
        if converts_left > 0:
            string_index = first_bad_search.start() - 1
            while string_index >= 0:
                if a_string[string_index] == "?":
                    a_string[string_index] = "#"
                    if converts_left > 0:
                        converts_left -= 1
                    else:
                        break
                string_index -= 1
        return len(re.search("[#]+", a_string).group())


    def find_uncertain_indices(self, a_string):
        ret_val = []
        for x in range(len(a_string)):
            if a_string[x] == "?":
                ret_val.append(x)
        return ret_val

    def find_bad_series_counts(self, a_string):
        bad_series = re.findall("[#]+", a_string)
        ret_val = []
        for series in bad_series:
            ret_val.append(len(series))
        return ret_val


def read_file(input_doc):
    rows = []
    f = open(input_doc, "r")
    for line in f:
        springs_string = re.search("[.#?]+", line).group()
        series_string = re.search("[0-9,]+", line).group()
        counts_string = re.split(",", series_string)
        counts = []
        for count_string in counts_string:
            counts.append(int(count_string))
        rows.append(RowOrigin(springs_string, counts))
    f.close()

    return rows


def get_sum_row_combinations_brute_force(rows):
    sum_row_comb = 0
    for row in rows:
        sum_row_comb += row.find_combinations_brute_force()
    return sum_row_comb


def get_sum_row_combinations_brute_force_part_two(rows):
    sum_row_combs = 0
    for row in rows:
        row.convert_to_part_two()
        row.print_row()
        sum_row_comb = row.find_combinations_brute_force()
        print(sum_row_comb)
        sum_row_combs += sum_row_comb
    return sum_row_combs


def get_sum_row_combinations(rows):
    return "TBD"


def get_sum_row_combinations_part_two(rows):
    return "TBD"


def main(input_doc):
    brute_force = True
    start_time = time.time()
    rows = read_file(input_doc)
    print("---------------------")
    print("Day 12 " + '"' + input_doc + '"')
    if brute_force:
        print("Solution (Part 1): " + str(get_sum_row_combinations_brute_force(rows)))              # 7716
        # print("Solution (Part 2): " + str(get_sum_row_combinations_brute_force_part_two(rows)))
    else:
        print("Solution (Part 1): " + str("TBD"))
        print("Solution (Part 2): " + str("TBD"))
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
