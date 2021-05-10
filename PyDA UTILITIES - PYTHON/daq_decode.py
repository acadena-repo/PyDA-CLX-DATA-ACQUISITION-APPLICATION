'''
======================================================================
PYTHON FOR DATA ACQUISITION                     VERSION: Beta
----------------------------------------------------------------------
DEVELOPER: ALEJANDRO CADENA                     RELEASE: 04.27.2021

FUNCTION: DECODE RAW DATA CAPTURED BY PyDA DATA ACQUISITION MODULE
ACCORDING WITH TELEGRAM DEFINITION CONFIGURATION FILE
======================================================================
'''
import os
import struct
from datetime import datetime
from pandas import DataFrame

def tlg(fname):
    path = os.getcwd() + '\\Telegram\\' + fname + '.txt'

    with open(path, mode='r', encoding='utf-8') as tlg_file:
        desc = tlg_file.readline()
        bcode = tlg_file.readline()

    return desc,bcode

def xfm_sint(braw):
    shex = ''.join(braw)

    return int(shex,16)

def xfm_int(braw, swp=0):
    if swp:
        shex = ''.join(braw[::-1])
    else:
        shex = ''.join(braw)

    return int(shex,16)


def xfm_dint(braw, swp=0):
    if swp:
        shex = ''.join(braw[::-1])
    else:
        shex = ''.join(braw)

    return int(shex, 16)


def xfm_real(braw, swp=0):
    shex = bytes.fromhex(''.join(braw))
    if swp:
        nfloat = struct.unpack('<f', shex)
    else:
        nfloat = struct.unpack('>f', shex)

    return nfloat[0]


def line_decode(rline, bcode):
    bline = [rline[x:x+2] for x in range(0, len(rline), 2)]
    data = []
    ixs, ixe = 0, 0

    for x in bcode:

        if x == '1':
            ixe += 1
            dxmf = bline[ixs:ixe]
            data.append(xfm_sint(dxmf))
        elif x == '2':
            ixe += 2
            dxmf = bline[ixs:ixe]
            data.append(xfm_int(dxmf,1))
        elif x == '3':
            ixe += 4
            dxmf = bline[ixs:ixe]
            data.append(xfm_dint(dxmf,1))
        elif x == '4':
            ixe += 4
            dxmf = bline[ixs:ixe]
            data.append(xfm_real(dxmf,1))
        ixs = ixe

    return data

def decoder(capture, telegram):
    cols,bcod = tlg(telegram)
    path = os.getcwd() + '\\Data\\' + capture + '.txt'
    df_data = []

    with open(path, mode='r', encoding='utf-8') as data:
        stamp = data.readline()

        while True:
            rline = data.readline()

            if not rline:
                break

            df_data.append(line_decode(rline, bcod))

    df_cols = cols.rstrip('\n').split(',')
    df = DataFrame(data=df_data, columns=df_cols)

    return df


if __name__ == '__main__':

    print('Python for Data Acquisition                                                    Version: Beta')
    print('=============================================================================================')
    print()
    daq_cap = input('Name of the file with the captured data: ')
    tlg_def = input('Name of the file with the Telegram Definition: ')

    ##CLEAR CONSOLE BEFORE THE CAPTURE
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')

    tstamp = datetime.now()
    path = os.getcwd() + '\\Data\\' + 'CLX-DAQ DATAFRAME ' + tstamp.strftime(' %d-%b-%Y_%H%M%S') + '.csv'

    print('Decoding raw data ....')
    df_export = decoder(daq_cap, tlg_def)
    df_export.to_csv(path_or_buf=path, index=False)
    print('Dataframe exported to: {0}'.format(path))




