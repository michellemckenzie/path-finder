# rush-hour-with-artificial-intelligence

# Background Info

The puzzle called "Rush Hour" begins with a six-by-six grid of squares. Little plastic cars and trucks are distributed across the grid in such a way as to prevent one special car from moving off the grid, thereby escaping the traffic jam. The initial configuration of cars and trucks is preordained by a set of cards, each containing a different starting pattern.

Cars occupy two contiguous squares, while trucks occupy three contiguous squares. All vehicles are oriented horizontally or vertically, never on the diagonal. Vehicles that are oriented horizontally may only move horizontally; vehicles that are oriented vertically may only move vertically. Vehicles may not be lifted from the grid, and there is never any diagonal movement. Vehicles may not be partially on the grid and partially off the grid.

The special car is called the X car. We'll represent it on the grid as two contiguous squares with the letter X in them. (We'll represent all other cars and trucks with different letters of the alphabet, but the special car will always be labeled with the letter X.) The X car is always oriented horizontally on the third row from the top; otherwise, the X car could never escape.

The goal state is any configuration of cars and trucks that can be obtained through correct application of the operators, such that the X car covers the rightmost two squares of the third row from the top
