# RAFTAR is the Ropey As Fuck TAlkback Resource.
# Copyright (c) 2017 Callum McLean
# Released under the MIT Licence - see LICENSE.md for details.

import sys
import argparse
import linphone

from raftar_rx import RAFTaRRX
from raftar_tx import RAFTaRTX

CODECS = ['PCMA', 'PCMU', 'OPUS', 'G722', 'SPEEX']
#CODECS=['PCMA']

def print_help():
    help_msg = "HCR RAFTaR: (c) Callum McLean 2017 \
    Usage: raftar_start.py sip_username sip_password [ -rx | -tx ]"

    print help_msg

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sip_username", help="Username for registering on a SIP service for the audio link.")
    parser.add_argument("sip_password", help="Password for registering on a SIP service for the audio link.")
    
    parser_rx_tx_group = parser.add_mutually_exclusive_group()
    parser_rx_tx_group.add_argument("-rx", action="store_const", dest="mode", const="rx", help="Starts a listening (station-end) instance.")
    parser_rx_tx_group.add_argument("-tx", action="store_const", dest="mode", const="tx", help="Starts a transmitting (field-end) instance.")

    args = parser.parse_args()
    if args.mode == "rx":
        raf_rx = RAFTaRRX(args.sip_username, args.sip_password, CODECS, 'ALSA: USB Audio Device',
                        'ALSA: USB Audio Device')
        raf_rx.run()
        print args
    elif args.mode == "tx":
        raf_tx = RAFTaRTX(args.sip_username, args.sip_password, CODECS, 'ALSA: USB Audio Device',
                        'ALSA: USB Audio Device')
        raf_tx.run()
        print args
