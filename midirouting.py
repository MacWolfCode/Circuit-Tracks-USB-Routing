import mido
import threading
import sys
# List available input ports

current_midi_channel = 0
channel_lock = threading.Lock()
tracks_port_name = ""
yamaha_port_name = ""
microfreak_port_name = ""
# Find the appropriate port names
print("Available MIDI input ports:")
for port in mido.get_input_names():
	print(f" - {port}")
	if "Circuit Tracks" in str(port):
		tracks_port_name = str(port)
	if "Digital Piano" in str(port):
		yamaha_port_name = str(port)
	if "Arturia MicroFreak" in str(port):
		microfreak_port_name = str(port)
def listen_for_channel_switch(input_port_name):
	"""
	Listens for a Specific SysEx message from the Circuit Tracks that's sent whenever a
	new track is pressed on the circuit, meaning my piano should send it's MIDI messages 
	to said channel
	It uses the global tracks_port name variable
	"""
	global current_midi_channel
	try:
		with mido.open_input(input_port_name) as input_port:
			print(f"Listening for MIDI messages on {tracks_port_name}...")
			for msg in input_port:
				if msg.type == "note_on":
					print(f"Received: {msg}")
				if msg.type == "sysex":
					#From my initial look this is the sysex message that means new selected track
					if msg.data[:7] == (0, 32, 41, 1, 100, 4, 3):
						new_midi_channel = msg.data[7]

						with channel_lock: # Update the shared current_channel safely
							current_midi_channel = new_midi_channel
						print(f"Switching MIDI Channel to {new_midi_channel + 1}")
	except IOError as e:
		print(f"Error: Unable to open MIDI port. Details: {e}")

def route_messages(yamaha, tracks, microfreak):
	"""
		Route the midi messages from my yamaha to my circuit tracks intercepting and changing
		the channel attribute so I can just keep my yamaha's transmitting channel the same
	"""
	global current_channel
	with mido.open_input(yamaha) as input_port, \
		 mido.open_output(tracks) as tracks_output_port, \
		 mido.open_output(yamaha) as yamaha_output_port, \
		 mido.open_output(microfreak) as microfreak_output_port:
		print(f"Routing MIDI messages from {yamaha} to {tracks}, {microfreak}, and {yamaha}...")
		for msg in input_port:
			if msg.type in ['note_on', 'note_off', 'control_change', 'program_change', 'pitchwheel']:
				# The sound feels weaker when I play with my digital piano so I'm gonna adjust it a bit
				if msg.type == 'note_on':
					msg.velocity = min(int(msg.velocity * 1.25), 127)
				with channel_lock:
					msg.channel = current_midi_channel
				tracks_output_port.send(msg)
				microfreak_output_port.send(msg)
				yamaha_output_port.send(msg)
				print(f"Routed: {msg}")

# Create threads
sysex_listener_thread = threading.Thread(target=listen_for_channel_switch, args=(tracks_port_name,))
routing_thread = threading.Thread(target=route_messages, args=(yamaha_port_name, tracks_port_name, microfreak_port_name))

# Start Threads
sysex_listener_thread.start()
routing_thread.start()

# Join threads to keep the program running
sysex_listener_thread.join()
routing_thread.join()