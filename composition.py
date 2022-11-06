import time

from controller import ODOP
from preferences import *
from maillage import *



class Composition:

    def __init__ (self, odop: ODOP, nb_samples: int = nb_samples):
        self.odop = odop
        self.nb_samples = nb_samples
        

    def run (self) -> tuple:
        """
        Run composition
        :return: success_bool, success_msg
        """

        if STATUS_VERBOSE: print('\nStarting run')

        X, Y, Z = fibonacci_sphere(nb_samples)

        #à modifier en fonction de la forme de X et Y
        #ne fontionnne pas pour les 1er i et j
        for i in range (len(Y)):
            self.odop.move_relative_c(Y[i] - Y[i - 1])
            for j in range (len(X)):
                self.odop.move_relative_p(X[j] - X[j - 1])
                #take picture
            self.odop.move_relative_p(-self.odop.get_angle('x'))

        '''for vertical_shot_id in range (self.vertical_shots_nb + 1):
            if STATUS_VERBOSE: print(f'\tCurrent vAngle is {self.odop.get_angle("x")}')

            # Reset Y-axis angle (controller-side reset deactivated because superfluous)
            if STATUS_VERBOSE: print('\tResetting hAngle. Was {}'.format(self.odop.get_angle('y')))
            self.odop .set_angle ('y', 0.)
            #success, val = self.odop .execute (command='move_abs y 0', time_window=60., readback='move_abs y: success')
            #if not success: return False, val

            # Run through horizontal steps (turntable rotation)
            for horizontal_shot_id in range (self.horizontal_shots_nb):
                if STATUS_VERBOSE: print(f'\t\tCurrent hAngle is {self.odop.get_angle("y")}')

                # Build file name
                filepath = SESSION_PATH + FILENAME_TEMPLATE .format(vertical_shot_id, self.odop.get_angle('x'), horizontal_shot_id, self.odop.get_angle('y'))
                if STATUS_VERBOSE: print(f'\t\tRequesting shot: {filepath}')

                # Take shot
                time.sleep(DELAY_BEFORE_SHOT)
                self.camera .capture(filepath=filepath)
                time.sleep(DELAY_AFTER_SHOT)

                # Move on Y-axis (turntable)
                self.odop .move_relative ('y', self.y_step_deg)

            # Move on X-axis (swing)
            success, val = self.odop .move_relative ('x', self.x_step_deg)
            if not success: return False, val'''

        if STATUS_VERBOSE: print('Run success\n')
        return True, ''
