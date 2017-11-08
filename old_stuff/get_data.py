#!/usr/bin/env python 

from lxml import etree
from jnpr.junos import Device
import getpass

PW = getpass.getpass("Password: ") 

d = {'SG1_MX1': '10.225.128.1'}

for i in d:
  i = Device(host=d[i],user='cne',password=PW)
  try:
    i.open()
  except Exception as err:
    print('Error: ' + repr(err))
    continue
  response = i.rpc.get_chassis_inventory(normalize=True) 
  print etree.dump(response)
  i.close()
