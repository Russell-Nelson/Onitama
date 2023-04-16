# Onitama
A digital implementation of the chess-like board game Onitama with an AI opponent.

Onitama is a simple game with very rewarding depth. Rules for how to play the game can be found [here](https://www.ultraboardgames.com/onitama/game-rules.php).

## Display
The game runs in the terminal against an AI opponent as the blue player. Run main.py in the terminal and it will print out an initial board state similar to the 
following:

\          -----     -----
\          -x-x-     -----             
\          --o--     -xox-  <-(The blue player's starting hand of two random cards. An "o" is a position of a piece to move and an "x" is a position to move to.)         
 \         x---x     --x--                
 \         -----     -----                
\          _______________                
\         | b  b  B  b  b |  <-(This is the top of the board and the blue pieces. "B" for the blue master pawn and "b" for regular blue pawns.)            
\         |               |               
 -----   | -  -  -  -  - |   -----       
 -----   |               |   -x-x-       
 -----   | -  -  -  -  - |   --o--  <-(Cards move clockwise around the board. So this card will be added to the red player's hand after their next move.)
 -----   |               |   --x--
 -----   | -  -  -  -  - |   -----
\         |               |
\         | r  r  R  r  r |  <-(This is the bottom of the board and the red pieces. "R" for the red master pawn and "r" for the regular red pawns.)
\          _______________
\          -----     -----
\          ---x-     -x---
\          -xo--     x-o--  <-(The red player's starting hand of two random cards)
\          ---x-     ---x-
\          -----     -----

## Input
You will be prompted for input on your turns. At the moment, the formatting for input is rather clunky.

One example of a valid input for the boardstate above would be (4,2)L(3,3)

The first pair of numbers, (4,2), represents the location of the piece that you would like to move. "4" indicates the row (zero indexed) and "2" indicates the
column (also zero indexed). So (4,2) indicates the red master pawn ("R") in the above game.

The middle letter of the input can be either "L" or "R". This indicates whether you would like to use the movement card on the left hand side of your player area 
or the movement card on the right hand side of your play area. In the above example, "L" indicates that the following movement card will be used by the red player:
-----
---x-
-xo--
---x-
-----

Finally, the second pair of numbers, (3,3), represents the location that the piece will move to. This location must be a legal move for the combination of piece
and card chosen. If you enter an illegal move or improper formatting, then the game will re-prompt you for input.


## The Blue Opponent
The AI opponent uses a depth-limited minimax algorithm with alpha-beta pruning. At the moment it runs to a depth of 4 and uses just about the most simple 
evaluation function possible. It is boring in the early game, but becomes surprisingly good once pieces are within range to interact. My plan for developing this
project further is to make better evaluation functions, test them by playing bots against each other, and maybe include different playstyles as options for setting
up a game.

