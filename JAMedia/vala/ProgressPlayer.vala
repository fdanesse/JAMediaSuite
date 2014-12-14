
public class ProgressPlayer : Gtk.EventBox{
    /*
    __gsignals__ = {
    "seek": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, )),
    "volumen": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}
    */

    private BarraProgreso barraprogreso = new BarraProgreso();
    private ControlVolumen volumen = new ControlVolumen();

    public ProgressPlayer(){

        /*
        self.volumen = ControlVolumen()
        */
        Gtk.Box hbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
        hbox.pack_start(this.barraprogreso, true, true, 0);
        hbox.pack_start(this.volumen, false, false, 0);

        this.add(hbox);
        /*
        self.barraprogreso.connect("user-set-value", self.__user_set_value)
        self.volumen.connect("volumen", self.__set_volumen)
        */
        this.show_all();
    }

    /*
    def __user_set_value(self, widget=None, valor=None):
        self.emit("seek", valor)

    def __set_volumen(self, widget, valor):
        self.emit('volumen', valor)
    */

    public void set_progress(double valor){
        this.barraprogreso.set_progress(valor);
    }
}


public class BarraProgreso : Gtk.EventBox{

    /*
    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}
    */

    private ProgressBar2 escala = new ProgressBar2();
    private double valor = 0.0;

    public BarraProgreso(){

        this.add(escala);
        this.show_all();

        //self.escala.connect('user-set-value', self.__emit_valor)
        this.set_size_request(-1, 24);
    }
    /*
    def __emit_valor(self, widget, valor):
        if self.valor != valor:
            self.valor = valor
            self.emit("user-set-value", self.valor)
    */

    public void set_progress(double valor){
        if (this.escala.presed){
            }
        else{
            if (this.valor == valor){
                }
            else{
                this.valor = valor;
                this.escala.ajuste.set_value(valor);
                this.escala.queue_draw();
                }
            }
    }
}


public class ProgressBar2 : Gtk.EventBox{

    private Gtk.Scale escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    public Gtk.Adjustment ajuste = new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0);
    public bool presed = false;
    //private int ancho = 10;
    //private int borde = 10;

    public ProgressBar2(){

        this.set_border_width(4);
        this.escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, this.ajuste);
        this.escala.set_digits(0);
        this.escala.set_draw_value(false);

        // FIXME: Implementar Dibujo con cairo
        //this.escala.draw.connect ((context) => {
        //    this.__expose(context);
		//});

        this.add(this.escala);
        this.show_all();

        /*
        icono = os.path.join(BASE_PATH, "Iconos", "controlslicer.svg")
        self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 24, 24)

        self.connect("motion-notify-event", self.__motion_notify_event)
        self.connect("expose_event", self.__expose)
        */
        this.escala.button_press_event.connect ((event) => {
            this.presed = true;
            return true;
            });

        this.escala.button_release_event.connect ((event) => {
            this.presed = false;
            return true;
            });
    }

    /*
    def __motion_notify_event(self, widget, event):
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

    def __expose(self, widget, event):
        """
        Dibuja el estado de la barra de progreso.
        """
        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        # todo el widget
        gc.set_rgb_fg_color(get_colors("toolbars"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        # vacio
        gc.set_rgb_fg_color(get_colors("drawingplayer"))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        # progreso
        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(get_colors("naranaja"))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # borde de progreso
        gc.set_rgb_fg_color(get_colors("window"))
        self.window.draw_rectangle(gc, False, xx, yy, ww, hh)

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        yimage = yy + hh / 2 - imgh / 2

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
            imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True
    */
}


public class ControlVolumen : Gtk.VolumeButton{
    /*
    __gsignals__ = {
    "volumen": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}
    */

    public ControlVolumen(){

        this.value_changed.connect ((valor) => {
            this.__value_changed(valor);
		});

        this.show_all();

        this.set_value(0.1);
    }

    private void __value_changed(double valor){
        stdout.printf ("%f\n", valor);
        //valor = int(valor * 10)
        //self.emit('volumen', valor)
        }
}
