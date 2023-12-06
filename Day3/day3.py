import re


def process_line(a_line):
    pass


f = open("input.txt", "r")
ret_val = 0
for line in f:
    ret_val += process_line(line)
print(ret_val)
