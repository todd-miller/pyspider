import random
from typing import List
from dataclasses import dataclass

SUITS = ("❤", "♠", "♣", "♦")
LABELS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")


@dataclass
class Card:
    suit: str
    label: str

    def __str__(self):
        return f"{self.label}{self.suit}"

    def __repr__(self):
        return f"Card(suit='{self.suit}', label='{self.label}')"

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __gt__(self, other: "Card") -> bool:
        return self.value > other.value

    @property
    def value(self):
        return LABELS.index(self.label) + 1

    @property
    def color(self):
        if self.suit in ["♠", "♣"]:
            color = "black"
        else:
            color = "red"
        return color

    @classmethod
    def fromStr(cls, string: str) -> "Card":
        suit = []
        label = []
        for char in string:
            if char in SUITS:
                suit.append(char)
            else:
                label.append(char)

        suit = ''.join(suit)
        label = ''.join(label)
        return cls(suit=suit, label=label)

    @classmethod
    def fromValue(cls, suit: str, value: int) -> "Card":
        return cls(suit=suit, label=LABELS[value-1])

    def canStack(self, other: "Card") -> bool:
        sameSuit = other.suit == self.suit
        differentColor = other.color != self.color
        return (sameSuit or differentColor) and self.value == other.value + 1

    def strictEquals(self, other: "Card") -> bool:
        return self == other and self.suit == other.suit


@dataclass
class Pile:
    """
    stack of hidden and visible cards within 1/10 piles that comprise the Spider board
    hidden & visible lists are ordered from closest to the table to furthest away: 
        (hidden[0] is facedown touching the table)
        (visible[0] is back-to-back with hidden[-1])
    """
    hidden: List[Card]
    visible: List[Card]

    def __str__(self) -> str:
        hidden = ["𔓘" for _ in self.hidden] 
        visible = [str(card) for card in self.visible] 
        return str(hidden + visible)

    def visible_as_str(self):
        return [str(card) for card in self.visible] 


    def addCards(self, cards: List[Card], force: bool = False) -> None:
        if force or self.visible[-1].canStack(cards[0]):
            self.visible += cards
        else:
            raise ValueError(f"{cards[0]} cannot be stacked on {self.visible[-1]}")

    def removeCards(self, index: int) -> None:
        current = self.visible[index]
        for card in self.visible[index+1:]:
            if not current.canStack(card):
                raise ValueError(f"{current} can not be moved with {card}, attempting to move: {self.visible_as_str()[index:]}")
            current = card
        self.visible = self.visible[:index]


class SpiderGame:
    def __init__(self):
        self.init = True

    @classmethod
    def new(cls) -> "SpiderGame":
        deck = createDeck() + createDeck()
        random.shuffle(deck)

        # need piles, 4-stacks of 6, 6-stacks of 5
        # need heap
        piles = []
        for i in range(0, 10):
            print(i) 
            piles.append(Pile(visible=[], hidden=[]))

        return cls()


def createDeck() -> List[Card]:
    cards = []
    for suit in SUITS:
        for label in LABELS:
            cards.append(Card(suit, label))
    return cards


def main():
    spiderDeck = createDeck() + createDeck()
    print(f"numCards: {len(spiderDeck)}")
    for card in spiderDeck:
        print(f"{str(card)}, \t{repr(card)}")


if __name__ == "__main__":
    main()

    # TODO - 
    #   - test Stack
    #   - test Card 
