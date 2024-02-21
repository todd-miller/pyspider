import random
import pytest

from ..main import Card, SUITS, LABELS, Pile


class TestCard: 
    def test_equality(self):
        card1 = Card(suit="❤", label="A");
        card2 = Card(suit="♣", label="A");
        card3 = Card(suit="❤", label="A");

        assert card1 == card2
        assert not card1.strictEquals(card2)
        assert card1.strictEquals(card3)

    def test_representations(self):
        suit, label = random.choice(SUITS), random.choice(LABELS)
        card = Card(suit, label);

        assert str(card) == f'{label}{suit}' 
        assert repr(card) == f"Card(suit='{suit}', label='{label}')"

    def test_canStack(self):
        base = Card(
            suit=random.choice(SUITS), 
            label=random.choice(list(LABELS)[1:])
        )

        canStack = [];
        for suit in SUITS:
            otherCard = Card.fromValue(suit=suit, value=base.value-1)
            if base.canStack(otherCard):
                canStack.append(str(otherCard))


        assert len(canStack) == 3


class TestPile:
    def test_addCards(self):
        cases = [
            (
                ['4❤', '3❤'],  # current Pile
                ['2❤', 'A❤'],  # cards to Add
                ['4❤', '3❤', '2❤', 'A❤']  # expected result
            ),
            (
                ['4♣', '3♣'],
                ['2❤', 'A❤'],
                ['4♣', '3♣', '2❤', 'A❤']
            ),

            (
                ['4❤', '3❤'],
                ['3❤', '2❤'],
                ValueError("3❤ cannot be stacked on 3❤")
            ),

            (
                ['4❤', '3❤'],
                ['2♦', 'A♦'],
                ValueError("2♦ cannot be stacked on 3❤")
            )
        ]

        for case in cases:
            visible, newCards, expected = case
            pile = Pile(hidden=[], visible=[Card.fromStr(card) for card in visible])
            toAdd = [Card.fromStr(card) for card in newCards]

            if isinstance(expected, Exception):
                with pytest.raises(type(expected)) as e:
                    pile.addCards(toAdd)
                assert str(e.value) == str(expected)

            else:
                pile.addCards(toAdd)
                assert pile.visible_as_str() == expected
    
    def test_removeCards(self):
        cases = [
            (
                ['4❤', '3❤', '2❤', 'A❤'],  # current Pile
                1,                         # index to grab and remove all cards after index
                ['4❤']                     # expected result
            ),
            (
                ['4❤', '10♦', '2❤', 'A❤'],
                1,
                ValueError("10♦ can not be moved with 2❤, attempting to move: ['10♦', '2❤', 'A❤']")
            )
        ]
        for case in cases:
            visibleCards, moveIndex, expected = case
            cards =  [Card.fromStr(card) for card in visibleCards]
            pile = Pile(hidden=[], visible=cards)

            if isinstance(expected, Exception):
                print("here at is Exception")
                with pytest.raises(type(expected)) as e:
                    pile.removeCards(moveIndex)
                assert str(e.value) == str(expected)

            else:
                pile.removeCards(moveIndex)
                assert pile.visible_as_str() == expected

