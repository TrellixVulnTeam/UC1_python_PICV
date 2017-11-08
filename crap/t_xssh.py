#!/usr/bin/env python3
from pexpect import pxssh
import re
import getpass
try:
    s = pxssh.pxssh()
    password = 'utDbTpgBiaCJmqKevwzY8E7L'
    username = 'root'
    hostname = '10.124.15.68'
    s.login(hostname, username, password)
    s.sendline('show version') 
    s.expect('found')
    string = str(s.before + s.after)
    t = re.sub(r'\\r',r'', string)[2:-1]
    t1 = re.sub(r'\\n', r'\n', t)
    print(t1)
    s.logout()
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)
