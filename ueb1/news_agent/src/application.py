
import sys
import gi
from gi.repository import Gtk, GLib, Gio, Handy
from .main_window import MainWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="de.falsei.ueb1news",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        Handy.init()
    
    def do_startup(self):
        Gtk.Application.do_startup(self)
        GLib.set_application_name("News Agent")
        GLib.set_prgname("News Agent")

    def do_activate(self):
        window = self.props.active_window
        if not window:
            window = MainWindow(application=self)
        window.present()


def main(version):
    app = Application()
    return app.run(sys.argv)

