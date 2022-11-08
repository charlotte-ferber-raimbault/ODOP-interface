# ODOP interface v1.0.0
Copyright (C) 2022 Mines Paris (PSL Research University). All rights reserved.

<br><br>

## Description
Controller program for <a href="https://www.smartpixels.fr">SmartPixels</a>' <strong>Omni-Directional Object Pictures</strong> (ODOP) automated scanner.

<br><br>


## How does it work ?
* The file 'main.py' enables the user to choose the mode.
* Every mode's orders are in the file "composition.py".
* This file calls motion functions from "controller.py".
* The motion functions send commands to the Arduino card, on which was previously uploaded "commande_odop.ino" thanks to Arduino IDE.
* The file "preferences.py" enables the user to change parameters (such as the PORT on whiwh the Arduino card is connected).
* The files "maillage.py and "functions.py" both define functions useful in the rest of the code.

<br><br>

## Requirements
* Python 3 (tested with Python 3.9.0; should work with Python 3.6.0 and newer)
* PySerial module (run "`pip install pyserial`")
