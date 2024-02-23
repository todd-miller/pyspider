import random
from typing import List, Tuple  
from dataclasses import dataclass

SUITS = ("❤", "♠", "♣", "♦")
LABELS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

def createStacks():
    stacks = [] 
    for suit in SUITS:
        stack = []
        for label in LABELS:
            stack.append(f"{label}{suit}")
        stacks.append(stack)
    return list(stacks)

COMPLETE_STACKS = createStacks()

HIDDEN_SYMBOL = '?'


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

    @staticmethod
    def cardsToStrings(cards: List["Card"]) -> List[str]:
        return [str(card) for card in cards]

    @staticmethod
    def cardsFromStrings(cards: List[str]) -> List["Card"]:
        return [Card.fromStr(card) for card in cards]


class Pile:
    """
    stack of hidden and visible cards within 1/10 piles that comprise the Board
    hidden & visible lists are ordered from closest to the table to furthest away: 
        (hidden[0] is facedown touching the table)
        (visible[0] is back-to-back with hidden[-1])
    """
    def __init__(self, hidden: List[Card], visible: List[Card], completed: list = []):
        self.hidden = hidden
        self.visible = visible
        self.completed = completed if completed else []

    def __str__(self) -> str:
       return str(self.toJson())

    def toJson(self):
        return len(self.hidden)*['?'] + Card.cardsToStrings(self.visible)

    def checkIfCompleted(self):
        suit = self.visible[0].suit
        
        cardsToCheck = Card.cardsToStrings(
                self.visible[-len(LABELS):]
        )
        fullSuit = Card.cardsToStrings(
                Factory().createSuit(suit, ascending=False)
        )

        if len(self.visible) >= len(LABELS) and cardsToCheck == fullSuit:
            self.completed.append(suit)
            self.removeCards(-len(LABELS))
            self.flipNextCard()

    def addCards(self, cards: List[Card], force: bool = False) -> None:
        if self.canAddCards(cards) or force:
            self.visible += cards
        else:
            raise ValueError(f"{cards[0]} cannot be stacked on {self.visible[-1]}")

        self.checkIfCompleted()

    def canAddCards(self, cards: List[Card]) -> Tuple[bool, str]:
        canAdd = self.visible[-1].canStack(cards[0])
        message = ""
        if not canAdd:
            message = f"{cards[0]} cannot be stacked on {self.visible[-1]}"
        return canAdd, message

    def removeCards(self, index: int) -> None:
        self.visible = self.visible[:index]
        if len(self.visible) == 0 and len(self.hidden) > 0:
            self.flipNextCard()

    def canRemoveCards(self, index: int) -> Tuple[bool, str]:
        canRemove = True
        message = ""
        try:
            current = card = self.visible[index]
            for card in self.visible[index+1:]:
                if not current.canStack(card):
                    canRemove = False
                    break
                current = card

            if not canRemove:
                attemptedMove = Card.cardsToStrings(self.visible[index:])
                message = f"{current} can not be moved with {card}, attempting to move: {attemptedMove}"
        except IndexError as e:
            canRemove = False
            message = str(e)

        return canRemove, message 

    def flipNextCard(self):
        if len(self.hidden) > 0:
            nextCard = self.hidden.pop()
            self.visible.insert(0, nextCard)


class Board:
    PILE_SIZES = [6, 6, 6, 6, 5, 5, 5, 5, 5, 5]

    def __init__(self, piles: List[Pile], stack: List[Card], completed: List[Card]):
        self.piles = piles
        self.stack = stack
        self.completed = completed

    @classmethod
    def new(cls, shuffle: bool = True) -> "Board":
        deck = Factory().createSpiderDeck(shuffle) 

        piles = []
        completed = []
        for pileSize in cls.PILE_SIZES:
            pileCards = deck[-pileSize:]
            del deck[-pileSize:]
            piles.append(
                Pile(hidden=pileCards[:-1], visible=[pileCards[-1]], completed=completed)
            )

        return cls(piles=piles, stack=deck, completed=completed)

    def displayBoard(self):
        for index, pile in enumerate(self.piles):
            print(f"{index}"+ ":" + f"{pile.toJson()}")

    def move(self, start, end):
        srcPileIndex, srcCardIndex = start
        srcPile, targetPile = self.piles[srcPileIndex], self.piles[end]
        srcCards = srcPile.visible[srcCardIndex:]

        if targetPile.canAddCards(srcCards) and srcPile.canRemoveCards(srcCardIndex):
            targetPile.addCards(srcCards)
            srcPile.removeCards(srcCardIndex) 
        else:
            raise ValueError(f"Cannot move src cards: {[str(card) for card in srcCards]} to targetPile: {targetPile.toJson()}")
        

class Factory:
    @staticmethod
    def createSuit(suit: str, ascending: bool = True) -> List[Card]:
        cards = []
        for label in LABELS:
            cards.append(Card(suit, label))

        if not ascending:
            cards.reverse()

        return cards

    def createDeck(self) -> List[Card]:
        cards = []
        for suit in SUITS:
            cards += self.createSuit(suit)
        return cards

    def createSpiderDeck(self, shuffle=True) -> List[Card]:
        deck =  self.createDeck() + self.createDeck()
        if shuffle: random.shuffle(deck)
        return deck
        

