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

    def execute (self, command: str, time_window: float = 2., readback: str = '', fatal: str = '') -> int:
        """
        Execute command and check for readback message and fatal message
        :param command: command
        :param time_window: time window to receive readback (in seconds)
        :param readback: readback message
        :param fatal: fatal message
        :return: status value (0=success, 1=timeout, 2=fatal)
        """

        # Send command
        if STATUS_VERBOSE: print(f'\"{command}\"')
        self.controller .write(bytes(command, 'utf-8'))
        time.sleep(0.05)

    #à modifier, sûrement simplifier
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
                if fatal and data_decoded == fatal:  # Exit loop with failure
                    return 2

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

    def get_angle (self, axis: str) -> float:
        if axis not in ('x', 'y'): return None
        return self.__angles [axis]'''
    
    def set_angle (self, axis: str, val: float):
        """
        Set recorded angle for specified axis
        :param axis: axis
        :param val: angle value (in deg)
        """
        if axis not in ('x', 'y'): return None
        self.__angles [axis] = val


    '''# Calibration
    def estimate_zero (self) -> tuple:
        """
        Move to minimum position and then back up to +25
        :return: success_bool, success_msg
        """

        # Move to bottom of range
        val = self.execute (
            command=f'move_rel x -200',
            time_window=TIME_WINDOW_MAX,
            readback='move_rel x: limit reached',
            fatal='move_rel x: success'
        )
        if val != 0: return False, 'unable to reach minimum'  # Exit if didn't find end stop

        # Move up to estimate zero position
        success, msg = self.move_relative ('x', 25)
        return success, msg

    
    def adjust_position (self, axis: str, exit_cmd: str = 'go', time_window = 600.):
        """
        Enable manual angular position adjustment of specified axis
        :param axis: axis
        :param exit_cmd: command to exit read loop
        :param time_window: timeout
        :return: success_bool, success_msg
        """

        # Information
        print(f'\nInput relative adjustments for {axis}-axis (in deg). Type \'{exit_cmd}\' to validate.')

        time_now = time.time()
        while True:
            # Check timeout
            if time.time() > time_now + time_window: return False, 'timeout'

            # Read command
            command = input('> ')
            if command == exit_cmd: return True, ''

            # Execute command
            try: self.move_relative(axis, float(command))
            except ValueError: continue'''


    '''def set_zero (self) -> bool:
        val = self.execute (command='set_zero', time_window=2., readback='set_zero: success')
        return val == 0


    def calibrate (self):
        """
        Calibrate ODOP
        """
        if STATUS_VERBOSE: print('\nCalibrating ODOP')
        success, msg = self.estimate_zero()
        if not success: raise InterruptedError(f'estimate_zero failure - {msg}')
        success, msg = self.adjust_position('x')
        if not success: raise InterruptedError(f'manual calibration failure - {msg}')
        self.set_zero()'''


    # Motion
    def move_relative_p (self, value: float) -> tuple:
        """
        Execute relative angular position command of specified axis
        :param axis: axis
        :param value: angular displacement
        :return: success_bool, success_msg
        """

        if value >= X_ANGLE_MIN and value <= X_ANGLE_MAX:
            
            # Log movement
            self.set_angle('x', value)

            # Execute command
            val = self.execute (
                command=f'rotate_p {float(value)}',
                time_window=min(max(abs(2*value), TIME_WINDOW_MIN), TIME_WINDOW_MAX),  # TIME_WINDOW_MIN <= time_window <= TIME_WINDOW_MAX
                readback=f'rotate_p : success',
                fatal=f'rotate_p : limit reached'
            )

            # Process output
            if   val == 0: return True, ''
            elif val == 2: return False, 'limit reached'
            else:          return False, 'timeout'
        else:
            print('Value out of axis range.')

    def move_relative_c (self, value: float) -> tuple:
        """
        Execute relative angular position command of specified axis
        :param axis: axis
        :param value: angular displacement
        :return: success_bool, success_msg
        """
        if value >= Y_ANGLE_MIN and value <= Y_ANGLE_MAX:
            # Log movement
            self.set_angle('y', value)

            # Execute command
            val = self.execute (
                command=f'rotate_c {float(value)}',
                time_window=min(max(abs(2*value), TIME_WINDOW_MIN), TIME_WINDOW_MAX),  # TIME_WINDOW_MIN <= time_window <= TIME_WINDOW_MAX
                readback=f'rotate_c : success',
                fatal=f'rotate_c : limit reached'
            )

            # Process output
            if   val == 0: return True, ''
            elif val == 2: return False, 'limit reached'
            else:          return False, 'timeout'
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
        self.move_relative_p (0.)

        # Then, go to the command
        self.move_relative_p (value)

    
    def move_absolute_c (self, value: float) -> tuple:
        """
        Execute absolute angular position command of specified axis
        :param axis: axis
        :param value: angular position
        :return: success_bool, success_msg
        """

        # Start by going to 0
        self.move_relative_c (0.)

        # Then, go to the command
        self.move_relative_c (value)
        
