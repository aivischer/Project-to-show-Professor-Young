import char_build, text


class Event(object):
    pass


class TownEvent(Event):
    pass


class CryptEvent(Event):
    pass



class Combat(object):

    def __init__(self, character, tile):
        self.char = character
        self.tile = tile

    def trigger(self):
        pass