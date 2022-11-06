import time

from controller import ODOP
from composition import Composition

from functions import type_input
from preferences import *

from maillage import *




    
'''# Initialise camera
    camera = Camera()
    while not camera.ready():
        time.sleep(0.1)
        camera.update_status()'''



'''# Calibrate ODOP
    odop.calibrate()'''
    
if __name__ == '__main__':

    # Initialise ODOP
    odop = ODOP()
    while not odop.ready():
        time.sleep(0.1)

    while True: #condition d'arrêt si problème à rajouter ?
        mode = type_input('Select mode : go_to to go to a specific position; group_pictures to take pictures at specific positions; automatic_pictures to automatically take a number of pictures\n>', str)
        if mode == 'go_to':
            pivot_position = type_input('Enter the angle of the pivot\n>', float)
            courroie_position = type_input('Enter the angle of the belt\n>', float)
            print('Successfully moved')
            mode = type_input('Do you want to take a picture ? y for yes, n for no\n>', str)
            if mode == 'y':
                #take picture
                print('Picture taken') # à mettre dans la fonction de prise de photo

        elif mode == 'group_pictures':
            positions = type_input('Enter the desired positions, as a list with the format [pivot angle, belt angle]\n>', list)

        elif mode == 'automatic_pictures':

            #à modifier
            while True:

                vertical_shots_nb   = type_input('Enter the number of vertical shots\n> ', int)
                horizontal_shots_nb = type_input('Enter the number of horizontal shots\n> ', int)

                # Create composition
                composition = Composition (
                    odop=odop,
                    #camera=camera,
                    vertical_shots_nb=vertical_shots_nb,
                    horizontal_shots_nb=horizontal_shots_nb
                )

                input(f'\nComposition initialised. Press any key to begin run.\n{RUN_MESSAGE}')

                # Run composer
                success, msg = composition.run()
                if not success: raise InterruptedError(f'run failure - {msg}')

        else:
            print('Error, invalid input')
    