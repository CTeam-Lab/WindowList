import subprocess

from gi.repository import Gtk, Gdk

class Events():
    def __init__(self):
        pass

    def window_visibility_event(self, widget, event):
        ## if window is obscured
        if event.state == 2:
            self.close()

    def on_clicked(self, widget):
        self.switch_window(widget.win_id)

    def switch_window(self,win_id):
        subprocess.Popen(['wmctrl','-i','-a',win_id], stdout=subprocess.PIPE)
        self.close()

    def close(self):
        Gtk.main_quit()

    def on_key_release(self, widget, ev, data=None):
        # IF ESC is pressed
        if ev.keyval == 65307:
            self.close()