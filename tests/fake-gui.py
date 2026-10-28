#!/usr/bin/python3
# Generated with AI for personal use. GPL-3.0-or-later.
# Synthetic desktop activation target; never talks to the OpenLogi agent.
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

app = Gtk.Application(application_id='org.openlogi.openlogi')

def activate(application):
    window = application.get_active_window()
    if window is None:
        window = Gtk.ApplicationWindow(application=application, title='Synthetic OpenLogi activation test')
        window.set_default_size(400, 200)
        window.set_child(Gtk.Label(label='Synthetic application. No hardware access.'))
    window.present()

app.connect('activate', activate)
app.run(None)
