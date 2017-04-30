# RAFTAR is the Ropey As Fuck TAlkback Resource.
# Copyright (c) 2017 Callum McLean
# Released under the MIT Licence - see LICENSE.md for details.

import logging
import signal
import time

import linphone


class RAFTaRTX:

    def __init__(self, user, passwd, codecs, snd_dev_pb='', snd_dev_cap=''):
        self.running = True
        callbacks = {
            'call_state_changed': self.call_state_changed,
            'registration_state_changed': self.registration_state_changed
        }
        self.codecs = codecs

        logging.basicConfig(level=logging.INFO)
        signal.signal(signal.SIGINT, self.on_sigint)
        linphone.set_log_handler(self.log_handler)

        self.core = linphone.Core.new(callbacks, None, None)
        self.core.max_calls = 1
        self.core.echo_cancellation_enabled = False
        self.core.video_capture_enabled = False
        self.core.video_display_enabled = False
        self.core.stun_server = 'stun.linphone.org'
        self.core.firewall_policy = linphone.FirewallPolicy.PolicyUseIce

        if snd_dev_pb:
            self.core.playback_device = snd_dev_pb
        if snd_dev_cap:
            self.core.capture_device = snd_dev_cap

        for codec in self.core.audio_codecs:
            if codec.mime_type.upper() in self.codecs:
                self.core.enable_payload_type(codec, True)
                logging.info("Enabled codec: {0}".format(codec.mime_type))

                # Set bitrates as per EBU 3347
                if codec.mime_type == "PCMA":
                    self.core.set_payload_type_bitrate(codec, 64)
                elif codec.mime_type == "PCMU":
                    self.core.set_payload_type_bitrate(codec, 64)
                elif codec.mime_type == "G722":
                    self.core.set_payload_type_bitrate(codec, 64)
            else:
                self.core.enable_payload_type(codec, False)
                logging.info("Disabled codec: {0}".format(codec.mime_type))

        self.configure_sip_account(user, passwd)

    def on_sigint(self, signal, frame):
        self.core.terminate_all_calls()
        self.running = False

    def log_handler(self, level, msg):
        method = getattr(logging, level)
        method(msg)

    def call_state_changed(self, core, call, state, message):
        if state == linphone.CallState.End:
            logging.info("Call ended. Reason: {reason}".format(
                reason=call.reason))
        elif state == linphone.CallState.Connected:
            logging.info("Call connected.")
        elif state == linphone.CallState.Idle:
            self.start_call("sip:hcr-rx1@sip.linphone.org")

    def registration_state_changed(self, core, call, state, message):
        if state == linphone.RegistrationState.Ok:
            logging.info("Registration OK, starting first call...")
            self.start_call("sip:hcr-rx1@sip.linphone.org")



    def configure_sip_account(self, username, password):
        proxy_cfg = self.core.create_proxy_config()
        addr = linphone.Address.new(
            "sip:{0}@sip.linphone.org".format(username))
        proxy_cfg.identity_address = addr
        proxy_cfg.server_addr = "sip:sip.linphone.org;transport=tls"
        proxy_cfg.register_enabled = True
        self.core.add_proxy_config(proxy_cfg)
        auth_info = self.core.create_auth_info(
            username, None, password, None, None, 'sip.linphone.org')
        self.core.add_auth_info(auth_info)

    def start_call(self, call_address):
        logging.info("Attempting call...")
        params = self.core.create_call_params(None)
        #params.audio_bandwidth_limit = 128
        address = linphone.Address.new(call_address)
        self.call = self.core.invite_address_with_params(address, params)

    def run(self):
        while self.running:
            self.core.iterate()
            time.sleep(0.03)
