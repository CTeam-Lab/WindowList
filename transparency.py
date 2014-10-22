import cairo

class Transparent:
    def __init__(self,*rgba):
        Transparent.makeTransparent(self)
        if len(rgba)>0:
            self.rgba=rgba[0]

    @staticmethod
    def expose (widget, event):

        if 'gtk.Layout' in str(type(widget)):
            cr=widget.bin_window.cairo_create()
        else:
            cr = widget.window.cairo_create()
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.rectangle(event.area)
        cr.fill()
        cr.set_operator(cairo.OPERATOR_OVER)
        try:
            widget.rgba
        except AttributeError:
            widget.rgba=(0.0,0.0,0.0,0.0)
        cr.set_source_rgba(*widget.rgba)
        cr.rectangle(event.area)
        cr.fill()

    @staticmethod
    def makeTransparent(widget,*rgba):
        return
        if len(rgba)>0:
            thing.rgba=rgba[0]
        widget.expose=Transparent.expose
        widget.set_app_paintable(True)
        screen = widget.get_screen()
        rgba = screen.get_rgba_colormap()
        widget.connect('expose-event', widget.expose)