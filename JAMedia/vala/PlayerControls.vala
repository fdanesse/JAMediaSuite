
public class PlayerControls : Gtk.EventBox{

    public signal void accion_controls(string accion);

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
        this.accion_controls(accion);
        }

    public void activar(int valor){
        if (valor == 0){
            this.atras.set_sensitive(false);
            this.play.set_sensitive(false);
            this.siguiente.set_sensitive(false);
            this.stop.set_sensitive(false);
            }
        else if (valor == 1){
            this.atras.set_sensitive(false);
            this.siguiente.set_sensitive(false);
            this.play.set_sensitive(true);
            this.stop.set_sensitive(true);
            }
        else{
            this.atras.set_sensitive(true);
            this.play.set_sensitive(true);
            this.siguiente.set_sensitive(true);
            this.stop.set_sensitive(true);
            }
        }

    public void set_paused(){
        this.play.set_paused(this.pix_play);
        }

    public void set_playing(){
        this.play.set_playing(this.pix_paused);
        }
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

    public void set_playing(Gdk.Pixbuf pixbuf){
        if (this.estado == false){
            this.estado = true;
            this.imagen.set_from_pixbuf(pixbuf);
            }
        }

    public void set_paused(Gdk.Pixbuf pixbuf){
        if (this.estado == true){
            this.estado = false;
            this.imagen.set_from_pixbuf(pixbuf);
            }
        }
}
