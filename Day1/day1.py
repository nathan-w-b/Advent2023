import re


def main():
    f = open("input.txt", "r")
    answer = 0
    answer_2 = 0
    for line in f:
        answer += first_and_last_digit(line)
        answer_2 += first_and_last_digit(insert_digits_into_literals(line))
    print("Solution (Part 1): " + str(answer))       # 54331
    print("Solution (Part 2): " + str(answer_2))     # 54518
    f.close()


def first_and_last_digit(a_line):
    digits = re.findall("[1-9]", a_line)
    value = int(digits[0] + digits[-1])
    return value


def insert_digits_into_literals(a_line):
    a_line = insert_digit("one", "1", a_line)
    a_line = insert_digit("two", "2", a_line)
    a_line = insert_digit("three", "3", a_line)
    a_line = insert_digit("four", "4", a_line)
    a_line = insert_digit("five", "5", a_line)
    a_line = insert_digit("six", "6", a_line)
    a_line = insert_digit("seven", "7", a_line)
    a_line = insert_digit("eight", "8", a_line)
    a_line = insert_digit("nine", "9", a_line)

    return a_line


def insert_digit(digit_string, digit, a_line):
    x = re.search(digit_string, a_line)
    while x:
        insert_index = x.start()+1
        a_line = a_line[:insert_index] + digit + a_line[insert_index:]
        x = re.search(digit_string, a_line)
    return a_line


main()
