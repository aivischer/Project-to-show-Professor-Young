from colorama import *


class Map(object):
    """
    Matrix is a list of rows of a
    rectangle. Each value in each
    row should be a string that will
    be diplayed in a merged R x C
    matrix. Maps also have borders.
    """
    def __init__(self, matrix):
        self.matrix = matrix

    def __str__(self):
        string = (Fore.BLACK + '=') * (len(self.matrix[0]) + 4) + '\n'
        for row in self.matrix:
            string += (Fore.BLACK + '| ') + ''.join(row) + (Fore.BLACK + ' |\n')
        string += '=' * (len(self.matrix[0]) + 4)
        return string
