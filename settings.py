from gi.repository import Gtk, Gdk
import ConfigParser
import os

class Handler():
    def __init__(self):
        CURRENT_DIR = os.path.dirname(__file__)
        self.cfg_file_name = os.path.join(CURRENT_DIR, 'settings')
        self.cfg_parser = ConfigParser.ConfigParser()
        self.cfg_parser.readfp(open(self.cfg_file_name))

    def update_file(self):
        with open(self.cfg_file_name,"wb") as cfg_file:
            self.cfg_parser.write(cfg_file)

    def get_theme(self):
        return self.cfg_parser.get("settings", "theme")

    def set_theme(self, theme):
        self.cfg_parser.set("settings", "theme", theme)
        self.update_file()

    def reloaded(self):
        if self.get_theme():
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(self.get_theme())
            screen = Gdk.Screen.get_default()
            Gtk.StyleContext.add_provider_for_screen(screen, css_provider,
                     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


