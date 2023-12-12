from abc import ABC, abstractmethod

class GameState:
    def __init__(self, turn, white_workers, blue_workers, grid):
        self._turn = turn
        self._white_workers = white_workers
        self._blue_workers = blue_workers
        self._grid = grid
    
    @property
    def turn(self):
        return self._turn

    @property
    def white_workers(self):
        return self._white_workers
    
    @property
    def blue_workers(self):
        return self._blue_workers
    
    @property
    def grid(self):
        return self._grid
    
    @turn.setter
    def turn(self, turn):
        self._turn = turn
    
    @white_workers.setter
    def white_workers(self, white_workers):
        self._white_workers = white_workers
    
    @blue_workers.setter
    def blue_workers(self, blue_workers):
        self._blue_workers = blue_workers

    @grid.setter
    def grid(self, grid):
        self._grid = grid

    ############################################
    ## Deep Copy for Memento & Possible Moves ##
    ############################################
    
    def get_worker_by_symbol(self, symbol):
        for worker in self._white_workers:
            if worker.symbol == symbol:
                return worker
        for worker in self._blue_workers:
            if worker.symbol == symbol:
                return worker

        return None 
    
    def get_workers_pos_by_symbol(self, symbol):
        matching_workers = []
        
        for worker in self._white_workers:
            if worker.symbol == symbol:
                matching_workers.append(worker.position)
        
        for worker in self._blue_workers:
            if worker.symbol == symbol:
                matching_workers.append(worker.position)

        return matching_workers
    
    def get_worker_by_position(self, position):
        for worker in self._white_workers:
            if worker.position == position:
                return worker
        for worker in self._blue_workers:
            if worker.position == position:
                return worker

        return None

class Memento(ABC):
    """
    The Memento interface provides a way to retrieve the memento's metadata,
    such as creation date or name. However, it doesn't expose the Originator's
    state.
    """

    @abstractmethod
    def get_turn(self) -> int:
        pass

    @abstractmethod
    def get_white_workers(self) -> list:
        pass

    @abstractmethod
    def get_blue_workers(self) -> list:
        pass

class Originator:
    # here create a functional to save the game state maybe dictionary
    """
    The Originator holds some important state that may change over time. It also
    defines a method for saving the state inside a memento and another method
    for restoring the state from it.
    """

    _state = None
    """
    For the sake of simplicity, the originator's state is stored inside a single
    variable.
    """

    def __init__(self, state: object) -> None:
        self._state = state
        print(f"Originator: My initial state is: {self._state}")

    def generate_game_state(self, turn, white_pos, blue_pos, grid) -> GameState:
        """
        The Originator's business logic may affect its internal state.
        Therefore, the client should backup the state before launching methods
        of the business logic via the save() method.
        """

        print("Originator: I'm doing something important.")
        self._state = GameState(turn, white_pos, blue_pos, grid)
        print(f"Originator: and my state has changed to: {self._state}")
        return self._state

    def save(self) -> Memento:
        """
        Saves the current state inside a memento.
        """

        return ConcreteMemento(self._state)

    def restore(self, memento: Memento) -> None:
        """
        Restores the Originator's state from a memento object.
        """

        self._state = memento.get_state()
        print(f"Originator: My state has changed to: {self._state}")

    @property
    def state(self):
        return self._state


class ConcreteMemento(Memento):
    def __init__(self, state: GameState) -> None:
        self._state = state

    def get_state(self) -> GameState:
        return self._state
    
    def get_turn(self) -> int:
        return self._state.turn

    def get_white_workers(self) -> list:
        return self._state.white_workers

    def get_blue_workers(self) -> list:
        return self._state.blue_workers

class Caretaker:
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento. It
    works with all mementos via the base Memento interface.
    """

    def __init__(self, originator: Originator) -> None:
        self._mementos = []
        self._undone_mementos = []
        self._originator = originator

    def backup(self) -> None:
        print("Caretaker: Saving Originator's state...")
        self._mementos.append(self._originator.save())
        self._undone_mementos = []

    def undo(self) -> None:
        if not len(self._mementos):
            return

        memento = self._mementos.pop()
        print(f"Caretaker: Restoring state to: {memento.get_turn()}")
        # try:
        self._originator.restore(memento)
        self._undone_mementos.append(memento)
        # except Exception:
        #     self.undo()

    def redo(self) -> None:
        if not self._undone_mementos:
            return

        memento = self._undone_mementos.pop()
        print(f"Caretaker: Redoing to: {memento.get_turn()}")
        try:
            self._originator.restore(memento)
            self._mementos.append(memento)
        except Exception:
            self.redo()

    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print("Blue Workers:", memento.get_blue_workers())
            print("White Workers:", memento.get_white_workers())

