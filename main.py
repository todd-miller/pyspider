import os

from engine import LABELS, Board


class Command:
    SUIT_MAP = {
        'h': '❤',
        'c': '♣',
        'd': '♦',
        's': '♠'
    }
    def __init__(self, value: str, board: Board):
        self.value = value
        self.board = board

    def parseCard(self, card: str):
        head = card[:-1]
        tail = card[-1]

        validLength = head in LABELS 
        lastCharacterIsSuit = tail in self.SUIT_MAP 
    
        if validLength and lastCharacterIsSuit: 
            return f"{head}{self.SUIT_MAP[tail]}"
        else:
            raise ValueError(f"Invalid card could not be parsed: {card}")

    def __contains__(self, item):
        return item in self.value

    def attemptMove(self):
        cards = self.value.split('to')
        try:
            move = [self.parseCard(card.strip()) for card in cards]
        except ValueError as e:
            move = f"ERROR: {e}\n invalid move: {cards[0]} -> {cards[1]}"
        return move

    @property
    def move(self):
        return 'to' in self.value

    @property
    def exit(self):
        return self.value in ["exit", "clear"]

    @property
    def deal(self):
        return self.value == "deal"


def main():
    board = Board.new()
    os.system('clear')
    while True:
        board.draw()
        command = Command(input("command: "), board)

        if command.deal:
            print("....dealing....")

        elif command.move:
            move = command.attemptMove()
            os.system('clear')
            print(f"{move}")

        elif command.exit:
            break

    print("\tGame Over")


if __name__ == "__main__":
    main()
