
class Worker:
    """Class representing a worker."""

    def __init__(self, symbol, default_position):
        self.symbol = symbol
        self.position = default_position

    @property
    def get_symbol(self):
        return self.symbol


class Player:
    """Class representing a player."""

    def __init__(self, color, workers):
        self.color = color
        self.workers = workers

    @property
    def get_workers(self):
        return self.workers
    
    @property
    def get_color(self):
        return self.color

class WhitePlayer(Player):
    """Class representing the White player."""

    def __init__(self):
        workers = [Worker('A', (3, 1)), Worker('B', (3, 3))]
        super().__init__('white', workers)

class BluePlayer(Player):
    """Class representing the Blue player."""

    def __init__(self):
        workers = [Worker('Y', (1, 2)), Worker('Z', (1, 4))]
        super().__init__('blue', workers)


# Here Memento Pattern
class Command:
    """Class representing a player move."""

    def __init__(self):
        pass

    def execute_command():
        raise NotImplemented
        # make poly on other commands


class SantoriniGame:
    """Class representing the Santorini game."""

    def __init__(self, players):
        self._players = players
        self._board = Board(self._players[0], players[1])
        self._current = self._players[0]
        self._turn = 1
    
    def _next(self):
        self._current = self._players[self._turn % 2]
        self._turn += 1

    def print_board(self):
        print(f"Turn: {self._turn}, {self._current.get_color} ({[worker[0] for worker in self._current.get_workers]})")
        self._board.print_board()

    # Memento (Another Class)
    def execute_command(self, m, d, b, command):
        # Execute Command With MDB Data
        self._next() # next player

    @property
    def get_current_player(self):
        return self._currentxww
    

class Board:
    """Class representing the Santorini Board."""

    def __init__(self, white, blue):
        self._grid = [[(0, []) for _ in range(5)] for _ in range(5)]

        self._add_workers_to_cell(3, 1, white.get_workers[0])
        self._add_workers_to_cell(1, 3, white.get_workers[1])
        self._add_workers_to_cell(1, 1, blue.get_workers[0])
        self._add_workers_to_cell(3, 3, blue.get_workers[1])

    def print_board(self):
        """Print the board."""
        for row in range(5):
            print("+--+--+--+--+--+")
            for col in range(5):
                height, workers = self._grid[row][col]
                print(f"|{height}{workers[0] if workers else ' '}", end="")

            print("|")
        print("+--+--+--+--+--+")

    def _add_workers_to_cell(self, row, col, workers):
        """Add workers to the cell."""
        self._grid[row][col] = (0, workers)



#########################################
########### Factory Method ##############

class PlayerFactory:
    @staticmethod
    def get_factory(player_type):
        if player_type == "human":
            return HumanPlayerFactory()
        elif player_type == "heuristic":
            return HeuristicPlayerFactory()
        else:
            raise ValueError("Invalid player type")


class HumanPlayerFactory(PlayerFactory):
    def create_player(self, color, workers):
        return HumanPlayer(color, workers)


class HeuristicPlayerFactory(PlayerFactory):
    def create_player(self, color, workers):
        return HeuristicPlayer(color, workers)


class HumanPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)


class HeuristicPlayer(Player):
    def __init__(self, color, workers):
        super().__init__(color, workers)