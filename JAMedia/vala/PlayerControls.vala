
public class PlayerControls : Gtk.EventBox{
    /*
    __gsignals__ = {
    "accion-controls": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}
    */

    private JAMediaToolButton atras = new JAMediaToolButton();
    private JAMediaToolButton play = new JAMediaToolButton();
    private JAMediaToolButton siguiente = new JAMediaToolButton();
    private JAMediaToolButton stop = new JAMediaToolButton();
    private Gdk.Pixbuf pix_play = null;
    private Gdk.Pixbuf pix_paused = null;

    public PlayerControls(){

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);

        this.pix_play = new Gdk.Pixbuf.from_file_at_size("Iconos/play.svg", 24, 24);
        this.pix_paused = new Gdk.Pixbuf.from_file_at_size("Iconos/pausa.svg", 24, 24);

        this.atras.set_imagen("Iconos/siguiente.svg", true, Gdk.PixbufRotation.NONE);
        this.atras.set_tooltip_text("Anterior");
        this.atras.clicked.connect (() => {
			this.__emit_accion("atras");
		});
        vbox.pack_start(this.atras, false, true, 0);

        this.play.set_imagen("Iconos/play.svg", false, Gdk.PixbufRotation.NONE);
        this.play.set_tooltip_text("Reproducir");
        this.play.clicked.connect (() => {
			this.__emit_accion("pausa-play");
		});
        vbox.pack_start(this.play, false, true, 0);

        this.siguiente.set_imagen("Iconos/siguiente.svg", false, Gdk.PixbufRotation.NONE);
        this.siguiente.set_tooltip_text("Siguiente");
        this.siguiente.clicked.connect (() => {
			this.__emit_accion("siguiente");
		});
        vbox.pack_start(this.siguiente, false, true, 0);

        this.stop.set_imagen("Iconos/stop.svg", false, Gdk.PixbufRotation.NONE);
        this.stop.set_tooltip_text("Detener Reproducción");
        this.stop.clicked.connect (() => {
			this.__emit_accion("stop");
		});
        vbox.pack_start(this.stop, false, true, 0);

        this.add(vbox);
        this.show_all();
    }

    private void __emit_accion(string accion){
        //self.emit("accion-controls", accion)
        }

    /*
    def activar(self, valor):
        if valor:
            map(sensibilizar, [self.atras, self.play,
                self.siguiente, self.stop])
        else:
            map(insensibilizar, [self.atras, self.play,
                self.siguiente, self.stop])

    def set_paused(self):
        self.play.set_paused(self.pix_play)

    def set_playing(self):
        self.play.set_playing(self.pix_paused)
    */
}


public class JAMediaToolButton : Gtk.ToolButton{

    private bool estado = false;
    private int pixels = 24;
    private Gtk.Image imagen = new Gtk.Image();

    public JAMediaToolButton(){

        this.set_icon_widget(this.imagen);
        this.imagen.show();
        this.imagen.set_size_request(this.pixels, this.pixels);
        this.show_all();
    }

    public void set_imagen(string archivo, bool flip, Gdk.PixbufRotation rotacion){
        Gdk.Pixbuf pix = new Gdk.Pixbuf.from_file_at_size(archivo, this.pixels, this.pixels);
        Gdk.Pixbuf pixbuf = null;
        if (flip == true){
            // false espeja en la vertical
            pixbuf = pix.flip(flip);
            }
        else{
            pixbuf = pix;
            }
        pixbuf = pixbuf.rotate_simple(rotacion);
        this.imagen.set_from_pixbuf(pixbuf);
        }
    /*
    def set_playing(self, pixbuf):
        if self.estado:
            return
        self.estado = True
        self.imagen.set_from_pixbuf(pixbuf)

    def set_paused(self, pixbuf):
        if not self.estado:
            return
        self.estado = False
        self.imagen.set_from_pixbuf(pixbuf)
    */
}
