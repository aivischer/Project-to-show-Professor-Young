import char_build as char
import random as rand
import display
from colorama import *
'''
Need to specify the size of World, Biomes, and Chunks.

'''


# ---------------------------------------------------------
# Analysis of tiles on map


def adjacent(x, y, size):
    return [((x+1)%size, y),
            ((x-1)%size, y),
            (x, (y+1)%size),
            (x, (y-1)%size)]


def adj_or_diag(x,y, size):
    return [((x+1)%size, y),
            ((x+1)%size, (y+1)%size),
            ((x+1)%size, (y-1)%size),
            (x, (y+1)%size),
            (x, (y-1)%size),
            ((x-1)%size, y),
            ((x-1)%size, (y+1)%size),
            ((x-1)%size, (y-1)%size)]


def in_radius(x, y, radius, size):
    in_rad = [(x, y)]
    outside = [(x, y)]
    for circle in range(radius):
        current = []
        for tile in outside:
            for adj in adj_or_diag(*tile, size):
                if adj not in in_rad and adj not in current:
                    adj_x = adj[0]
                    adj_y = adj[1]
                    dx = abs(x-adj_x)
                    dy = abs(y-adj_y)
                    if (dx**2+dy**2)**.5 <= radius:
                        current += [adj]
        outside = current
        in_rad += outside
    return in_rad


str_dict = {'ocean': Fore.CYAN + Back.BLUE + '_',
            'forest': Fore.GREEN + 'T',
            'mountain': Fore.LIGHTRED_EX + 'A',
            'crypt': Fore.BLACK + Style.BRIGHT + '=',
            'crypt_mid': Fore.GREEN + Style.BRIGHT + '∩',
            'town': Fore.WHITE + Style.BRIGHT + 'H',
            'town_mid': Fore.BLACK + Style.BRIGHT + '=',
            'plains': Fore.GREEN + '.'}


