import linphone
import logging
import signal
import time
import sys
import json
import urllib2

class RAFTaRRX:
	def __init__(self, user='', passwd='', whitelist=[], snd_dev_pb='', snd_dev_cap=''):
		self.running = True
		self.whitelist = whitelist
		callbacks = {
			'call_state_changed': self.call_state_changed
		}
		self.codecs = ['PCMA', 'PCMU', 'OPUS', 'G722', 'SPEEX']

		logging.basicConfig(level=logging.INFO)
		signal.signal(signal.SIGINT, self.on_sigint)
		linphone.set_log_handler(self.log_handler)
		
		self.core = linphone.Core.new(callbacks, None, None)
		self.core.max_calls = 1
		self.core.echo_cancellation_enabled = True
		self.core.video_capture_enabled = False
		self.core.video_display_enabled = False
		self.core.stun_server = 'stun.linphone.org'
		self.core.firewall_policy = linphone.FirewallPolicy.PolicyUseIce

		if snd_dev_pb: self.core.playback_device = snd_dev_pb
		if snd_dev_cap: self.core.capture_device = snd_dev_cap

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
		if state == linphone.CallState.IncomingReceived:
			incoming_uri = call.remote_address.as_string_uri_only()
			logging.info("Incoming call from {0}".format(incoming_uri))
			if call.remote_address.as_string_uri_only() in self.whitelist:
				params = core.create_call_params(call)
#				params.record_file = "/home/pi/recording_{0}.wav".format(time.strftime("%y-%m-%d %H%M%S"))
				params.audio_bandwidth_limit = 128
				core.accept_call_with_params(call, params)
#				call.start_recording()
				logging.info("Call accepted")
			else:
				core.decline_call(call, linphone.Reason.Declined)
				logging.info("Call declined: caller not in whitelist")
				chat_room = core.get_chat_room_from_uri(self.whitelist[0])
				msg = chat_room.create_message(call.remote_address_as_string + ' tried to call')
				chat_room.send_chat_message(msg)

	def configure_sip_account(self, username, password):
		proxy_cfg = self.core.create_proxy_config()
		addr = linphone.Address.new("sip:{0}@sip.linphone.org".format(username))
		proxy_cfg.identity_address = addr
		proxy_cfg.server_addr = "sip:sip.linphone.org;transport=tls"
		proxy_cfg.register_enabled = True
		self.core.add_proxy_config(proxy_cfg)
		auth_info = self.core.create_auth_info(username, None, password, None, None, 'sip.linphone.org')
		self.core.add_auth_info(auth_info)

	def run(self):
		while self.running:
			self.core.iterate()
			time.sleep(0.03)

username = sys.argv[1]
password = sys.argv[2]

print "Getting updated whitelist"
resp = urllib2.open("https://raw.githubusercontent.com/calmcl1/hcr-raftar/master/whitelist")
body = resp.read()
whitelist = json.loads(body)["whitelist"]
			
raf = RAFTaRRX(username, password, whitelist, 'ALSA: USB Audio Device',
		'ALSA: USB Audio Device')

raf.run()
