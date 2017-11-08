#!/usr/bin/env python

import paramiko
import getpass
import os
import time
import d_list
import sys

########################################################################################

def get_sysargv():

  message = 'Usage:\nnew-ssh.py --srx - for all srxs\nnew-ssh.py --mx  - for all mxs\nnew-ssh.py --efw - for all efws\nnew-ssh.py --cfw - for all cfws\nnew-ssh.py --lab or with no arg - for all labs\n\n\nThe default user is cne'

  if len(sys.argv)<2:
    devices = d_list.lab
    print('Working with all LAB devicess')
  elif len(sys.argv)>=2 and sys.argv[1] == '--srx':
    devices = d_list.efw
    devices.update(d_list.cfw)
    print('Working with the all SRX devicess')
  elif len(sys.argv)>=2 and sys.argv[1] == '--efw':
    devices = d_list.efw
    print('Working with the all EFW devicess')
  elif len(sys.argv)>=2 and sys.argv[1] == '--cfw':
    devices = d_list.cfw
    print('Working with the all CFW devicess')
  elif len(sys.argv)>=2 and sys.argv[1] == '--all':
    devices = d_list.efw
    devices.update(d_list.cfw)
    devices.update(d_list.mx)
    print('Working with the all Juniper devicess')
  elif len(sys.argv)>=2 and sys.argv[1] == '--mx':
    devices = d_list.mx
    print('Working with the all MX devicess')
  elif len(sys.argv)>=2 and sys.argv[1] == '--lab':
    devices = d_list.lab
    print('Working with the all LAB devicess')
  elif len(sys.argv)>=2 and sys.argv[1] == '--help':
    print(message)
    sys.exit(1)
  else:
    print(message)
    print len(sys.argv)
    sys.exit(1)
  return devices

##################################################################################################

def get_init_data():

  UN = 'cne'
  PW = getpass.getpass("Password for %s: "% UN) 

  fn = raw_input("Enter name of the destination file: ")

  my_Command = raw_input("Which command? Type here: ")

  init_data = {'username':UN, 'password':PW, 'fname':fn, 'command': my_Command}

  return init_data

###################################################################################################

def get_info(devices=d_list.lab, uname='cne', pword='nothing', fname='tmp.txt', command='exit'):

  try: os.remove(fname)
  except: pass

  paramiko.util.log_to_file("paramiko.log")

  for device in devices:
    with paramiko.SSHClient() as client:

      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
      try:
        client.connect(hostname=devices[device], username= uname, password= pword)
        print 'Connected to {}'.format(device)

      except Exception as var:
        print 'Something is wrong with {}: {}\n Going to next loop'.format(device, var)
        continue

    
      stdin, stdout, stderr = client.exec_command(command)
      with open(fname, 'a') as f:
        f.write('\n{}> {}\n'.format(device, command))
        f.write(stdout.read())
        f.write(stderr.read())
        f.close()

##################################################################################################

if __name__ == '__main__':

  devices = get_sysargv()

  init_data = get_init_data()

  get_info(devices, init_data['username'], init_data['password'], init_data['fname'], init_data['command'])

