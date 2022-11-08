# Copyright (C) 2022 Mines Paris (PSL Research University). All rights reserved.

import serial  # pip install pyserial
import time

from preferences import *



class Controller:

    def __init__ (self, baud_rate: int = BAUD_RATE, port = PORT, ready_msg = READY_MSG, time_init_max = TIME_INIT_MAX):
        self.controller = serial.Serial(port=port, baudrate=baud_rate, timeout=.1)
        self.ready_msg = ready_msg
        self.__ready = False
        self.time_init = time.time()
        self.time_init_max = time_init_max

        if not self.__ready:
            self.__check_ready()
    
    def __check_ready (self):
        while True:
            data = self.controller .readline()

            if data:
                data_decoded = data.decode(encoding='utf-8')[:-2]
                if STATUS_VERBOSE: print(data_decoded)

                if data_decoded == self.ready_msg:
                    self.__ready = True
                    break
                if time.time() > self.time_init + self.time_init_max:
                    raise InterruptedError('controller not ready')
    
    def ready (self):
        return self.__ready

    def execute (self, command: str, time_window: float = 2., readback: str = '') -> int:
        """
        Execute command and check for readback message
        :param command: command
        :param time_window: time window to receive readback (in seconds)
        :param readback: readback message
        :return: status value (0=success, 1=timeout)
        """

        # Send command
        if STATUS_VERBOSE: print(f'\"{command}\"')
        self.controller .write(bytes(command, 'utf-8'))
        time.sleep(0.05)

        # Process readback
        time_start = time.time()  # in seconds
        if DEBUG_VERBOSE: print(f'{int(time_start)} - waiting till {int(time_start + time_window)} ({time_window} seconds)')
        while time.time() < time_start + time_window:
            # Read data
            data = self.controller .readline()

            if data:
                data_decoded = data.decode(encoding='utf-8')[:-2]
                if STATUS_VERBOSE: print(data_decoded)

                if readback and data_decoded == readback:  # Exit loop with success
                    return 0

        if readback: return 1
        else: return 0  # True if readback unspecified


class ODOP (Controller):

    def __init__ (self, baud_rate: int = BAUD_RATE, port = PORT, ready_msg = READY_MSG, time_init_max = TIME_INIT_MAX):
        super(ODOP, self).__init__ (baud_rate, port, ready_msg, time_init_max)
        self.__angles = {'x': 0., 'y': 0.}

    '''def get_version (self):
        self.execute (command='version')

    def get_status (self) -> tuple:
        val = self.execute (command='status', time_window=2., readback='Status ok')
        if val == 0: return True, ''
        else: return False, 'unable to verify status'
'''
    def get_angle (self, axis: str) -> float:
        if axis not in ('x', 'y'): return None
        return self.__angles [axis]
    
    def set_angle (self, axis: str, val: float):
        """
        Set recorded angle for specified axis
        :param axis: axis
        :param val: angle value (in deg)
        """
        if axis not in ('x', 'y'): return None
        self.__angles [axis] = val

    # Motion
    def move_relative_p (self, value: float) -> tuple:
        """
        Execute relative angular position command of specified axis
        :param axis: axis
        :param value: angular displacement
        :return: success_bool, success_msg
        """
        new_angle = self.get_angle('x') + value
        nb_steps = round(value*steps_per_deg) # To send a command in steps to the motor

        if new_angle >= X_ANGLE_MIN and new_angle <= X_ANGLE_MAX:
            
            # Log movement
            self.set_angle('x', new_angle)

            # Execute command
            val = self.execute (
                command=f'rotate_p {float(nb_steps)}',
                time_window=TIME_WINDOW_MAX,
                readback=f'rotate_p : success'
            )
            
            # Process output
            if   val == 0:
                # Inform user
                print(f'Successfully moved to {self.get_angle("x")}')
                return True, ''
            else:          
                return False, 'timeout'
        else:
            print('Value out of axis range.')

    def move_relative_c (self, value: float) -> tuple:
        """
        Execute relative angular position command of specified axis
        :param axis: axis
        :param value: angular displacement
        :return: success_bool, success_msg
        """
        new_angle = self.get_angle('y') + value
        motor_angle = value*belt_to_motor # Because the angle of the motor is different from the angle of the belt
        nb_steps = round(motor_angle*steps_per_deg) # To send a command in steps to the motor

        if new_angle >= Y_ANGLE_MIN and new_angle <= Y_ANGLE_MAX:
            # Log movement
            self.set_angle('y', new_angle)

            # Execute command
            val = self.execute (
                command=f'rotate_c {float(nb_steps)}',
                time_window=TIME_WINDOW_MAX,
                readback=f'rotate_c : success'
            )

            # Process output
            if   val == 0:
                # Inform user
                print(f'Successfully moved to {self.get_angle("y")}')
                return True, ''
            else:          
                return False, 'timeout'
        else:
            print('Value out of axis range.')


    def move_absolute_p (self, value: float) -> tuple:
        """
        Execute absolute angular position command of specified axis
        :param axis: axis
        :param value: angular position
        :return: success_bool, success_msg
        """

        # Start by going to 0
        self.move_relative_p(-self.get_angle('x'))

        # Then, go to the command
        self.move_relative_p(value)

    
    def move_absolute_c (self, value: float) -> tuple:
        """
        Execute absolute angular position command of specified axis
        :param axis: axis
        :param value: angular position
        :return: success_bool, success_msg
        """

        # Start by going to 0
        self.move_relative_c(-self.get_angle('y'))

        # Then, go to the command
        self.move_relative_c(value)
        
    # Taking pictures
    def take_picture(self):
        """
        Execute taking picture command
        :return: success_bool, success_msg
        """
        # Execute command
        val = self.execute (
            command=f'take_picture',
            time_window=TIME_WINDOW_MAX,
            readback=f'take_picture : success'
        )

        # Process output
        if   val == 0:
            # Inform user
            print('Picture taken')
            return True, ''
        else:          
            return False, 'timeout'

