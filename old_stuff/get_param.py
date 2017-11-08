#!/usr/bin/env python 


import paramiko
import time
import getpass
import os


paramiko.util.log_to_file("filename.log")

#UN = raw_input("Username : ")
PW = getpass.getpass("Password: ") 


fn = 'CLC_output.txt'
f = open(fn, 'w')                                                                                              
f.close()   

d={ 'NY1_EFW': '10.254.7.1',
    'UC1_EFW': '10.254.124.1',
    'CA3_EFW': '10.254.104.1',
    'CA2_EFW': '10.254.59.1',
    'CA1_EFW': '10.254.54.1',
    'DE3_EFW': '10.254.186.1',
    'AU1_EFW': '10.254.164.1',
    'SG1_EFW': '10.254.134.1',
    'UT1_EFW': '10.254.98.1',
    'GB3_EFW': '10.254.109.1',
    'DE1_EFW': '10.254.114.1',
    'VA2_EFW': '10.254.170.1',
    'GB1_EFW': '10.254.64.1',
    'VA1_EFW': '10.254.129.1',
    'IL1_EFW': '10.254.9.1',
    'WA1_EFW': '10.254.88.1',
    'AU1_CFW': '10.164.15.1',
    'CA1_CFW': '10.54.15.1',
    'CA2_CFW': '10.59.15.1',
    'CA3_CFW': '10.104.15.1',
    'DE1_CFW': '10.114.15.1',
    'DE3_CFW': '10.186.15.1',
    'GB1_CFW': '10.64.15.1',
    'GB3_CFW': '10.109.15.1',
    'IL1_CFW': '10.98.100.1',
    'NE1_CFW': '10.239.8.4',
    'NY1_CFW': '10.78.15.1',
    'SG1_CFW': '10.134.8.4',
    'UC1_CFW': '10.124.15.1',
    'UT1_CFW': '10.98.15.1',
    'VA1_CFW': '10.129.15.1',
    'VA2_CFW': '10.170.15.1',
    'WA1_CFW': '10.88.15.1',
    'AU1_MX1': '10.226.32.1',
    'AU1_MX2': '10.226.32.2',
    'CA1_MX1': '10.226.64.1',
    'CA1_MX2': '10.226.64.2',
    'DE3_MX1': '10.226.0.1',
    'DE3_MX2': '10.226.0.2',
    'GB1_MX1': '10.224.128.1',
    'GB1_MX2': '10.224.128.2',
    'GB3_MX1': '10.224.160.1',
    'GB3_MX2': '10.224.160.2',
    'SG1_MX1': '10.225.128.1',
    'SG1_MX2': '10.225.128.2',
    'VA2_MX1': '10.226.96.1',
    'VA2_MX2': '10.226.96.2',
    'WA1_MX1': '10.226.128.1',
    'WA1_MX2': '10.226.128.2',
    }

d1={'SG1_MX1': '10.225.128.1','SG1_MX2': '10.225.128.2'}

# This loop get IPs of CFWs and EFW and does double SSH from CFW to EFW
for i in  d:
    cfw_ip = d[i]
    hn = i
    print cfw_ip
    print hn

    buf = '' 
    output = ''
	
    try:
         twrssh = paramiko.SSHClient()
         twrssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         twrssh.connect(cfw_ip, port=22, username='alex.chuvakov', password=PW)
         print "Connected sucessfully to %s" % hn
    except paramiko.AuthenticationException:
        print "Authentication failed when connecting to %s. Going to next site." % hn
        continue
    except:
        print "Could not SSH to %s, waiting for it to start. Going to next site" % hn
        continue

    remote = twrssh.invoke_shell()
    time.sleep(2)

    output = remote.recv(65000)
	
# This 'if' checks if we are in the BSD shell or in CLI

    if output.endswith(('% ', '%\t')):
        print('In shell')
        remote.send('cli ' + 'show chassis hardware \| display xml \| no-more \n')
        time.sleep(6)
        buf = remote.recv(65000)
    elif output.endswith('> '):
        print('In CLI')
        remote.send('show chassis hardware | display xml | no-more \n')
        time.sleep(6)
        buf = remote.recv(65000)
    else:
        print ('NO PROMT!, next loop')
        continue
	
	
    twrssh.close() 

    
    f = open(fn, 'a')
    f.write(hn)
    f.write(buf)
    f.close()


    

