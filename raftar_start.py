# RAFTAR is the Ropey As Fuck TAlkback Resource.
# Copyright (c) 2017 Callum McLean
# Released under the MIT Licence - see LICENSE.md for details.

import sys

import linphone

from raftar_rx import RAFTaRRX
from raftar_tx import RAFTaRTX

CODECS = ['PCMA', 'PCMU', 'OPUS', 'G722', 'SPEEX']

if __name__ == "__main__":

    mode = sys.argv[1].upper()
    username = sys.argv[2]
    password = sys.argv[3]

    if mode == "RX":
        raf_rx = RAFTaRRX(username, password, CODECS, 'ALSA: USB Audio Device',
                          'ALSA: USB Audio Device')
        raf_rx.run()
    elif mode == "TX":
        raf_tx = RAFTaRTX(username, password, CODECS, 'ALSA: USB Audio Device',
                          'ALSA: USB Audio Device')
        raf_tx.run()
