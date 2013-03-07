Script for storing calibration on AFL-408BB
-------------------------------------------

 1. Start the computer
 2. Connect a keyboard to a viewer usb port
 3. Press ctrl+alt+F1
 4. You will now come to a command prompt mode 
 5. Type in "sudo -i" and press enter
 6. Type in "pkill java" and press enter
 7. Now the application should be killed, meaning that if you switch to the application you will not see it
 9. Type in "export DISPLAY=:0" and press enter
10. Type in "gCal 4" and press enter
11. go to the calibration application by pressing alt+F7.
12. tap on the markers on the screen.
13. go back to command promt to store calibration data permanently by pressing ctrl+alt+F1
14. Make sure you are connected to Elektronix "Internet LAN"
15. Type in "dhclient eth0"
16. Type in "cd /usr/local/share/sicktouch"
17. Type in "./runme.sh"
18. Reboot the machine to make sure that the calibration data is still working.
19. Done!