import random
import stackables as stk
import environment as env
import event

'''

'''


class Char(object):
    def __init__(self):
        self.energy = 0
        self.max_items = 20
        self.statuses = []
        self.items = []
        self.magic = []
        self.name = input('What was your name again? ')
        self.light_radius = 3
        self.world_size = 16
        spawn_loc = [random.randint(0, self.world_size-1) for i in range(6)]
        self.world = env.World(18005882300, self, self.world_size)
        self.biome = self.world.get_biome(spawn_loc[0], spawn_loc[1])
        self.chunk = self.biome.get_chunk(spawn_loc[2], spawn_loc[3])
        self.tile = self.chunk.get_tile(spawn_loc[4], spawn_loc[5])
        for place in [self.world, self.biome, self.chunk, self.tile]:
            place.contents += [self]
        self.get_nearby_tiles()

    def get_nearby_tiles(self):
        x = self.tile.x
        y = self.tile.y
        for tile in env.in_radius(x, y, self.light_radius,
                                  self.chunk.size):
            self.chunk.get_tile(*tile)

    def show_chunk_map(self):
        self.chunk.char_map()
        return

    def north(self):
        tile_x = self.tile.x
        tile_y = self.tile.y
        if tile_y == 0:
            chunk_x = self.chunk.x
            chunk_y = self.chunk.y
            if chunk_y == 0:
                biome_x = self.biome.x
                biome_y = self.biome.y
                if biome_y == 0:
                    return
                self.biome.contents.remove(self)
                self.biome = self.world.get_biome(biome_x, (biome_y-1)%self.world.size)
                self.biome.contents += [self]
            self.chunk.contents.remove(self)
            self.chunk = self.biome.get_chunk(chunk_x, (chunk_y-1)%self.biome.size)
            self.chunk.contents += [self]
        self.tile.contents.remove(self)
        self.tile = self.chunk.get_tile(tile_x, (tile_y-1)%self.chunk.size)
        self.tile.contents += [self]
        self.get_nearby_tiles()
        self.show_chunk_map()

    def south(self):
        tile_x = self.tile.x
        tile_y = self.tile.y
        if tile_y == self.chunk.size-1:
            chunk_x = self.chunk.x
            chunk_y = self.chunk.y
            if chunk_y == self.biome.size-1:
                biome_x = self.biome.x
                biome_y = self.biome.y
                if biome_y == self.world.size-1:
                    return
                self.biome.contents.remove(self)
                self.biome = self.world.get_biome(biome_x, (biome_y+1)%self.world.size)
                self.biome.contents += [self]
            self.chunk.contents.remove(self)
            self.chunk = self.biome.get_chunk(chunk_x, (chunk_y+1)%self.biome.size)
            self.chunk.contents += [self]
        self.tile.contents.remove(self)
        self.tile = self.chunk.get_tile(tile_x, (tile_y+1)%self.chunk.size)
        self.tile.contents += [self]
        self.get_nearby_tiles()
        self.show_chunk_map()

    def east(self):
        tile_x = self.tile.x
        tile_y = self.tile.y
        if tile_x == self.chunk.size-1:
            chunk_x = self.chunk.x
            chunk_y = self.chunk.y
            if chunk_x == self.biome.size-1:
                biome_x = self.biome.x
                biome_y = self.biome.y
                if biome_y == self.world.size-1:
                    return
                self.biome.contents.remove(self)
                self.biome = self.world.get_biome((biome_x+1)%self.world.size, biome_y)
                self.biome.contents += [self]
            self.chunk.contents.remove(self)
            self.chunk = self.biome.get_chunk((chunk_x+1)%self.biome.size, chunk_y)
            self.chunk.contents += [self]
        self.tile.contents.remove(self)
        self.tile = self.chunk.get_tile((tile_x+1)%self.chunk.size, tile_y)
        self.tile.contents += [self]
        self.get_nearby_tiles()
        self.show_chunk_map()

    def west(self):
        tile_x = self.tile.x
        tile_y = self.tile.y
        if tile_x == 0:
            chunk_x = self.chunk.x
            chunk_y = self.chunk.y
            if chunk_x == 0:
                biome_x = self.biome.x
                biome_y = self.biome.y
                if biome_x == 0:
                    return
                self.biome.contents.remove(self)
                self.biome = self.world.get_biome((biome_x-1)%self.world.size, biome_y)
                self.biome.contents += [self]
            self.chunk.contents.remove(self)
            self.chunk = self.biome.get_chunk((chunk_x-1)%self.biome.size, chunk_y)
            self.chunk.contents += [self]
        self.tile.contents.remove(self)
        self.tile = self.chunk.get_tile((tile_x-1)%self.chunk.size, tile_y)
        self.tile.contents += [self]
        self.get_nearby_tiles()
        self.show_chunk_map()

    def move(self, direction):
        current_str_type = self.tile.type
        if direction == 'n':
            self.north()
        elif direction == 'w':
            self.west()
        elif direction == 's':
            self.south()
        elif direction == 'e':
            self.east()
        if self.tile.new:
            self.tile.new = False
            event.Combat(self, self.tile).trigger()
        if self.tile.type == current_str_type:
            pass


    # def set_position(self, x, y):
        # self.position = (x, y)

    def rename(self):
        self.name = input('You feel dizzy... What was your name again? ')

    def adjust_energy(self, delta):
        """Positive or negative change in
        energy."""
        self.energy += delta

    def gain_status(self, status):
        for ind in range(len(self.statuses)):
            if type(self.statuses[ind]) == type(status):
                self.statuses[ind] += status
                return None
        self.statuses += [status]

    def gain_item(self, item):
        if len(self.items) >= self.max_items:
            print(f'You cannot pick up {item} because'
                  f'you are carrying too many items.')
            return None
        if stk.Material in type(item).__bases__:
            for ind in range(len(self.items)):
                current = self.items[ind]
                if current.name == item.name:
                    self.items = self.items[:ind] + (current + item) + self.items[ind + 1:]
                    return None
            self.items += [item]
        if isinstance(item, stk.Unique):
            self.items += [item]

    def gain_magic(self, magic):
        self.magic += [magic]


if __name__ == '__main__':
    print('To move, in the prompt, type "w" for north, "s" for south, '
          '\n"a" for west, or "d" for east, followed by "Enter". ')
    a = Char()
    print('Now press "w", "s", "a", or "d".')
    while True:
        command = input()
        if command == 'w':
            a.north()
        elif command == 's':
            a.south()
        elif command == 'a':
            a.west()
        elif command == 'd':
            a.east()
        else:
            print('Command not recognized yet!')