# SantoriniGame
OOP Based Santorini Game CLI

just leave your ideas here, or message me

# ChatGPT UML idea + Folder Structure:

Game.py:

# Game
Board.py:

# Board
Cell
Position
Player.py:

# Player
Worker
Move.py:

# Move
Direction
History.py:

# History
CommandPattern.py:

# Game Class:

Responsibilities:

Manages the game state.
Controls the flow of the game.
Interacts with players.
Attributes:

board: Board - Represents the game board.
players: List[Player] - Stores the players in the game.
currentPlayer: Player - Tracks the current player.
Methods:

startGame()
playTurn()
checkWinCondition()

# Board Class:

Responsibilities:

Represents the game board.
Manages the state of the grid.
Attributes:

grid: List[List[Cell]] - Represents the 5x5 grid.
Methods:

placeWorker(worker: Worker, position: Position)
moveWorker(worker: Worker, direction: Direction)
buildLevel(worker: Worker, direction: Direction)
isMoveValid(worker: Worker, direction: Direction)

# Player Class:

Responsibilities:

Represents a player in the game.
Holds the workers controlled by the player.
Attributes:

color: Color - Represents the player's color.
workers: List[Worker] - Stores the workers controlled by the player.
Methods:

selectWorker()
makeMove(worker: Worker, move: Move)
chooseBuildDirection()

# Worker Class (Player):

Responsibilities:

Represents a worker on the board.
Attributes:

position: Position - Represents the worker's current position on the board.
player: Player - Represents the player who owns the worker.
Methods:

move(direction: Direction)
build(direction: Direction)

# Cell Class:

Responsibilities:

Represents a cell on the game board.
Attributes:

level: int - Represents the level of the building on the cell.
worker: Worker - Represents the worker on the cell.

# Position Class:

Responsibilities:

Represents a position on the game board.
Attributes:

row: int
column: int

# Direction Enum:

Represents the cardinal directions for movement and building.

# Move Class:

Responsibilities:
Represents a player's move.
Encapsulates the information about which worker to move, the direction to move, and the direction to build.

# History Class (Part of the Pattern) and 
# Command Pattern (not a class, but a pattern):
Originator, Caretaker, Command

