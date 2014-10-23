import globals
import yaml
import os
import transparency
import desktops
import events
import menu
import settings
import var_dump
from gi.repository import Gtk, Gdk, cairo, Wnck as wnck

class Create(Gtk.Window):
    def __init__(self):
        super(Create, self).__init__()
        self.events = events.Events()
        self.set_name('MyWindow')
        self.set_resizable(False)
        self.menu = menu.Menu()
        self.menu.set_window(self)
        self.menu.create_menu()


        self.settings = settings.Handler()
        self.settings.reloaded()

        self.set_decorated(False)
        self.set_position(1)
        self.set_title(globals.APP_NAME)
        self.set_border_width(0)
        self.set_opacity(0)
        #self.resize(800,600)
        #self.fullscreen()

        table = Gtk.Table(3,6,False)
        self.new_desktop_list = desktops.Create().get_desktops()

        # Create a new notebook, place the position of the tabs
        self.notebook = Gtk.Notebook()
        self.notebook.set_show_border(False)
        self.notebook.set_tab_pos(2)
        self.add_desktops()

        table.attach(self.notebook, 0,6,0,1)

        transparency.Transparent.makeTransparent(table)
        self.add(table)

        self.connect("destroy", Gtk.main_quit)
        self.connect("button_press_event", self.events.menu_popup)
        self.connect("visibility_notify_event", self.events.window_visibility_event)
        self.connect("key-release-event", self.events.on_key_release)
        #self.show_menu()
        self.show_all()

    def add_desktops(self):

        wnck_screen = wnck.Screen.get_default()

        while Gtk.events_pending():
            Gtk.main_iteration()

        wnck_screen.force_update()
        wnck_list = wnck_screen.get_windows()

        for key, desktop in self.new_desktop_list.iteritems():

            bufferf = "%s" % (desktop['title'])

            frame = Gtk.Frame()
            transparency.Transparent.makeTransparent(frame)
            i = 1
            VButtonBox = Gtk.HBox()
            mainBox = Gtk.VBox(False)

            #VButtonBox.set_layout(gtk.BUTTONBOX_START);
            for window in desktop['windows'].iteritems():

                # convert hex id to int for comparison
                id_int = int(window[0],16)
                wnckwindow = ''

                # find matching wnck window
                for wnck_window in wnck_list:
                    if id_int == wnck_window.get_xid():
                        wnckwindow = wnck_window
                        break

                btn = self.add_button(window[1], window[0], wnckwindow)
                btn.set_size_request(100,100)

                VButtonBox.pack_start(btn, False, False, 2)
                i = i + 1

            mainBox.pack_start(VButtonBox, False, False, False)

            frame.add(mainBox)

            frame.set_shadow_type(Gtk.ShadowType.NONE)
            frame.show()

            label = Gtk.Label(bufferf)
            
            self.notebook.append_page(frame, label)

    def add_button(self, win_title, win_id, wnck_window):
        image = Gtk.Image()
        image.set_from_pixbuf(wnck_window.get_icon())

        btn1 = Gtk.Button('')
        btn1.set_tooltip_text (win_title);
        btn1.set_always_show_image(True)
        btn1.set_image(image)
        btn1.win_id = win_id
        btn1.connect("clicked", self.events.on_clicked)
        return btn1
