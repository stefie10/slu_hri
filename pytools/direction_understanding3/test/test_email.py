import email

import lcm

def on_email_msg(channel, data):
    msg = email.message_from_string(data)
    print "received: [%s]" % msg.get_payload().strip()

lc = lcm.LCM()

lc.subscribe("EMAIL", on_email_msg)

print "waiting for EMAIL message via LCM"
while True:
    lc.handle()
