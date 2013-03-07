Script for storing calibration on AFL-408BB
-------------------------------------------

Installation
------------

#. Copy the `sicktouch` directory to `/usr/local/share`
#. Create the file `/usr/local/share/sicktouch/.ftppassword`, and make it look like below

    .. code-block:: none

        username=<username here>
        password=<password here>
        hostaddr=xxx.xxx.xxx.xxx

#. Copy runme.sh to `/usr/local/bin/runme.sh`

Usage
-----

#. Start the computer
#. Connect a keyboard to a viewer usb port
#. Press ctrl+alt+F1
#. You will now come to a command prompt mode 
#. Type in "sudo -i" and press enter
#. Type in "pkill java" and press enter
#. Now the application should be killed, meaning that if you switch to the application you will not see it
#. Type in "export DISPLAY=:0" and press enter
#. Type in "gCal 4" and press enter
#. go to the calibration application by pressing alt+F7.
#. tap on the markers on the screen.
#. go back to command promt to store calibration data permanently by pressing ctrl+alt+F1
#. Make sure you are connected to Elektronix "Internet LAN"
#. Type in "dhclient eth0"
#. Type in "cd /usr/local/share/sicktouch"
#. Type in "./runme.sh"
#. Reboot the machine to make sure that the calibration data is still working.
#. Done!
