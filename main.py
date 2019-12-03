#!/usr/bin/python
import os
import signal
from gi.repository import Gtk, AppIndicator3, GLib


# Status:       Connected
# Time:         7:01:55
# IP:           209.58.185.232
# Server:       HK#2
# Features:     Normal
# Protocol:     UDP
# Kill Switch:  Disabled
# Country:      Hong Kong
# City:         Hong Kong
# Load:         31%


class IndicatorProtonVPN(object):

    def __init__(self):
        self.app = AppIndicator3.Indicator.new(
            'indicator-protonvpn', "network-offline",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.app_menu = Gtk.Menu()
        self.quit_button = Gtk.MenuItem('quit')
        self.quit_button.connect('activate', lambda *args: Gtk.main_quit())
        self.app_menu.append(self.quit_button)
        self.app.set_menu(self.app_menu)
        self.app_menu.show_all()
        self.app.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.update_label()


    def update_label(self):
        stream = os.popen('protonvpn s')
        stream_raw = stream.read()
        output = stream_raw.split("\n")

        if 'Disconnected' in output[0] or len(output) < 10:
          self.app.set_icon('network-offline')
          self.app.set_label('', '')
        else:
          server = output[3].split(':')[1].strip()
          protocol = output[5].split(':')[1].strip()
          load = output[9].split(':')[1].strip()
          time_partial = output[1].split(':')
          time = time_partial[1].strip() + "h " + time_partial[2].strip() + "m"

          self.app.set_icon('network-transmit-receive')
          self.app.set_label(server + " (" + load + ") " + time, '')
        
        GLib.timeout_add_seconds(1, self.set_app_label)

    def set_app_label(self):
        self.update_label()


ind = IndicatorProtonVPN()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()