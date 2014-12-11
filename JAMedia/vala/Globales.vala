public Gtk.SeparatorToolItem get_separador(bool draw, int ancho, bool expand){
    Gtk.SeparatorToolItem separador = new Gtk.SeparatorToolItem();
    separador.set_draw(draw);
    separador.set_size_request(ancho, -1);
    separador.set_expand(expand);
    return separador;
}

public Gtk.ToolButton get_button(string archivo, bool flip, int pixels, string tooltip){
    Gdk.Pixbuf pix = new Gdk.Pixbuf.from_file_at_size(archivo, pixels, pixels);
    Gdk.Pixbuf pixbuf;
    if (flip == true){
        pixbuf = pix.flip(flip);
        }
    else{
        pixbuf = pix;
        }
    Gtk.Image img = new Gtk.Image.from_pixbuf(pixbuf);
	Gtk.ToolButton button = new Gtk.ToolButton(img, null);
	button.set_tooltip_text(tooltip);
    return button;
}
