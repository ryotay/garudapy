
### PLAY WITH GARUDA.PY ###

# VERSION: 0.1.2
# COMPATIBLE: Garuda_Update_Jan13

# PREPARATION
# open garuda.ini and replace <--SET PATH-->
# with current working directory (3 places)
# $ vi garuda.ini

# Run python in the directory where you put garuda.py
# $ python

# CONNECT
import garuda
sock = garuda.connect()

# REGISTER GADGET
ret = garuda.register(sock)
print ret.get('result')

# GET COMPATIBLE GADGET LIST
ret = garuda.getlist(sock, 'xml', 'sbml')
print ret.get('gadgets')

# SEND DATA
ret = garuda.activate(sock)
print ret.get('result')
import os # to get current working directory path
ret = garuda.send(sock, os.getcwd()+'/test.xml', 'Demo Gadget A', '07d7932d-6337-42c1-acf5-746a617b2e47')
print ret.get('result')

# LOAD DATA
ret = garuda.activate(sock)
print ret.get('result')
ret = garuda.load(sock)
# gadget is waiting for load data request...
# send data to this gadget from other gadgets.
print ret.get('path')

exit()