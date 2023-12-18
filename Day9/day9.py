import re
import time


class ValueHistory:
    def __init__(self, values,):
        self.values = values

    def find_next_val(self):
        differences = []
        finished = True
        for x in range(1, len(self.values)):
            new_dif = self.values[x] - self.values[x-1]
            differences.append(new_dif)
            if new_dif != 0:
                finished = False
        if finished:
            return self.values[-1]
        else:
            return ValueHistory(differences).find_next_val() + self.values[-1]

    def find_prev_val(self):
        differences = []
        finished = True
        for x in range(1, len(self.values)):
            new_dif = self.values[x] - self.values[x - 1]
            differences.append(new_dif)
            if new_dif != 0:
                finished = False
        if finished:
            return self.values[0]
        else:
            return self.values[0] - ValueHistory(differences).find_prev_val()


def get_sum_of_next_values(value_histories):
    sum = 0
    for history in value_histories:
        solution = history.find_next_val()
        sum += solution
    return str(sum)


def get_sum_of_prev_values(value_histories):
    sum = 0
    for history in value_histories:
        solution = history.find_prev_val()
        sum += solution
    return str(sum)


def read_file(input_doc):
    value_histories = []
    f = open(input_doc, "r")
    for line in f:
        values = re.split(' ', line)
        for x in range(len(values)):
            values[x] = int(values[x])
        value_histories.append(ValueHistory(values))
    f.close()
    return value_histories


def main(input_doc):
    start_time = time.time()
    value_histories = read_file(input_doc)
    print("---------------------")
    print("Day 9 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(get_sum_of_next_values(value_histories)))     # 1904165718
    print("Solution (Part 2): " + str(get_sum_of_prev_values(value_histories)))     # 964
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
