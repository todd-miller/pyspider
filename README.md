# PySpider
Spider-solitare game logic within python and the command line.


## Motivation
Sensible toe-dip into game programming while using some tools I already know. My goal
to have a neat thing to do as a side project that is very, very small in scope.

If I like it, i'll spin it into other projects
If I hate it, i'll probably delete this README, so no worries.

## Helpful Commands:
test methods matching <testName> while displaying stdout for tests that are passing
`pytest -k <testName> -rP`

## Progress So Far:
I can print a graphically simple, but logically accurate board. 

- a Card has:
    - a label
    - a suit
- each Pile can:
    - display cards correctly where hidden cards are displayed as '?'
    - append legal cards to the Pile
    - make legal removes from the Pile 
    - removes cards that are part of a completed set 
    - keeps track of completed sets
- the SpiderGame can:
    - handle player moves, where illegal moves are simply not transacted

### Graphics
COMPLETE: 0
0:['?', '?', '?', '?', '?', 'K♦']
1:['?', '?', '?', '?', '?', '7♦']
2:['?', '?', '?', '?', 'K♣']
3:['?', '?', '?', '?', '?', '8♣']
4:['?', '?', '?', 'A♣']
5:['?', '?', '?', '?', '10♠']
6:['?', '?', '?', '?', '5♠']
7:['?', '?', '?', '?', 'K❤']
8:['?', '?', '?', '?', '8❤']
9:['?', '?', '?', '?', '3❤', '2♣', 'A♦']
REMAINING: 5

## Next Steps:
- Game Loop -> need to add controls to make this playable
- Make UX better, 
    - make the commands as simple as possible for making command line moves
    - i forsee an issue of a user entering the suits icon:
        - maybe i'll listen for double "hh = ❤", "dd = ♦", etc.
- Single click returns first legal move option 
        - I'd like to write this, it seems fun
- Test a full game
    - wonder if I could keep a fixture that's an entire game worth of moves and just
    have the computer run it.
...
- I wonder how good I could make UX, better card graphics & animations?
    - damn: [chafapy](https://chafapy.mage.black/usage/tutorial.html)
