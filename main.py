# Copyright (C) 2022 Mines Paris (PSL Research University). All rights reserved.

import time
import csv

from controller import ODOP
from composition import Composition

from functions import type_input
from preferences import *

from maillage import *


if __name__ == '__main__':

    # Initialise ODOP
    odop = ODOP()
    while not odop.ready():
        time.sleep(0.1)

    while True:

        # Create composition
        composition = Composition (odop=odop)

        mode = type_input('Select mode : go_to to go to a specific position; group_pictures to take pictures at specific positions; automatic_pictures to automatically take a number of pictures\n>', str)
        
        if mode == 'go_to':
            pivot_position = type_input('Enter the angle of the pivot\n>', float)
            belt_position = type_input('Enter the angle of the belt\n>', float)

            # Run composer
            success, msg = composition.go_to(pivot_position, belt_position)
            if not success: raise InterruptedError(f'run failure - {msg}')
            
            mode = type_input('Do you want to take a picture ? y for yes, n for no\n>', str)
            if mode == 'y':
                odop.take_picture()
            
            composition.go_to(0., 0.)


        elif mode == 'group_pictures':
            positions = type_input('Enter the desired positions, as a list with the format [pivot angle, belt angle]\n>', list)
            success, msg = composition.group_pictures(positions)
            if not success: raise InterruptedError(f'run failure - {msg}')

        elif mode == 'automatic_pictures':
            nb_pictures = type_input('Enter the number of pictures\n>', int)
            success, msg = composition.automatic_pictures(nb_pictures)
            if not success: raise InterruptedError(f'run failure - {msg}')

        else:
            print('Error, invalid input')
    