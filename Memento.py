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
    def get_grid(self) -> int:
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

    def generate(self, game_state) -> GameState:
        """
        The Originator's business logic may affect its internal state.
        Therefore, the client should backup the state before launching methods
        of the business logic via the save() method.
        """

        self._state = game_state
        return self.save()

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


class ConcreteMemento(Memento):
    def __init__(self, state: GameState) -> None:
        self._state = state

    def get_state(self) -> GameState:
        return self._state
    
    def get_turn(self) -> int:
        return int(self._state.turn)
    
    def get_grid(self) -> list:
        return self._state.grid

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

        # Save Current Originator State
        current_state = self._originator.save()
        # If not yet appended, then append and update
        if current_state not in self._mementos:
            self._mementos.append(current_state)
            self._undone_mementos = []

        print(len(self._mementos))
        print(len(self._undone_mementos))

    def undo(self) -> None:
        print("before",len(self._mementos))
        print("before",len(self._undone_mementos))

        # Obtain Latest Momento from the list
        originator_state = self._originator.save()
        memento = self._mementos.pop()
        # Impornt: check after pop()
        if not self._mementos:
            self._mementos.append(originator_state)
            self._originator.restore(memento)
            return
        
        # First preserve the current originator state
        self._undone_mementos.append(self._originator.save())
        # Restore to the originator to display it
        self._originator.restore(memento)

        print(len(self._mementos))
        print(len(self._undone_mementos))

    def redo(self) -> None:
        
        if not len(self._undone_mementos):
            return
        print("before",len(self._mementos))
        print("before",len(self._undone_mementos))
        
        originator_state = self._originator.save()
        memento = self._undone_mementos.pop()
        if not self._undone_mementos:
            self._undone_mementos.append(originator_state)
            self._originator.restore(memento)
            return
        # Restore to the originator to display it
        self._originator.restore(memento)

        # if len(self._undone_mementos) > 0:
        #     self._mementos.append(memento)

        print(len(self._mementos))
        print(len(self._undone_mementos))

    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print("Blue Workers:", memento.get_blue_workers())
            print("White Workers:", memento.get_white_workers())

