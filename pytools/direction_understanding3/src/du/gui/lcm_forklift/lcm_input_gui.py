#!/usr/bin/env python

import gtk
import lcm
import time
from arlcm.comment_t import comment_t

lc = lcm.LCM()

# otherwise, pop up a gtk window
dlg = gtk.Dialog ("Direction Input", 
        buttons = (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
            gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

textview = gtk.TextView ()
label = gtk.Label("140 characters remaining")

dlg.vbox.pack_start(textview, True, True)
dlg.vbox.pack_start(label, False, True)
dlg.vbox.show_all()
dlg.set_default_size(400, 150)
textview.set_wrap_mode(gtk.WRAP_WORD)
textview.grab_focus()

def on_key_press(widget, event):
    if gtk.gdk.keyval_name(event.keyval) == "Return" and not \
            (event.state & gtk.gdk.SHIFT_MASK):
        dlg.response (gtk.RESPONSE_ACCEPT)

def on_text_changed(buffer):
    text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
    if len(text) > 140:
        text = text[:140]
        buffer.set_text(text)
    label.set_text("%d characters remaining" % (140 - len(text)))

textview.get_buffer().connect("changed", on_text_changed)

textview.set_events(gtk.gdk.KEY_PRESS_MASK)
textview.connect("key-press-event", on_key_press)

response = None
while response != gtk.RESPONSE_REJECT:
    response = dlg.run()

    if response == gtk.RESPONSE_ACCEPT:
        tb = textview.get_buffer()
        text = tb.get_text(tb.get_start_iter(), tb.get_end_iter())
        msg = comment_t()
        msg.utime = int(time.time() * 1000000)
        msg.comment = text

        print "Publishing DIRECTION_INPUT:",text
        lc.publish("DIRECTION_INPUT", msg.encode())

dlg.dispose()
