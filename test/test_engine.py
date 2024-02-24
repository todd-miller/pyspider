import random

from ..engine import (
    HIDDEN_SYMBOL, SUITS,
    LABELS, Card, Factory, Pile, Board 
)


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


        assert len(canStack) == 4


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
                "3❤ cannot be stacked on 3❤"
            ),

            (
                ['4❤', '3❤'],
                ['2♦', 'A♦'],
                ['4❤', '3❤','2♦', 'A♦'],
            )
        ]

        for case in cases:
            visible, newCards, expected = case
            pile = Pile(hidden=[], visible=[Card.fromStr(card) for card in visible])
            toAdd = Card.cardsFromStrings(newCards) 

            canAdd, message = pile.canAddCards(toAdd)

            if canAdd:
                pile.addCards(toAdd)
                assert Card.cardsToStrings(pile.visible) == expected
            else:
                assert message == expected

    def test_removeCards(self):
        # TODO - need to extend cases
        cases = [
            (
                [],                        # current Pile.hidden
                ['4❤', '3❤', '2❤', 'A❤'],  # current Pile.visible
                1,                         # index to grab and remove all cards after index
                ['4❤']                     # expected result
            ),
            (
                [],
                ['4❤', '10♦', '2❤', 'A❤'],
                1,
                "10♦ can not be moved with 2❤, attempting to move: ['10♦', '2❤', 'A❤']"
            ),
            (
                [],
                [],
                0,
                "list index out of range"
            ),
            (
                ['Q❤'],
                ['10♦'],
                0,
                ['Q❤'],
            )


        ]
        for case in cases:
            hidden, visible, moveIndex, expected = case
            pile = Pile(
                hidden=Card.cardsFromStrings(hidden),
                visible=Card.cardsFromStrings(visible),
                completed=[]
            )

            canRemove, message = pile.canRemoveCards(moveIndex)
            if canRemove:
                pile.removeCards(moveIndex)
                assert Card.cardsToStrings(pile.visible) == expected
            else:
                assert message == expected

    def test_hiddenCardFlips(self):
        hidden = Card.cardsFromStrings(['J❤', '10♦', 'K❤', '7❤']) 
        visible = Card.cardsFromStrings(['10♦'])

        pile = Pile(hidden=hidden, visible=visible, completed=[])
        pile.removeCards(-1)
        assert pile.toJson() == list(HIDDEN_SYMBOL * 3) + ['7❤']

    def test_hiddenCards(self):
        hidden = Card.cardsFromStrings(['J❤', '10♦', 'K❤', '7❤'])
        visible = Card.cardsFromStrings(['10♦']) 

        pile = Pile(hidden=hidden, visible=visible)
        assert pile.toJson() == list(HIDDEN_SYMBOL*4) + ['10♦']

    def testCompletes(self):
        fullSuit = Factory().createSuit("♦", ascending=False)
        hiddenCard = Card.fromStr('J♣')
        pile = Pile(
            hidden=[hiddenCard], 
            visible=fullSuit[:-1], 
            completed=[]
        )
        pile.addCards([Card(suit='♦', label='A')])

        assert pile.completed == ['♦']
        assert pile.visible ==  [hiddenCard]
        assert pile.hidden == []

class TestBoard:

    def assertBoardShape(self, board) -> None:
        for i, pileSize in enumerate(Board.PILE_SIZES):
            hiddenSize = pileSize - 1
            pile = board.piles[i]
            assert len(pile.visible) == 1
            assert pile.toJson()[:hiddenSize] == list(HIDDEN_SYMBOL * hiddenSize)

        assert len(board.piles) == 10
        assert len(board.stack) == 50

    def test_newGame(self):
        shuffled = Board.new()
        unshuffled = Board.new(shuffle=False)

        self.assertBoardShape(shuffled)
        self.assertBoardShape(unshuffled)

    def test_move(self):
        board= Board.new(shuffle=False)
        board.draw()
        board.move((4, -1), 9)
        print('- ' * 25)
        board.draw()
        print('- ' * 25)
        board.move((2, -1), 9)
        board.draw()
        print('= ' * 25)

