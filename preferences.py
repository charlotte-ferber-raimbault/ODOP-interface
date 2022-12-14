# Copyright (C) 2022 Mines Paris (PSL Research University). All rights reserved.

# Program settings
SESSION_PATH = "c:\\tmp\\"
FILENAME_TEMPLATE = "odop-vI{}-vA{}-hI{}-hA{}.jpg"

# Serial settings
PORT = 'COM6'  
BAUD_RATE = 9600
READY_MSG = 'Controller ready'  # Program waits for this message

# X-axis angular range, in degrees
X_ANGLE_MIN = 0.
X_ANGLE_MAX = 360.

# Y-axis angular range, in degrees
Y_ANGLE_MIN = 0.
Y_ANGLE_MAX = 90.

# Delays
TIME_INIT_MAX = 60.  # Maximum initialisation time for ODOP (in seconds)
TIME_WINDOW_MIN = 2.  # Minimum time window to execute a command
TIME_WINDOW_MAX = 120.  # Maximum time window to execute a command (default for move_abs commands)
DELAY_BEFORE_SHOT = 1.
DELAY_AFTER_SHOT = 1.5

# Verbose 
DEBUG_VERBOSE = False
STATUS_VERBOSE = True
RUN_MESSAGE = 'Make sure to remove all calibration wires before starting run.'


steps_per_deg_p = 200*16/360 # Number of steps per degree 
steps_per_deg_c = 200/360 # Number of steps per degree 

belt_to_motor = 453/35.015 # Inverse of reduction ratio between motor and belt