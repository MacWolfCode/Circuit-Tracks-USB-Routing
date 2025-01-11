I wanted my digital piano to always be controlling whatever the selected track on my circuit was. 
That way I can super easily switch between loop the two Circuit synths, my Microfreak, and playing my 
actual Digital Piano. 

My Circuit Tracks, my Arturia Microfreak and my Yamaha P-125 are connected to my computer by USB. there's already a midi route
set up for the Circuit to control my Yamaha on MIDI channel 4 over USB. I'm on ubuntu so I just used aconnect.

My Circuit is connected to my Microfreak with standard MIDI cables.  

I used threads and I set up a listener for the midi message a circuit sends when it switches its selected
track. I store which track and therefore what midi channel my digital piano should be sending messages to. 
Then, everytime my piano sends a MIDI signal over USB, my program intercepts it, changes the message's channel
to whatever is currently selected on the Circuit and forwards the message along to the Circuit. 

This way I can just leave my Yamaha on it's default channel and have my computer do all the work for me (Switching 
channels on my digital piano is a total pain).

**Also, because I don't know how to get the circuit to repeat these messages to the external equipment. I am just
simultaneously forwarding the MIDI messages to my piano and my Microfreak so that sound actually comes out of them. 
