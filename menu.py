from gi.repository import Gtk, Gdk
import subprocess
import collections
import os
import settings

class Menu(Gtk.Menu):
    def __init__(self):
        super(Menu, self).__init__()
        self.settings = settings.Handler()

        themes = {}

        p1 = subprocess.Popen(('find', '/usr/share/themes', '-type', 'd', '-name', 'gtk-3.0'), stdout=subprocess.PIPE)
        (sout,serr) = p1.communicate()

        for line in sout.split('\n'):
            if not line:
                continue

            name = line.split('/')[4]
            themes[name] = line + '/gtk.css'

        self.themes = themes


    def set_window(self, window):
        self.window = window

    def create_menu(self):
        themesMenu = Gtk.Menu()
        themes = Gtk.MenuItem("Themes")
        themes.set_submenu(themesMenu)
        themeMenu = Gtk.MenuItem("Faianca")
        themeMenu.connect("button_press_event", self.theme_clicked, '')

        themesMenu.append(themeMenu)

        for theme, path in self.themes.iteritems():
            themeMenu = Gtk.MenuItem(theme)
            themeMenu.connect("button_press_event", self.theme_clicked, path)
            themesMenu.append(themeMenu)

        about = Gtk.MenuItem("About")
        about.connect("button_press_event", self.about)
        self.append(themes)
        self.append(about)
        self.show_all()

    def theme_clicked(self, widget, event, path):

        self.settings.set_theme(path)

        if path:
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(path)
            screen = Gdk.Screen.get_default()
            Gtk.StyleContext.add_provider_for_screen(screen, css_provider,
                     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        else:
            Gtk.main_quit()


    def about(self, widget, event):
        about = Gtk.AboutDialog()
        about.set_position(1)
        about.set_program_name("WindowsListGui")
        about.set_version("0.1")
        about.set_copyright("(c) Jorge Meireles")
        about.set_comments("WindowListGUI for Linux")
        about.set_website("http://www.ponteiro-team.com")
        about.run()
        about.destroy()