
public class Toolbar : Gtk.Toolbar{

    public Toolbar(){

        Gtk.SeparatorToolItem separador = new Gtk.SeparatorToolItem();
        separador.set_draw(false);
        separador.set_size_request(3, -1);
        separador.set_expand(false);
        this.insert(separador, -1);

        Gdk.Pixbuf pixbuf = new Gdk.Pixbuf.from_file_at_size("Iconos/JAMedia.svg", 35, 35);
        Gtk.Image img = new Gtk.Image.from_pixbuf(pixbuf);
        //Gtk.Image img = new Gtk.Image.from_icon_name("document-open", Gtk.IconSize.SMALL_TOOLBAR);
		Gtk.ToolButton button1 = new Gtk.ToolButton(img, null);
		button1.set_tooltip_text("Creditos");
        button1.clicked.connect (() => {
			stdout.printf ("Button 1\n");
		});
		this.insert(button1, -1);

        this.show_all();
    }
}
