import re
import time


class Card:
    def __init__(self, face, joker=""):
        self.face = face
        self.value = self.get_value(joker)

    def get_value(self, joker):
        if self.face == joker:
            return 1
        elif self.face == "A":
            return 14
        elif self.face == "K":
            return 13
        elif self.face == "Q":
            return 12
        elif self.face == "J":
            return 11
        elif self.face == "T":
            return 10
        else:
            return int(self.face)


class Hand:
    def __init__(self, hand_string, bid_string, joker=""):
        if joker != "":
            self.num_jokers = len(re.findall(joker, hand_string))
        else:
            self.num_jokers = 0
        self.hand_string = hand_string.replace(joker, "")
        cards = []
        for char in hand_string:
            cards.append(Card(char, joker))
        self.cards = cards
        self.bid = int(bid_string)
        self.strength = self.get_strength()
        # strengths:
        # high card=1, one pair=2, two pair=3, three of a kind=4, full house=5, four of a kind=6, five of a kind=7

    def __lt__(self, other):
        if self.strength != other.strength:
            return self.strength < other.strength
        else:
            for x in range(len(self.cards)):
                if self.cards[x].value != other.cards[x].value:
                    return self.cards[x].value < other.cards[x].value

    def strength_of_cards_by_first(self, string_of_cards):
        kinds = len(re.findall(string_of_cards[0], string_of_cards))
        if kinds == 5:
            return 7
        elif kinds == 4:
            return 6
        elif kinds == 3:
            return 4
        elif kinds == 2:
            return 2
        else:
            return 1

    def get_strength(self):
        max_strength = 1
        working_hand = self.hand_string
        while len(working_hand) > 1:
            strength = self.strength_of_cards_by_first(working_hand)
            if strength > 4:
                max_strength = strength
                break
            elif strength + max_strength == 6:
                max_strength = 5
                break
            elif strength == 4:
                max_strength = 4
            elif strength == 2:
                if max_strength == 2:
                    max_strength = 3
                    break
                else:
                    max_strength = 2
            working_hand = working_hand.replace(working_hand[0], "")
        if self.num_jokers >= 4:
            return 7
        elif self.num_jokers == 3:
            return max_strength + 5
        elif self.num_jokers == 2:
            if max_strength == 4:
                return 7
            elif max_strength == 2:
                return 6
            else:
                return 4
        elif self.num_jokers == 1:
            if max_strength > 4:
                return 7
            elif max_strength > 1:
                return max_strength + 2
            else:
                return 2
        else:
            return max_strength


def get_total_winnings(input_doc, joker):
    f = open(input_doc, "r")
    hands = []
    for line in f:
        hands.append(Hand(
            re.search(".*\s", line).group()[:5],
            re.search("\s[0-9]*", line).group()[1:],
            joker))
    f.close()
    hands = sorted(hands)
    winnings = 0
    for x in range(len(hands)):
        winnings += hands[x].bid * (x + 1)
    return winnings


def main(input_doc):
    start_time = time.time()
    print("---------------------")
    print("Day 7 " + '"' + input_doc + '"')
    print("Solution (Part 1): " + str(get_total_winnings(input_doc, "")))   # 252656917
    print("Solution (Part 2): " + str(get_total_winnings(input_doc, "J")))  # 253499763
    print("---------------------")
    print(" - Process took " + str((time.time() - start_time) * 1000) + "ms")


main("input.txt")
