# wyjątek złego ruchu tzn. próba wykonania ruchu niedozwolonego
class BadMoveExceptions(Exception):
    def __init__(self):
        self.message = f'bad move'


# wyjątek kliknięcia poza planszę do gry ale w oknie samej gry
class OutsideBoardExceptions(Exception):
    def __init__(self):
        self.message = f'outside board exce'