class Structure(object):
    """Composed of tiles, has different
    qualities based on the type of structure
    it is.
    Ocean: ____
    Forest: TTTT
    Mountain: AAAA
    Crypt: =∩=
    Town: H=H
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Structure({self.name})'


# ------------------------------------------------------------
# Tile section


class Tile(object):
    """The smallest unit available for a player
    to traverse. May contain enemies and whatnot."""
    def __init__(self, x_pos, y_pos, character, seed, chunk,
                 str_type=Structure('plains')):
        rand.seed(seed)
        self.x = x_pos
        self.y = y_pos
        self.new = True
        self.chunk = chunk
        self.contents = []
        self.char = character
        self.type = str_type

    def add_contents(self, obj):
        self.contents += [obj]


class Chunk(object):
    """A chunk is composed of tiles, and determines what
    structures appear on those tiles."""

    def __init__(self, x_pos, y_pos, size, character, seed, biome,
                 str_settings=(4, 4, 4, 4, 4, 4)):
        rand.seed(seed)
        self.x = x_pos
        self.y = y_pos
        self.biome = biome
        self.size = size
        self.char = character
        self.contents = []
        self.tile_seeds = {}
        self.tiles = {}
        for x in range(self.size):
            for y in range(self.size):
                self.tile_seeds[(x, y)] = rand.random()
        self.structures = {(x, y): Structure('plains')
                           for x in range(self.size)
                           for y in range(self.size)}
        self.propagate_all(*str_settings)

# Tile propagation

    def propagate_ocean(self, num, o_size):
        """Propagates before mountains."""
        oceans = rand.randint(0, num)
        if oceans == 0:
            return
        for ocean in range(oceans):
            start = (rand.randint(0, self.size - 1), rand.randint(0, self.size - 1))
            self.structures[start].name = 'ocean'
            ocean_current = [start]
            for rep in range(o_size):
                new_oceans = []
                for parent in ocean_current:
                    for child in adjacent(*parent, self.size):
                        if child in ocean_current:
                            continue
                        chance = rand.randint(0,1)
                        if chance:
                            self.structures[child].name = 'ocean'
                            new_oceans += [child]
                ocean_current += new_oceans

    def propagate_mountain(self, num, m_size):
        """Same as propagate_forest, except can
        spread along diagonals. Propagates before
        forests.
        """
        mountains = rand.randint(0, num)
        if mountains == 0:
            return
        for mountain in range(mountains):
            start = (rand.randint(0, self.size - 1), rand.randint(0, self.size - 1))
            self.structures[start].name = 'mountain'
            mountain_current = [start]
            for rep in range(m_size):
                new_mountains = []
                for parent in mountain_current:
                    for child in adj_or_diag(*parent, self.size):
                        if child in mountain_current:
                            continue
                        chance = rand.randint(0, 3)
                        if chance == 3:
                            if self.structures[child].name == 'ocean':
                                continue
                            self.structures[child].name = 'mountain'
                            new_mountains += [child]
                mountain_current += new_mountains

    def propagate_forest(self, num, f_size):
        """
        Propagates the forest structures in a chunk;
        num is the maximum number of forests. Size is
        the number of times to increase the size of
        the forest.
        """
        forests = rand.randint(0, num)
        if forests == 0:
            return
        for forest in range(forests):
            start = (rand.randint(0, self.size - 1), rand.randint(0, self.size - 1))
            self.structures[start].name = 'forest'
            forest_current = [start]
            for rep in range(f_size):
                new_forests = []
                for parent in forest_current:
                    for child in adjacent(*parent, self.size):
                        if child in forest_current:
                            continue
                        chance = rand.randint(0, 1)
                        if chance:
                            if self.structures[child].name == 'mountain':
                                continue
                            if self.structures[child].name == 'ocean':
                                continue
                            self.structures[child].name = 'forest'
                            new_forests += [child]
                forest_current += new_forests

    def add_towns(self):
        towns = rand.randint(0, 1)
        if towns == 0:
            return
        new_town = (rand.randint(0, self.size - 2), rand.randint(0, self.size-1))
        self.structures[new_town].name = 'town'
        tile_adj = (new_town[0] + 1, new_town[1])
        self.structures[tile_adj].name = 'town'

    def add_crypts(self):
        chance = rand.randint(1, 10)
        if chance < 10:
            return
        new_crypt = (rand.randint(0, self.size - 2), rand.randint(0, self.size-1))
        if self.structures[new_crypt].name == 'town':
            new_crypt = (new_crypt[0], (new_crypt[1] - 1) % self.size)
        self.structures[new_crypt].name = 'crypt'
        tile_adj = (new_crypt[0] + 1, new_crypt[1])
        self.structures[tile_adj].name = 'crypt'

    def propagate_all(self, ocean_num, o_size,
                      forest_num, forest_size,
                      mountain_num, mount_size):
        self.propagate_ocean(ocean_num, o_size)
        self.propagate_mountain(mountain_num, mount_size)
        self.propagate_forest(forest_num, forest_size)
        self.add_towns()
        self.add_crypts()

    def add_contents(self, obj):
        self.contents += [obj]

# The rest of the tile methods

    def add_tile(self, x, y, size=None):
        if size is None:
            size = self.size
        self.tiles[(x, y)] = Tile(x, y, self.char, self.tile_seeds[(x, y)], self,
                                  self.structures[(x, y)])

    def get_tile(self, x, y, size=None):
        if (x, y) in self.tiles:
            return self.tiles[(x, y)]
        if size is None:
            size = self.size
        tile = Tile(x, y, self.char, self.tile_seeds[(x, y)], self,
                    self.structures[(x, y)])
        self.tiles[(x, y)] = tile
        return tile

    def structures_matrix(self):
        matrix = [[] for i in range(self.size)]
        for key in self.structures:
            matrix[key[1]] += [str_dict[self.structures[key].name]]
        return matrix

    def char_map_matrix(self):
        matrix = [[Fore.BLACK + 'e'] * self.size for i in range(self.size)]
        for key in self.tiles:
            matrix[key[1]][key[0]] = str_dict[self.tiles[key].type.name]
            if self.char in self.tiles[key].contents:
                matrix[key[1]][key[0]] = Fore.RESET + 'o'
        return matrix

    def map(self, matrix):
        for row in matrix:
            for ind in range(1, 2 * len(row)-1, 2):
                if row[ind-1] == str_dict['mountain'] and row[ind] == str_dict['mountain']:
                    row.insert(ind, str_dict['mountain'])
                elif row[ind-1] == str_dict['ocean'] and row[ind] == str_dict['ocean']:
                    row.insert(ind, str_dict['ocean'])
                elif row[ind-1] == str_dict['forest'] and row[ind] == str_dict['forest']:
                    row.insert(ind, str_dict['forest'])
                elif row[ind-1] == str_dict['town'] and row[ind] == str_dict['town']:
                    row.insert(ind, str_dict['town_mid'])
                elif row[ind-1] == str_dict['crypt'] and row[ind] == str_dict['crypt']:
                    row.insert(ind, str_dict['crypt_mid'])
                else:
                    row.insert(ind, ' ')
        print(display.Map(matrix))
        return

    def char_map(self):
        self.map(self.char_map_matrix())
        return


# -------------------------------------------------------------
# Biome section


class Biome(object):
    """A biome determines a common set of features
    between each of its components, chunks."""
    def __init__(self, x_pos, y_pos, size, character, seed, world):
        rand.seed(seed)
        self.x = x_pos
        self.y = y_pos
        self.new = True
        self.world = world
        self.size = size
        self.contents = []
        self.char = character
        self.chunk_seeds = {}
        self.chunks = {}
        for x in range(self.size):
            for y in range(self.size):
                self.chunk_seeds[(x, y)] = rand.random()

    def add_contents(self, obj):
        self.contents += [obj]

    def add_chunk(self, x, y, size=None):
        if size is None:
            size = self.size
        self.chunks[(x, y)] = Chunk(x, y, size, self.char,
                                    self.chunk_seeds[(x, y)], self)

    def get_chunk(self, x, y, size=None):
        """Searches biome for specifed chunk and
        creates a chunk at that location if one
        is not found."""
        if (x, y) in self.chunks:
            return self.chunks[(x, y)]
        if size is None:
            size = self.size
        chunk = Chunk(x, y, size, self.char, self.chunk_seeds[(x, y)], self)
        self.chunks[(x, y)] = chunk
        return chunk


# --------------------------------------------------------------
# World section


class World(object):
    """A world is composed of biomes."""
    def __init__(self, seed, character, size=10):
        rand.seed(seed)
        self.size = size
        self.new = True
        self.contents = []
        self.char = character
        self.biome_seeds = {}
        for x in range(self.size):
            for y in range(self.size):
                self.biome_seeds[(x, y)] = rand.random()
        self.biomes = {}

    def add_contents(self, obj):
        self.contents += [obj]

    def add_biome(self, x, y, size=None):
        if size is None:
            size = self.size
        self.biomes[(x, y)] = Biome(x, y, size, self.char,
                                    self.biome_seeds[(x, y)], self)

    def get_biome(self, x, y, size=None):
        """Searches for the biome at x, y
        and creates a new biome with specified size if
        biome is not found at given position."""
        if (x, y) in self.biomes:
            return self.biomes[(x, y)]
        if size is None:
            size = self.size
        biome = Biome(x, y, self.size, self.char, self.biome_seeds[(x, y)], self)
        self.biomes[(x, y)] = biome
        return biome

