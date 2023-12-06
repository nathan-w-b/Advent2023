import re


class rgbSet:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def check_fail(self, draw_set_string):
        color_strings = re.split(",", draw_set_string)

        for color_string in color_strings:
            parts = re.split("\s", color_string)
            color_count = int(parts[1])
            color = parts[2]
            if color == "red":
                check = self.red
            elif color == "blue":
                check = self.blue
            else:
                check = self.green

            if color_count > check:
                return True
        return False

    def check(self, draw_set_string):
        color_strings = re.split(",", draw_set_string)

        for color_string in color_strings:
            parts = re.split("\s", color_string)
            color_count = int(parts[1])
            color = parts[2]
            if color == "red":
                if self.red < color_count:
                    self.red = color_count
            elif color == "blue":
                if self.blue < color_count:
                    self.blue = color_count
            else:
                if self.green < color_count:
                    self.green = color_count


def process_line(a_line, game_check):
    a_line = a_line[5:]
    game_num = re.search("[0-9]*", a_line).group()
    a_line = a_line[len(game_num)+1:]
    game_num = int(game_num)

    draws = re.split(";", a_line)
    for draw in draws:
        if game_check.check_fail(draw):
            return 0
    return game_num


def process_line_2(a_line):
    a_line = a_line[5:]
    game_num = re.search("[0-9]*", a_line).group()
    a_line = a_line[len(game_num) + 1:]

    draws = re.split(";", a_line)
    min_set = rgbSet(0, 0, 0)
    for draw in draws:
        min_set.check(draw)
    return min_set.red * min_set.blue * min_set.green


f = open("input.txt", "r")
ret_val = 0
ret_val_2 = 0
game_check = rgbSet(12, 13, 14)
for line in f:
    ret_val += process_line(line, game_check)
    ret_val_2 += process_line_2(line)
print(ret_val)
print(ret_val_2)
