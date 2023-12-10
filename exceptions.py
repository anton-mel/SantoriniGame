class MoveError(Exception):
    """Fix later"""

    def __init__(self, move_type, direction):
        super().__init__()
        self.move_type = move_type
        self.direction = direction

