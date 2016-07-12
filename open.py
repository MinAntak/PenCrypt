import subprocess
import gi
import os
import time
from threading import Thread
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Open(Gtk.Window):
    def __init__(self):
        super(Open, self).__init__()

        self.set_title("Open")
        self.set_size_request(400, 100)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        p = subprocess.check_output(["zenity", "--file-selection"], stderr=subprocess.PIPE)
        self.data = p.decode("utf-8")
        self.data = self.data.rstrip()

        self.field_text = Gtk.Label("Password:")
        self.field_text.set_size_request(100, 25)
        self.fixed.put(self.field_text, 20, 10)

        self.field = Gtk.Entry()
        self.field.set_visibility(False)
        self.field.set_size_request(200, 25)
        self.fixed.put(self.field, 150, 10)

        cancel = Gtk.Button("Cancel")
        cancel.connect("clicked", self.on_clicked_cancel)
        cancel.set_size_request(100, 25)
        self.fixed.put(cancel, 100, 50)

        ok = Gtk.Button("OK")
        ok.connect("clicked", self.on_clicked_ok)
        ok.set_size_request(100, 25)
        self.fixed.put(ok, 250, 50)

        self.show_all()

    def on_clicked_cancel(self, widget):
        self.destroy()

    def on_clicked_ok(self, widget):
        p = subprocess.Popen(
            ["veracrypt", self.data, "-p", self.field.get_text(), "--pim=0", "--keyfiles=", "--mount", "/mnt/veracryptAuto", "--protect-hidden=no", "--explore"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        thread = Thread(target = self.MyThread)
        thread.start()
        self.destroy()


    def MyThread(self):
        time.sleep(20)
        p1 = subprocess.Popen(
            ["veracrypt", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p1.communicate()
        err = err.decode("utf-8")
        err = err.rstrip();
        if (err != ""):
            p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Wrong password"], stderr=subprocess.PIPE)


