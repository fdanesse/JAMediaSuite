
public class BalanceWidget : Gtk.EventBox{
    /*
    __gsignals__ = {
    'balance-valor': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
        (gobject.TYPE_FLOAT, gobject.TYPE_STRING))}
    */

    private ToolbarcontrolValores brillo = new ToolbarcontrolValores("Brillo");
    private ToolbarcontrolValores contraste = new ToolbarcontrolValores("Contraste");
    private ToolbarcontrolValores saturacion = new ToolbarcontrolValores("Saturación");
    private ToolbarcontrolValores hue = new ToolbarcontrolValores("Matíz");
    private ToolbarcontrolValores gamma = new ToolbarcontrolValores("Gamma");

    public BalanceWidget(){

        Gtk.AttachOptions flags = Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL;
        Gtk.Table tabla = new Gtk.Table(5, 1, true);

        tabla.attach(this.brillo, 0, 1, 0, 1, flags, flags, 0, 0);
        tabla.attach(this.contraste, 0, 1, 1, 2, flags, flags, 0, 0);
        tabla.attach(this.saturacion, 0, 1, 2, 3, flags, flags, 0, 0);
        tabla.attach(this.hue, 0, 1, 3, 4, flags, flags, 0, 0);
        tabla.attach(this.gamma, 0, 1, 4, 5, flags, flags, 0, 0);

        this.add(tabla);
        this.show_all();

        this.set_size_request(150, -1);
        /*
        self.brillo.connect('valor', self.__emit_senial, 'brillo')
        self.contraste.connect('valor', self.__emit_senial, 'contraste')
        self.saturacion.connect('valor', self.__emit_senial, 'saturacion')
        self.hue.connect('valor', self.__emit_senial, 'hue')
        self.gamma.connect('valor', self.__emit_senial, 'gamma')
        */
    }
    /*
    def __emit_senial(self, widget, valor, tipo):
        self.emit('balance-valor', valor, tipo)

    def set_balance(self, brillo=50.0, contraste=50.0,
        saturacion=50.0, hue=50.0, gamma=10.0):
        if saturacion != None:
            self.saturacion.set_progress(saturacion)
        if contraste != None:
            self.contraste.set_progress(contraste)
        if brillo != None:
            self.brillo.set_progress(brillo)
        if hue != None:
            self.hue.set_progress(hue)
        if gamma != None:
            self.gamma.set_progress(gamma)
    */
}


public class ToolbarcontrolValores : Gtk.Toolbar{
    /*
    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}
    */

    private SlicerBalance escala = new SlicerBalance();
    private Gtk.Frame frame = new Gtk.Frame("");
    private Gtk.Label label = new Gtk.Label("");

    public ToolbarcontrolValores(string titulo){

        Gtk.ToolItem item2 = new Gtk.ToolItem();
        item2.set_expand(true);

        this.frame.set("label_widget", this.label);
        this.label.set_text(titulo);
        this.frame.set("label_xalign", 0.5);
        this.frame.set("label_valign", 0.5);
        this.frame.set_border_width(4);

        Gtk.EventBox event = new Gtk.EventBox();
        event.set_border_width(4);
        event.add(this.escala);
        this.frame.add(event);
        this.frame.show_all();

        item2.add(this.frame);
        this.insert(item2, -1);
        this.show_all();

        //self.escala.connect("user-set-value", self.__user_set_value)
    }
    /*
    def __user_set_value(self, widget=None, valor=None):
        if valor > 99.4:
            valor = 100.0
        self.emit('valor', valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))

    def set_progress(self, valor):
        self.escala.set_progress(valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))
    */
}


public class SlicerBalance : Gtk.EventBox{
    /*
    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}
    */

    private Gtk.Scale escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    public Gtk.Adjustment ajuste = new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0);

    public SlicerBalance(){

        this.escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, this.ajuste);
        this.escala.set_digits(0);
        this.escala.set_draw_value(false);

        this.add(this.escala);
        this.show_all();

        //self.escala.connect('user-set-value', self.__emit_valor)
        this.escala.value_changed.connect (() => {
			stdout.printf ("%f\n", this.escala.get_value ());
			//self.emit("user-set-value", valor)
		});
    }
    /*
    def set_progress(self, valor=0.0):
        self.escala.ajuste.set_value(valor)
        self.escala.queue_draw()
    */
}


/*
class BalanceBar(gtk.HScale):

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.ancho, self.borde = (7, 10)

        icono = os.path.join(BASE_PATH, "Iconos", "controlslicer.svg")
        self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 16, 16)

        self.connect("expose_event", self.__expose)

        self.show_all()

    def __expose(self, widget, event):
        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        gc.set_rgb_fg_color(get_colors("window"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        gc.set_rgb_fg_color(get_colors("drawingplayer"))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(get_colors("naranaja"))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        yimage = yy + hh / 2 - imgh / 2

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
            imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True

    def do_motion_notify_event(self, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """
        if event.state == gtk.gdk.MOD2_MASK | gtk.gdk.BUTTON1_MASK:
            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)
            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)

*/
