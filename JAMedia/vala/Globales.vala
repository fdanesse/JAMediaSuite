public Gtk.SeparatorToolItem get_separador(bool draw, int ancho, bool expand){
    Gtk.SeparatorToolItem separador = new Gtk.SeparatorToolItem();
    separador.set_draw(draw);
    separador.set_size_request(ancho, -1);
    separador.set_expand(expand);
    return separador;
}

public Gtk.ToolButton get_button(string archivo, bool flip, Gdk.PixbufRotation rotacion, int pixels, string tooltip){
    Gdk.Pixbuf pix = new Gdk.Pixbuf.from_file_at_size(archivo, pixels, pixels);
    Gdk.Pixbuf pixbuf = null;
    if (flip == true){
        // false espeja en la vertical
        pixbuf = pix.flip(flip);
        }
    else{
        pixbuf = pix;
        }
    pixbuf = pixbuf.rotate_simple(rotacion);
    Gtk.Image img = new Gtk.Image.from_pixbuf(pixbuf);
	Gtk.ToolButton button = new Gtk.ToolButton(img, null);
	button.set_tooltip_text(tooltip);
    return button;
}


public class Streaming : GLib.Object{

    public string nombre;
    public string path;

    public Streaming(string nombre, string path){
        this.nombre = nombre;
        this.path = path;
    }
}
