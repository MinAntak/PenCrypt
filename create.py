import subprocess

import random
import gi
import os
import time
from filedata import FileData
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from threading import Thread

class NewContainer(Gtk.Window):
    def __init__(self):
        super(NewContainer, self).__init__()

        self.set_title("New")
        self.set_size_request(550, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        title = Gtk.Label("Create new volume:")
        title.set_size_request(250, 25)
        self.fixed.put(title, 50, 20)

        self.text1 = Gtk.Label("Filename:")
        self.text1.set_size_request(100, 25)
        self.fixed.put(self.text1, 20, 50)

        self.entry1 = Gtk.Entry()
        self.entry1.set_size_request(250, 25)
        self.fixed.put(self.entry1, 200, 50)

        self.text2 = Gtk.Label("Location:")
        self.text2.set_size_request(100, 25)
        self.fixed.put(self.text2, 20, 100)

        self.label2 = Gtk.Label("/")
        self.label2.set_size_request(100, 20)
        self.fixed.put(self.label2, 200, 100)


        self.button2 = Gtk.Button("Change")
        self.button2.connect("clicked", self.on_clicked_change)
        self.button2.set_size_request(30, 25)
        self.fixed.put(self.button2, 450, 100)

        self.text3 = Gtk.Label("Password:")
        self.text3.set_size_request(100, 25)
        self.fixed.put(self.text3, 20, 150)

        self.entry3 = Gtk.Entry()
        self.entry3.set_visibility(False)
        self.entry3.set_size_request(250, 25)
        self.fixed.put(self.entry3, 200, 150)

        self.text4 = Gtk.Label("Repeat password:")
        self.text4.set_size_request(100, 25)
        self.fixed.put(self.text4, 20, 200)

        self.entry4 = Gtk.Entry()
        self.entry4.set_visibility(False)
        self.entry4.set_size_request(250, 25)
        self.fixed.put(self.entry4, 200, 200)

        self.text5 = Gtk.Label("Encryption:")
        self.text5.set_size_request(100, 25)
        self.fixed.put(self.text5, 20, 250)

        self.radio5_1 = Gtk.RadioButton.new_with_label_from_widget(None, "AES")
        self.fixed.put(self.radio5_1, 200, 250)
        self.radio5_2 = Gtk.RadioButton.new_from_widget(self.radio5_1)
        self.radio5_2.set_label("serpent")
        self.fixed.put(self.radio5_2, 300, 250)
        self.radio5_3 = Gtk.RadioButton.new_from_widget(self.radio5_1)
        self.radio5_3.set_label("twofish")
        self.fixed.put(self.radio5_3, 400, 250)


        self.text6 = Gtk.Label("Size(MB):")
        self.text6.set_size_request(100, 25)
        self.fixed.put(self.text6, 20, 300)

        self.entry6 = Gtk.Entry()
        self.entry6.set_size_request(250, 25)
        self.fixed.put(self.entry6, 200, 300)

        self.text7 = Gtk.Label("File system:")
        self.text7.set_size_request(100, 25)
        self.fixed.put(self.text7, 20, 350)

        self.radio7_1 = Gtk.RadioButton.new_with_label_from_widget(None, "FAT")
        self.fixed.put(self.radio7_1, 200, 350)
        self.radio7_2 = Gtk.RadioButton.new_from_widget(self.radio7_1)
        self.radio7_2.set_label("ext4")
        self.fixed.put(self.radio7_2, 300, 350)
        self.radio7_3 = Gtk.RadioButton.new_from_widget(self.radio7_1)
        self.radio7_3.set_label("ext3")
        self.fixed.put(self.radio7_3, 400, 350)

        self.text8 = Gtk.Label("Create hidden volume?:")
        self.text8.set_size_request(100, 25)
        self.fixed.put(self.text8, 20, 400)

        self.radio8_1 = Gtk.RadioButton.new_with_label_from_widget(None, "Nie")
        self.fixed.put(self.radio8_1, 200, 400)
        self.radio8_2 = Gtk.RadioButton.new_from_widget(self.radio8_1)
        self.radio8_2.set_label("Tak")
        self.fixed.put(self.radio8_2, 300, 400)

        self.text9 = Gtk.Label("Hidden password:")
        self.text9.set_size_request(100, 25)
        self.fixed.put(self.text9, 20, 450)

        self.entry9 = Gtk.Entry()
        self.entry9.set_visibility(False)
        self.entry9.set_size_request(250, 25)
        self.fixed.put(self.entry9, 200, 450)

        self.text10 = Gtk.Label("Hidden size(MB):")
        self.text10.set_size_request(100, 25)
        self.fixed.put(self.text10, 20, 500)

        self.entry10 = Gtk.Entry()
        self.entry10.set_size_request(250, 25)
        self.fixed.put(self.entry10, 200, 500)

        cancel = Gtk.Button("Cancel")
        cancel.connect("clicked", self.on_clicked_cancel)
        cancel.set_size_request(100, 25)
        self.fixed.put(cancel, 250, 550)

        next = Gtk.Button("Next")
        next.connect("clicked", self.on_clicked_next)
        next.set_size_request(100, 25)
        self.fixed.put(next, 400, 550)

        self.show_all()

    def on_clicked_change(self, widget):
        p = subprocess.check_output(["zenity", "--file-selection", "--directory"],stderr=subprocess.PIPE)
        self.label2.set_text(p.decode("utf-8"))

    def on_clicked_cancel(self, widget):
        self.destroy()

    def _resolve_radio(self, master_radio):
        active = next((
            radio for radio in
            master_radio.get_group()
            if radio.get_active()
        ))
        return active.get_label()

    def on_clicked_next(self, widget):
        data = FileData()

        data.name = self.entry1.get_text()
        data.location = self.label2.get_text()
        data.password = self.entry3.get_text()
        data.encrypt = self._resolve_radio(self.radio5_1)
        data.size= self.entry6.get_text()
        data.system = self._resolve_radio(self.radio7_1)
        data.isHidden = self._resolve_radio(self.radio8_1)
        data.hiddenPassword = self.entry9.get_text()
        data.hiddenSize = self.entry10.get_text()
        if data.name=='':
            p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Wrong filename"],stderr=subprocess.PIPE)

        elif data.location=='':
            p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Wrong location"],stderr=subprocess.PIPE)

        elif data.password == '':
            p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Wrong password"],stderr=subprocess.PIPE)
        elif self.entry3.get_text() != self.entry4.get_text():
            p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Passwords don't matches"], stderr=subprocess.PIPE)
        elif data.size == '':
            p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Wrong size"], stderr=subprocess.PIPE)
        elif self._resolve_radio(self.radio8_1) == "Tak":
            if data.hiddenPassword == '':
                p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Wrong hidden password"], stderr=subprocess.PIPE)
            elif data.hiddenSize == '':
                p = subprocess.Popen(["zenity", "--error", "--title=Error", "--text='Wrong hidden size"], stderr=subprocess.PIPE)
            else:
                CreateNew(data)
                self.destroy()
        else:
            CreateNew(data)
            self.destroy()


class CreateNew(Gtk.Window):
    def __init__(self, data):
        super(CreateNew, self).__init__()

        self.set_title("Creating new volume")
        self.set_size_request(200, 200)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        self.text = Gtk.Label("Creating file: " + data.name)
        self.text.set_size_request(100, 25)
        self.fixed.put(self.text, 20, 50)

        self.spinner = Gtk.Spinner()
        self.fixed.put(self.spinner, 100, 100)
        self.spinner.start()
        self.show_all()
        thread = Thread(target=self.makeNew(data))
        thread.start()

    def makeNew(self, data):
        time.sleep(2)
        rand="a"
        for zm in range(320):
            number = random.randrange(100)
            rand += str(number)

        f = open("rand", 'w')
        f.write(rand)
        f.close()

        string = data.location.rstrip()
        string = string+'/'+data.name

        string2 = data.location.rstrip()
        string2 = string2+'/'+"pend.sec"
        with open('out', 'w') as f:
            p = subprocess.Popen(["veracrypt", "-c", string, "-p", data.password, "--hash", "sha512", "--pim=0", "--volume-type=Normal", "--keyfiles=", "--random-source=rand", "--force", "--encryption", data.encrypt, "--size", data.size+'M', "--filesystem", data.system], stdout=f, stderr=f)
        os.waitpid(p.pid, 0)

        f = open(string2, 'w')
        f.write(data.name)
        f.close()



        if(data.isHidden == "Tak"):
            with open('out', 'w+') as f:
                p = subprocess.Popen(
                    ["veracrypt", "-c", string, "-p", data.hiddenPassword, "--hash", "sha512", "--pim=0", "--volume-type=Hidden",
                     "--keyfiles=", "--random-source=rand", "--force", "--encryption",
                     data.encrypt, "--size", data.hiddenSize + 'M', "--filesystem", data.system], stdout=f, stderr=f)
            os.waitpid(p.pid, 0)

        p3 = subprocess.Popen(
            ["zenity", "--text-info", "--filename=out", "--title=Finish"], stderr=subprocess.PIPE)

        self.destroy()
