import time

from controller import ODOP
from preferences import *
from maillage import *



class Composition:

    def __init__ (self, odop: ODOP, nb_samples: int = nb_samples):
        self.odop = odop
        self.nb_samples = nb_samples

    def go_to (self, x_angle : float, y_angle : float) -> tuple:
        """
        Goes to a position
        :param x_angle: position of the pivot
        :param y_angle: position of the belt
        :return: success_bool, success_msg
        """

        if STATUS_VERBOSE: print('\nStarting run')

        self.odop.move_absolute_c(y_angle)
        self.odop.move_absolute_p(x_angle)

        if STATUS_VERBOSE: print('Run success\n')
        return True, ''

    def group_pictures (self, list: list) -> tuple:
        """
        Run group pictures
        :param list: list pf the positions
        :return: success_bool, success_msg
        """

        if STATUS_VERBOSE: print('\nStarting run')    

        for i in range(1, len(list)):            
            self.odop.move_absolute_c(list[i][1])
            self.odop.move_relative_p(list[i][0])
            self.odop.take_picture()

        if STATUS_VERBOSE: print('Run success\n')
        return True, ''

    def automatic_pictures (self, nb_samples: int = nb_samples) -> tuple:
        """
        Run automatic pictures
        :param nb_samples: number of pictures
        :return: success_bool, success_msg
        """

        if STATUS_VERBOSE: print('\nStarting run')

        M = maillage(nb_samples)

        # To start at the position (0, 0)
        if self.odop.get_angle('x') != 0:
            self.odop.move_absolute_p(0.)
        if self.odop.get_angle('y') != 0:
            self.odop.move_absolute_c(0.)
        
        # For the position (0, 0)
        self.odop.take_picture()

        y_angle = 0

        # For the rest
        for i in range(1, len(M)):            
            self.odop.move_relative_c(M[i][0] - M[i - 1][0])
            self.odop.move_relative_p(M[i][1] - M[i - 1][1])
            self.odop.take_picture()
            if M[i][0] != y_angle:
                self.odop.move_relative_p(-self.odop.get_angle('x')) # the pivot does one revolution as a maximum
                y_angle = M[i][0]
        
