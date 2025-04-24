# PiINDIControlPad
Telescope Control panel for 7" HDMI display for Raspberry Pi.

This software is intended to not only provide a control panel for a telescope but also operate all aspects of the telescope except actually moving motors - it's expected that the user has connected the Raspberry Pi via USB and set up a driver for the telescope under INDI (see indilib.org for more information). In my case I am using a home built 16" F4.5 Dobsonian Telescope with an OnStep controller controlling the stepper motors that move the scope in Alt Az as well as provide for two focus motors and a field rotation motor.

![Image of Control Panel](https://raw.githubusercontent.com/gordtulloch/PiINDIControlPad/main/ControlPanel.png)

In general when a user enters an object into the control panel, the telescope will check that it is above the horizon (Altitude > 15deg) then slew the telescope to that object using the INDI telescope driver. In the meantime, a flag is set that "The telescope moved" so that the next time through the main loop, a platesolve in initiated. The platesolve takes an image of the sky through the camera specified in the script (in my case a Raspberry Pi PiCam V2 directly attached to the Raspberry Pi with a long lens) and attempts to do a platesolve to determine the actual coordinates that the telescope is pointed to. Once these coordinates are determined an offset is calculated and if larger than a preset value (normally 30 arcsecs) an adjusted slew command is sent to the telescope. The process repeats until the object in the telescope field is within the preset value of arcsecs of the object whereupon the telescope will stop platesolving and track the object. A user can initiate a solve from the control panel in case the scope is bumped etc.

To calibate the platesolve the user hits the Sync button - the program will save the current object coords, the solver will run and determine the offset of the telescope from the computed centre RA,Dec of the field of the camera doing the solving. This offset will be applied when determining whether the telescope needs to be slewed so the user does not have to centre the camera on the telescope field exactly to get good telescope positioning.

INSTALLATION

On Debian or Ubuntu, follow directions on https://www.hnsky.org/astap.htm to install ASTAP on your platform, then:

    sudo apt-add-repository ppa:mutlaqja/ppa
    sudo apt-get update
    sudo apt install git indi-full gsc kstars-bleeding swig libcfitsio-dev libnova-dev python3 python3-tk python-is-python3 python3-pip python3-venv cmake python3-setuptools python3-dev libindi-dev swig libcfitsio-dev libnova-dev mysql-server

    sudo mysql
    CREATE DATABASE pyindicontrolpad;
    CREATE USER 'pyindicontrolpad'@'localhost' IDENTIFIED BY 'secret';
    ALTER USER 'pyindicontrolpad'@'localhost' IDENTIFIED WITH mysql_native_password BY 'secret';
    GRANT ALL PRIVILEGES ON pyindicontrolpad.* TO 'pyindicontrolpad'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;
    
    git clone https://github.com/gordtulloch/PiINDIControlPad.git
    cd PiINDIControlPad
    python -m venv .venv
    source .venv/bin/activate
    pip3 install "git+https://github.com/indilib/pyindi-client.git@674706f#egg=pyindi-client"
    pip install astropy numpy tzlocal pytz photutils mysql-connector-python-rf 

You can run the simulators from the command line to test with:

    indiserver indi_simulator_telescope indi_simulator_ccd
	
You probably want to do this in a seperate terminal window to make it easy to see logging statements from indiserver.

Run the programs with:

Mini interface:
    source .venv/bin/activate

    python mini.py

Control pad interface:
    source .venv/bin/activate

    python controlpad.py
