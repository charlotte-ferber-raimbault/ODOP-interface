# Copyright (C) 2022 Mines Paris (PSL Research University). All rights reserved.

import csv

from controller import ODOP
from preferences import *
from maillage import *



class Composition:

    def __init__ (self, odop: ODOP):
        self.odop = odop
        
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

    def group_pictures (self, liste : list) -> tuple:
        """
        Run group pictures
        :param liste: list of the positions
        :return: success_bool, success_msg
        """
        # Field names
        fields = ['Order', 'Pivot angle', 'Belt angle']

        # Blank list of rows
        rows = []

        # Name of the cv file
        filename = 'group_pictures.csv'

        if STATUS_VERBOSE: print('\nStarting run')    
        print(liste)
        for i in range(len(liste)):            
            self.odop.move_absolute_c(liste[i][1])
            self.odop.move_absolute_p(liste[i][0])
            self.odop.take_picture()
            rows.append([i, liste[i][0], liste[i][1]])

        # Creating the file
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter = ',')
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)

        # To end at the position (0, 0)
        if self.odop.get_angle('x') != 0:
            self.odop.move_absolute_p(0.)
        if self.odop.get_angle('y') != 0:
            self.odop.move_absolute_c(0.)

        if STATUS_VERBOSE: print('Run success\n')
        return True, ''

    def automatic_pictures (self, nb_samples: int) -> tuple:
        """
        Run automatic pictures
        :param nb_samples: number of pictures
        :return: success_bool, success_msg
        """
        # Field names
        fields = ['Order', 'Pivot angle', 'Belt angle']

        # Blank list of rows
        rows = [[0, 0., 0.]] # Picture taken at (0., 0.)

        # Name of the cv file
        filename = 'automatic_pictures.csv'

        if STATUS_VERBOSE: print('\nStarting run')

        M = maillage(nb_samples)

        # To start at the position (0, 0)
        if self.odop.get_angle('x') != 0:
            self.odop.move_absolute_p(0.)
        if self.odop.get_angle('y') != 0:
            self.odop.move_absolute_c(0.)
        
        # For the position (0, 0)
        #self.odop.take_picture()

        y_angle = 0

        # For the rest
        for i in range(1, len(M)):            
            self.odop.move_relative_c(M[i][0] - M[i - 1][0])
            self.odop.move_relative_p(M[i][1] - M[i - 1][1])
            #self.odop.take_picture()
            rows.append([i, M[i][0], M[i][1]])
            if M[i][0] != y_angle:
                self.odop.move_relative_p(-self.odop.get_angle('x')) # The pivot does one revolution as a maximum
                y_angle = M[i][0]
        
        # Creating the file
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter = ',')
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)
        
        # To end at the position (0, 0)
        if self.odop.get_angle('x') != 0:
            self.odop.move_absolute_p(0.)
        if self.odop.get_angle('y') != 0:
            self.odop.move_absolute_c(0.)

        if STATUS_VERBOSE: print('Run success\n')
        return True, ''