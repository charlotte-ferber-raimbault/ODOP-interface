import time

from controller import ODOP
from composition import Composition

from functions import type_input
from preferences import *

from maillage import *



if __name__ == '__main__':
    
    '''# Initialise camera
    camera = Camera()
    while not camera.ready():
        time.sleep(0.1)
        camera.update_status()'''


    # Initialise ODOP
    odop = ODOP()
    while not odop.ready():
        time.sleep(0.1)

    '''# Calibrate ODOP
    odop.calibrate()'''


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