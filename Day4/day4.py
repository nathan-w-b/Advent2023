import re


def main(input_doc):
    print("---------------------")
    print("Day 4 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(sum_card_points(input_doc)))      # 32609
    print("Solution (Part 2): " + str(sum_num_cards(input_doc)))        # 14624680
    print("---------------------")


def sum_card_points(input_doc):
    f = open(input_doc, "r")
    sum = 0
    for card in f:
        num_matches = get_card_match_count(card)
        if num_matches > 0:
            sum += 2 ** (num_matches - 1)
    f.close()
    return sum


def sum_num_cards(input_doc):
    f = open(input_doc, "r")
    sum = 0
    running_tally = []
    for card in f:
        num_matches = get_card_match_count(card)
        num_cards = 1
        if len(running_tally) > 0:
            num_cards += running_tally.pop(0)
        sum += num_cards
        for x in range(num_matches):
            if len(running_tally) < x + 1:
                running_tally.append(num_cards)
            else:
                running_tally[x] += num_cards
    f.close()
    return sum


def get_card_match_count(card):
    card = re.sub(".*[0-9]*:\s", "", card)
    winning_nums_string = re.search(".*\s[|]", card).group()
    card_nums_string = re.search("[|]\s.*", card).group()
    winning_nums = re.split("\s", winning_nums_string)
    winning_nums.pop()
    while True:
        if '' in winning_nums:
            winning_nums.remove('')
        else:
            break

    card_nums = re.split("\s", card_nums_string)
    card_nums.pop(0)
    matches = 0
    for num in card_nums:
        if num in winning_nums:
            matches += 1

    return matches


main("input.txt")
