'''
======================================================================
PYTHON FOR DATA ACQUISITION                     VERSION: Beta
----------------------------------------------------------------------
DEVELOPER: ALEJANDRO CADENA                     RELEASE: 04.27.2021

FUNCTION: CAPTURE AND LOG UDP PACKAGES SENT BY A PLC CONTROLLER THRU
A SOCKET INSTANCE. EACH PACKAGE CAPTURE IS UP TO 462 BYTES.
======================================================================
'''
import os
import sys
from datetime import datetime
import scapy.all

mit_licence = '''
MIT License
Copyright (c) 2021 Alejandro Cadena Ramirez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
def daq(nic, port):
    packet = scapy.all.sniff(iface=nic, count=1, filter=port)
    data = packet[0].lastlayer()
    payload = bytes(data).hex()
    return payload


print('Python for Data Acquisition                                                    Version: Beta')
print('=============================================================================================')
print(mit_licence)
print('=============================================================================================')
print(scapy.all.show_interfaces())
nidx = int(input('Select the index for the interface to be used:'))
nport = input('Port number that Data Server is connected:')
desc = input('Description for data file:')

##GET THE NETWORK INTERFACE THAT IS USED TO CAPTURE UDP DATAGRAMS & PORT CONNECTED TO SOURCE
nic = scapy.all.dev_from_index(nidx)
port = 'port ' + nport

##GET FILE NAME WITH DATA LOGGED
tstamp = datetime.now()
fname = 'CLX-DAQ ' + desc + tstamp.strftime(' %d-%b-%Y_%H%M%S') + '.txt'

##CHECK FOR DATA DIRECTORY
dpath = os.getcwd() + '\\Data'
if not(os.path.exists(dpath)):
    os.mkdir('Data')

##GET ABSOLUTE PATH TO DATA FILE
file = dpath + '\\' + fname

##CLEAR CONSOLE BEFORE THE CAPTURE
if os.name == 'nt':
    os.system('cls')
elif os.name == 'posix':
    os.system('clear')

try:
    with open(file, mode= 'w', encoding= 'utf-8') as f:
        f.write('CLX PYTHON DATA ACQUISITION FILE - TIMESTAMP: ' + str(tstamp) + "\n")
        print('Recording data into file: {} .....'.format(fname))
        print('To stop recording press: Ctl+C')
        while True:
            capture = daq(nic.data['description'], port)
            f.write(capture)
            f.write("\n")

except:
    f.close()
    print('Data file was closed .....')
    sys.exit(1)




