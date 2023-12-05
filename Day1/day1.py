import re

def process_line(a_line):
    a_line = translate_num("one", "1", a_line)
    a_line = translate_num("two", "2", a_line)
    a_line = translate_num("three", "3", a_line)
    a_line = translate_num("four", "4", a_line)
    a_line = translate_num("five", "5", a_line)
    a_line = translate_num("six", "6", a_line)
    a_line = translate_num("seven", "7", a_line)
    a_line = translate_num("eight", "8", a_line)
    a_line = translate_num("nine", "9", a_line)

    digits = re.findall("[1-9]", a_line)
    value = int(digits[0] + digits[-1])
    print(value)
    return value


def translate_num(string, num, a_line):
    x = re.search(string, a_line)
    while x:
        insert_int = x.start()+1
        a_line = a_line[:insert_int] + num + a_line[insert_int:]
        x = re.search(string, a_line)
    return a_line


f = open("input.txt", "r")
ret_val = 0
for line in f:
    ret_val += process_line(line)
print(ret_val)
