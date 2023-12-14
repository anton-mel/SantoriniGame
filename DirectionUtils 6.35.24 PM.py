class DirectionUtils:
    @staticmethod
    def get_direction_delta(direction):
        direction_deltas = {
            "n": (-1, 0),
            "ne": (-1, 1),
            "e": (0, 1),
            "se": (1, 1),
            "s": (1, 0),
            "sw": (1, -1),
            "w": (0, -1),
            "nw": (-1, -1),
        }
        return direction_deltas[direction]

