#!/usr/bin/env python3

import pexpect

def communicate_w_d(IP, UN, PN, command):
  with pexpect.spawn('ssh {1}@{0}'.format(IP, UN)) as s:
    #Waiting for the password prompt
    first_reply = s.expect([r'assword:', 'Are you sure you want to continue connecting'],timeout =  10)
    if first_reply == 0:
      s.sendline(PW)
      try:
        s.expect(r'\w+@\S+.*[$#>]', timeout = 10)
        prompt = str(s.after)[2:-1]
        print('We are here:\n' + prompt)
      except:
        print("We got the password prompt and sent the password, but the exception was thrown")
        exit()
    elif first_reply == 1:
      s.sendline('yes')
      try:
        s.expect(r'assword:', timeout = 10)
        s.sendline(PW)
        s.expect(r'[$#>]', timeout = 10)
        prompt = str(s.before + s.after)[2:-1]
        print('We are here:\n' + prompt)
      except:
        print("We got the password prompt and sent the password, but the exception was thrown")
        exit()
    else:
      print("No password prompt")
      exit()
    s.sendline(command)
    print("Sent: " + command)
    try:
      i = s.expect([r'assword:', r'[$#>%] '])
      if i == 0:
        mid_pass = input('Asked for a password, please type it: ')
        s.sendline(mid_pass)
        s.expect(r'[$#>%]')
        string = str(s.before + s.after)[2:-1]
        print(string)
      elif i == 1:
        string = str(s.before + s.after)[2:-1].split(r'\n')[-1]
        print('The prompt is: ' + string)
    except:
      string = str(s.before + s.after)[2:-1]
      print(string)
      print('No proper prompt, exiting')
      exit()
  

if __name__ == '__main__':
  IP = '10.124.15.68'
  UN = 'root'
  PW = 'utDbTpgBiaCJmqKevwzY8E7L'
  command = 'scp delete.me root@10.225.32.3:/'
  communicate_w_d(IP, UN, PW, command)
