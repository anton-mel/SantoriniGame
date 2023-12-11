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

    @staticmethod
    def get_direction(delta):
        delta_dict = {
            (-1, 0): "n",
            (-1, 1): "ne",
            (0, 1): "e",
            (1, 1): "se",
            (1, 0): "s",
            (1, -1): "sw",
            (0, -1): "w",
            (-1, -1): "nw",
        }

        try:
            return delta_dict[delta]
        except Exception:
            print("hi")

    def calculate_direction(original, new):
        delta = (new[0] - original[0], new[1] - original[1])

        return DirectionUtils.get_direction(delta)

    @staticmethod
    def move_result(current, direction):
        delta = DirectionUtils.get_direction_delta(direction)
        new_position = (current[0] + delta[0], current[1] + delta[1])
        return new_position
