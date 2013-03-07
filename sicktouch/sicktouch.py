# -*- coding: utf-8 -*- 
#!/usr/bin/env python

from lib import netifaces
from optparse import OptionParser
from ftplib import FTP
import ftplib

class iface:
    def __init__(self, iface, penmount_file):
        self.iface = iface
        self.penmount_file = penmount_file
        
    def get_mac(self):
        try:
            ifinfo = netifaces.ifaddresses(self.iface)
            mac = ifinfo[17][0]['addr']
            return mac
        except ValueError, e:
            raise SystemExit(e)
        
    def read_coords(self):
        try:
            f = open(self.penmount_file)
            coords = f.readline()
            f.close()
            return coords
        except IOError, e:
            raise SystemExit(e)
            
    def write_config(self, destination):
        mac = u'%s' % self.get_mac()
        coords = u'%s' % self.read_coords()
        config = mac + "=" + coords + "\n"
        
        # Checks database file for duplicate MAC addresses.
        # Returns True if file is "clean", and False if duplicate is found.
        def check_for_duplicate():
            text = open(destination, 'r').read()
            print "Looking for duplicates in", destination
            if text.find(mac) == -1:
                print " * Coordinates for", mac, "not found.\nAdding to database"
                return True
            else:
                print " *", mac, "already exists in the database.\n * WARNING: WILL NOT WRITE TO DATABASE!"
                return False
        try:
            if check_for_duplicate():
                f = open(destination, 'a')
                f.writelines(config)
                f.close()
                print "Success!\nWrote calibration to file %s" % destination
        except IOError, e:
            raise SystemExit(e)
      
            
class sickftp:
    def __init__(self, username, password, address):
        self.username = username
        self.password = password
        self.address = address
        
    def connect(self):
        self.ftp = FTP(self.address)
        try:
            print self.ftp.login(self.username, self.password)
        except ftplib.Error, e:
            raise SystemExit(e)
            
            
    
    def download(self, filename):
        directory = '/SickIVP/Calibration'
        self.ftp.cwd(directory)
        try:
            writefile = open(filename, 'wb')
            print "Downloading " + filename
            self.ftp.retrbinary('RETR calibration.db', writefile.write)
            writefile.close()
        except IOError, e:
            self.ftp.close()
            raise SystemExit(e)
        
    def upload(self, filename):
        directory = '/SickIVP/Calibration'
        self.ftp.cwd(directory)
        try:
            readfile=open(filename,'rb')
            print "Uploading "+ filename
            self.ftp.storbinary('STOR calibration.db', readfile)
            readfile.close()
        except IOError, e:
            self.ftp.close()
            raise SystemExit(e)


def main():
    def iface_callback(option, opt_str, value, parser):
        myif = iface(value[0], value[1])
        myif.write_config(value[2])
        
    def download_callback(option, opt_str, value, parser):
        username = raw_input("Enter username: ")
        password = raw_input("Enter password: ")
        sick = sickftp(username, password , '10.47.22.100')
        sick.connect()
        sick.download(value)
        sick.ftp.close()
        
        
    def upload_callback(option, opt_str, value, parser):
        username = raw_input("Enter username: ")
        password = raw_input("Enter password: ")
        sick = sickftp(username, password, '10.47.22.100')
        sick.connect()
        sick.upload(value)
        sick.ftp.close()
        
    def dumb_callback(option, opt_str, value, parser):
        username = value[0]
        password = value[1]
        ipaddress = value[2]
        
        sick = sickftp(username, password, ipaddress)
        sick.connect()
        sick.download('/tmp/calibration.db')
        myif = iface('eth0', '/etc/penmount.dat')
        myif.write_config('/tmp/calibration.db')
        sick.upload('/tmp/calibration.db')
        
        
        
    usage = "usage: %prog [options] args"
    parser = OptionParser(usage)

    parser.add_option('--iface',
                      action = 'callback',
                      callback = iface_callback,
                      type = 'string',
                      nargs = 3,
                      help = 'Writes calibration for specific interface.\
                              Requires 3 args: 1) Network interface, 2) penmount.dat source location, and 3) calibration database target destination.\
                              Example --iface eth0 /etc/penmount.dat /tmp/calibration.db'
                      )
    
    parser.add_option('--download',
                      action = 'callback',
                      callback = download_callback,
                      type = 'string',
                      nargs = 1,
                      help= 'Downloads calibration.db from Elektronix FTP Server.\
                              Example "--download /tmp/calibration.db" saves the calibration database to /tmp/calibration.db'
                      )
    
    parser.add_option('--upload',
                      action = 'callback',
                      callback = upload_callback,
                      type = 'string',
                      nargs = 1,
                      help= 'Uploads calibration.db to Elektronix FTP Server. \
                              Example "--upload /tmp/calibration.db" uploads /tmp/calibration.db to the FTP server.'
                      )
    
    parser.add_option('--dumb',
                      action = 'callback',
                      callback = dumb_callback,
                      type = 'string',
                      nargs = 3,
                      help = 'Automatically downloads calibration.db from Elektronix FTP server, \
                                adds calibration coordinates for eth0, and uploads the file back to FTP server. \
                                Username and passwords are passed as arguments. \
                                Example "--dumb myuser mysecretpassword ipaddress'
                      )

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error("incorrect number of arguments. Try --help")

if __name__ == '__main__':
    main()

    
    
    