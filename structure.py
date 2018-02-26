from colorama import *


# --------------------------------------------
# Color dictionaries


clear = (Fore.RESET + Style.RESET_ALL + Back.RESET + '')


fore_colors = {'red': Fore.RED, 'light_red': Fore.LIGHTRED_EX,
               'blue': Fore.BLUE, 'light_blue': Fore.LIGHTBLUE_EX,
               'cyan': Fore.CYAN, 'light_cyan': Fore.LIGHTCYAN_EX,
               'green': Fore.GREEN, 'light_green': Fore.LIGHTGREEN_EX,
               'yellow': Fore.YELLOW, 'light_yellow': Fore.LIGHTYELLOW_EX,
               'magenta': Fore.MAGENTA, 'light_magenta': Fore.LIGHTMAGENTA_EX,
               'black': Fore.WHITE, 'light_white': Fore. LIGHTWHITE_EX,
               'white': Fore.BLACK, 'light_black': Fore.LIGHTBLACK_EX,
               'reset': Fore.RESET}


back_colors = {'red': Back.RED, 'light_red': Back.LIGHTRED_EX,
               'blue': Back.BLUE, 'light_blue': Back.LIGHTBLUE_EX,
               'cyan': Back.CYAN, 'light_cyan': Back.LIGHTCYAN_EX,
               'green': Back.GREEN, 'light_green': Back.LIGHTGREEN_EX,
               'yellow': Back.YELLOW, 'light_yellow': Back.LIGHTYELLOW_EX,
               'magenta': Back.MAGENTA, 'light_magenta': Back.LIGHTMAGENTA_EX,
               'black': Back.WHITE, 'light_white': Back. LIGHTWHITE_EX,
               'white': Back.BLACK, 'light_black': Back.LIGHTBLACK_EX,
               'reset': Back.RESET}


color_styles = {'bright': Style. BRIGHT, 'normal': Style.NORMAL,
                'dim': Style.DIM, 'reset': Style.RESET_ALL}


# --------------------------------------------
# Images


class Image(object):
    def __init__(self, letter=' ', back='reset', fore='reset', style='reset'):
        self.letter = letter
        self.back = back_colors[back]
        self.fore = fore_colors[fore]
        self.style = color_styles[style]

    def __str__(self):
        return self.back + self.fore + self.style + self.letter + clear

    def __repr__(self):
        return self.back + self.fore + self.style + self.letter + clear

    def __add__(self, other):
        return str(self) + str(other)

    def __eq__(self, other):
        return ((self.letter == other.letter) and
                (self.back == other.back) and
                (self.fore == other.fore) and
                (self.style == other.style))

    def set_back(self, color):
        self.back = back_colors[color]

    def set_fore(self, color):
        self.fore = fore_colors[color]

    def set_style(self, style):
        self.style = color_styles[style]

    def set_letter(self, letter):
        self.letter = letter


# --------------------------------------------
# Structures


class Structure(object):

    def __init__(self, priority, image=Image()):
        self.image = image
        self.priority = priority

    def __repr__(self):
        return f'Structure({self.priority}, {self.image})'

    def __str__(self):
        """
        Every structure has a different
        str() representation; used for
        making the map.
        """
        return self.image

    def __add__(self, other):
        return str(self) + str(other)

    def __eq__(self, other):
        return ((self.priority == other.priority) and
                (self.image == other.letter))

    def __hash__(self):
        return hash(id(self))


class Floor(object):
    def __init__(self, priority, image=Image()):
        self.priority = priority
        self.image = image

    def __repr__(self):
        return f'Floor({self.image})'

    def __str__(self):
        return

    def __eq__(self, other):
        return ((self.priority == other.priority) and
                (self.image == other.image))


# -------------------------------------------------------
# Tools for combining images


def tile_image(floor, structure):
    """Takes two input images and returns the back
    of one, plus the fore of the other."""
    return Image(back=floor.back if structure.back == 'reset' else structure.back,
                 letter=structure.letter, fore=structure.fore, style=structure.style)


# ------------------------------------------------------
# Structure list and extension


structures = {'void_floor': Floor(0),
              'ground_floor': Floor(1, Image(back='light_green')),
              'ocean_floor': Floor(2, Image(back='blue')),
              'empty_tile': Structure(0, Image(letter=' ')),
              'grass_tile': Structure(1, Image(letter='/', fore='green')),
              'mountain_tile': Structure(1, Image(letter='A', fore='white')),
              'forest_tile': Structure(1, Image(letter='T', fore='green')),
              'ocean_tile': Structure(1, Image(letter='_', fore='cyan')),
              'town_tile': Structure(1, Image(letter='H', fore='light_red', style='bright')),
              'crypt_tile': Structure(1, Image(letter='=', fore='white', style='bright')),
              'player': Structure(20, Image(letter='o', fore='yellow', style='bright'))}


def add_structure(name, structure):
    structures[name] = structure


# -----------------------------------------------------
# Filler images


filler_list = {(structures['void_floor'], structures['void_floor']): Image(),
               (structures['ground_floor'], structures['ground_floor']): Image(back='light_green'),
               (structures['ocean_floor'], structures['ocean_floor']): Image(back='blue'),
               (structures['empty_tile'], structures['empty_tile']): Image(),
               (structures['mountain_tile'], structures['mountain_tile']): Image(letter='A', fore='light_black'),
               (structures['grass_tile'], structures['grass_tile']): Image(letter='/', fore='green'),
               (structures['forest_tile'], structures['fores_tile']): Image(letter='T', fore='green'),
               (structures['ocean_tile'], structures['ocean_tile']): Image(letter='_', fore='cyan'),
               (structures['town_tile'], structures['town_tile']): Image(letter='=', fore='light_black'),
               (structures['crypt_tile'], structures['crypt_tile']): Image(letter='∩', fore='black')}


def add_filler(structure1, structure2, filler):
    filler_list[(structure1, structure2)] = filler
    return None


# ------------------------------------------------------
# MultiStructures


class MultiStructure(object):
    """Dictionary of tile keys; each
    key holds a list of structures that
    the tile contains."""
    def __init__(self, tile_dict):
        self.tile_dict = tile_dict

    def __repr__(self):
        return f'MultiStructure{self.tile_dict}'


def mountain():
    pass


def ocean():
    pass


def forest():
    pass


def crypt():
    pass


def town():
    pass
