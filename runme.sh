#!/bin/bash
#
# Execution script for storing calibration coordinates
#
# CHANGELOG:
# 16.12.2011:
#   - Fixed bug which makes the calibration script store the penmount.dat
#     of current machine to /mnt/persist/os_config/root/etc/penmount.dat
#   - Moved .ftppassword to application directory instead of
#     /mnt/persist/os_config/root/root
#   - Moved HOSTADDR to .ftppassword instead of hardcoding to this file, so that storing
#     the calibration can be done remotely if desired by changing the address. 
#
# 07.09.2012
#	- Added absolute paths to .ftppassword and sicktouch.py files
#

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Some variables
CALIB="/tmp/calibration.db"
INTERFACE="eth0"
PENMOUNT="/etc/penmount.dat"
DBLOCATION="/mnt/persist/os_config/touch/calibration.db"
PASSFILE="/usr/local/share/sicktouch/.ftppassword"
SICKTOUCH="/usr/local/share/sicktouch/bin/sicktouch.py"
PYTHON="/usr/bin/env python"

# Check if python script exists
if [ ! -e $SICKTOUCH ]; then
  print "$SICKTOUCH does not seem to exist."
  exit 0
fi

# Check if penmount.dat exists
if [ ! -r $PENMOUNT ]; then
  print "Could not read $PENMOUNT, exiting"
  exit 0
fi

# Run python script to save calibration to ftp
if [ -r $PASSFILE ]; then
  USERNAME=`awk -F'=' '/username/ {print $2}' $PASSFILE`
  PASSWORD=`awk -F'=' '/password/ {print $2}' $PASSFILE`
  HOSTADDR=`awk -F'=' '/hostaddr/ {print $2}' $PASSFILE`
  $PYTHON $SICKTOUCH --dumb $USERNAME $PASSWORD $HOSTADDR
  
  # Copy calibration.db to /mnt/persist/os_config/touch/calibration.db
  cp $CALIB $DBLOCATION

else
  echo "Could not open $PASSFILE for reading."
fi
