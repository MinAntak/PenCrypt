import subprocess
import gi
import os
import sys
import time
from threading import Thread
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AutoMount(object):
    def __init__(self):
        p1 = subprocess.Popen(
            ["veracrypt", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p1.communicate()
        err = err.decode("utf-8")
        err = err.rstrip()
        if os.path.exists("/mnt/USB/pend.sec"):
            print("Mounted")
            sys.exit()
        elif os.path.exists("/mnt/veracryptAuto"):
            sys.exit()
        elif (err==''):
            p = subprocess.Popen(["veracrypt", "-d"])
            os.waitpid(p.pid, 0)
            p1 = subprocess.Popen(["sudo", "umount", "/mnt/USB"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.waitpid(p1.pid, 0)

            sys.exit()
        else:
            with open('out', 'w') as f:
                p=subprocess.Popen(["lsblk", "-l", "-n", "-p", "-o", "NAME"], stdout=f)
            os.waitpid(p.pid, 0)
            with open('out') as f:
                content = f.read().splitlines()

            i = 0
            for dysk in content:
                p = subprocess.Popen(["sudo", "mount", dysk, "/mnt/USB", "-o", "umask=000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                os.waitpid(p.pid, 0)
                if os.path.exists("/mnt/USB/pend.sec"):
                    Open()
                    break
                p = subprocess.Popen(["sudo", "umount", "/mnt/USB"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                os.waitpid(p.pid, 0)
                i=i+1
            if i == content.__len__():
                sys.exit()


class Open(Gtk.Window):
    def __init__(self):
        super(Open, self).__init__()

        self.set_title("Open")
        self.set_size_request(400, 100)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

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
        p1 = subprocess.Popen(["sudo", "umount", "/mnt/USB"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.waitpid(p1.pid, 0)
        self.destroy()
        sys.exit()

    def on_clicked_ok(self, widget):
        with open('/mnt/USB/pend.sec') as f:
            content = f.read().splitlines()

        location="/mnt/USB/"+content[0]
        p3 = subprocess.Popen(
            ["veracrypt", location, "-p", self.field.get_text(), "--pim=0", "--keyfiles=", "--mount", "/mnt/veracrypt", "--protect-hidden=no", "--explore"])
        thread = Thread(target=self.MyThread)
        thread.start()
        self.destroy()

    def MyThread(self):
        time.sleep(20)
        p1 = subprocess.Popen(
            ["veracrypt", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p1.communicate()
        err = err.decode("utf-8")
        if (err != ""):
            p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Wrong password"], stderr=subprocess.PIPE)
            Open()
        else:
            sys.exit()