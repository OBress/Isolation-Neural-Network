


class Player:
    def __init__(self, name, number, pos):
        self.name = name
        self.number = number
        self.moves = 0
        # (row, col)
        self.pos = pos