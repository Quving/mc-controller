import os, gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class McController(Gtk.Widget):

    def __init__(self):
        Gtk.Widget.__init__(self)

        # Button 1
        self.button1 = Gtk.Button(label="Click Here")
        self.button1.connect("clicked", self.on_button_clicked)
        self.add(self.button1)

        # Button 2


    def on_button_clicked(self, widget):
        print("Hello World")
        os.system("ls")
        os.system("gnome-terminal -e 'bash -c \"sudo apt-get update; exec bash\"'")
