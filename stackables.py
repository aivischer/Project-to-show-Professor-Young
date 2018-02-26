class Stackable(object):
    """Abstract base class for all objects
    that stack in one way or another."""
    def __init__(self, stacks, max_stack_size):
        self.stack_size = stacks
        self.max_stack_size = max_stack_size

    def __add__(self, other):
        return self.__class__(self.stack_size + other.stack_size, self.max_stack_size)

    def __repr__(self):
        name_length = len(__name__)
        return f'{self.__class__}'[9 + name_length:-2] + f'({self.stack_size}, {self.max_stack_size})'


class Status(Stackable):
    """Base class for status effects."""
    pass


class Poison(Status):
    pass


class Burn(Status):
    pass


class Item(Stackable):
    """Base class for items."""
    def __init__(self, name, size, max_size):
        super().__init__(size, max_size)
        self.name = name


class Material(Item):
    def __add__(self, other) -> list:
        total = self.stack_size + other.stack_size
        stacks = total // self.max_stack_size
        remainder = total % self.max_stack_size
        stacks_list = [type(self)(remainder)]
        stacks_list += [type(self)(self.max_stack_size) for i in range(stacks)]
        return stacks_list


class Stardust(Material):
    def __init__(self, size):
        super().__init__('Stardust', size, 100)


class Unique(Item):
    """Items that have a maximum
    stack size of 1, and hence do
    not stack."""
    def __init__(self, name, description):
        super().__init__(name, 1, 1)
        self.desc = description
