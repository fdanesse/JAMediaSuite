
public Gtk.SeparatorToolItem get_separador(bool draw, int ancho, bool expand){
    Gtk.SeparatorToolItem separador = new Gtk.SeparatorToolItem();
    separador.set_draw(draw);
    separador.set_size_request(ancho, -1);
    separador.set_expand(expand);
    return separador;
    }
