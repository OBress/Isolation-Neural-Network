# Isolation-Neural-Network
The game of Isolation is a game in which you are on a 9x9 grid where each of the 2 players are on a grid. Every time a player moves, the sqaure it was on becomes solid and can no longer move. Players can move like a queen in chess. The winning player is the player who can move last.

The neat algorithm seems to have difficulty with the number of possible states in the game making it learn very inefficiently. It was also hard to try and make it not output illegal moves. Overall, didn't have much success yet with isolation and had more success with optimized alpha beta + flood search.
