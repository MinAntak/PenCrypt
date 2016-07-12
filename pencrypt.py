#!/usr/bin/env python3

import subprocess
import gi
import sys
import os
import getopt
from create import NewContainer
from open import Open
from automount import AutoMount
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class OknoGlowne(Gtk.Window):
    def __init__(self):
        super(OknoGlowne, self).__init__()

        self.set_title("PenCrypt")
        self.set_size_request(350, 300)
        self.connect("destroy", Gtk.main_quit)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        title = Gtk.Label("Hidden volumes manager")
        title.set_size_request(250, 25)
        self.fixed.put(title, 50, 20)

        title2 = Gtk.Label("Select:")
        title2.set_size_request(250, 25)
        self.fixed.put(title2, 50, 60)

        newbutton = Gtk.Button("Create new volume")
        newbutton.connect("clicked", self.on_clicked_new)
        newbutton.set_size_request(250, 25)
        self.fixed.put(newbutton, 50, 100)

        open = Gtk.Button("Open volume")
        open.connect("clicked", self.on_clicked_open)
        open.set_size_request(250, 25)
        self.fixed.put(open, 50, 150)

        automount = Gtk.Button("AutoMount")
        automount.connect("clicked", self.on_clicked_automount)
        automount.set_size_request(250, 25)
        self.fixed.put(automount, 50, 200)

        dismount = Gtk.Button("Dismount all")
        dismount.connect("clicked", self.on_clicked_dismount)
        dismount.set_size_request(250, 25)
        self.fixed.put(dismount, 50, 250)

        self.show_all()

    def on_clicked_new(self, widget):
        NewContainer()

    def on_clicked_open(self, widget):
        Open()

    def on_clicked_automount(self, widget):
        AutoMount()

    def on_clicked_dismount(self, widget):
        p=subprocess.Popen(["veracrypt", "-d"])
        os.waitpid(p.pid, 0)
        p1 = subprocess.Popen(["sudo", "umount", "/mnt/USB"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.waitpid(p1.pid, 0)


sys.argv
total = len(sys.argv)
cmdargs = str(sys.argv)
if(len(sys.argv) > 1):
    if(sys.argv[1] == "-a"):
        AutoMount()
        Gtk.main()
    else:
        OknoGlowne()
        Gtk.main()
else:
    OknoGlowne()
    Gtk.main()

