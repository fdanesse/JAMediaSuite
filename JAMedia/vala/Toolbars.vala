
public class Toolbar : Gtk.EventBox{

    public Toolbar(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = new Gtk.SeparatorToolItem();
        separador1.set_draw(false);
        separador1.set_size_request(3, -1);
        separador1.set_expand(false);
        toolbar.insert(separador1, -1);

        Gdk.Pixbuf pixbuf1 = new Gdk.Pixbuf.from_file_at_size("Iconos/JAMedia.svg", 35, 35);
        Gtk.Image img1 = new Gtk.Image.from_pixbuf(pixbuf1);
        //Gtk.Image img = new Gtk.Image.from_icon_name("document-open", Gtk.IconSize.SMALL_TOOLBAR);
		Gtk.ToolButton button1 = new Gtk.ToolButton(img1, null);
		button1.set_tooltip_text("Creditos");
        //button1.clicked.connect (() => {
		//	stdout.printf ("Button 1\n");
		//});
		button1.clicked.connect (() => {
			this.__show_credits();
		});
		toolbar.insert(button1, -1);

        Gdk.Pixbuf pixbuf2 = new Gdk.Pixbuf.from_file_at_size("Iconos/JAMedia-help.svg", 24, 24);
        Gtk.Image img2 = new Gtk.Image.from_pixbuf(pixbuf2);
		Gtk.ToolButton button2 = new Gtk.ToolButton(img2, null);
		button2.set_tooltip_text("Ayuda");
		button2.clicked.connect (() => {
			this.__show_help();
		});
		toolbar.insert(button2, -1);

        Gdk.Pixbuf pixbuf3 = new Gdk.Pixbuf.from_file_at_size("Iconos/configurar.svg", 24, 24);
        Gtk.Image img3 = new Gtk.Image.from_pixbuf(pixbuf3);
		Gtk.ToolButton button3 = new Gtk.ToolButton(img3, null);
		button3.set_tooltip_text("Configuraciones");
		button3.clicked.connect (() => {
			this.__emit_accion("show-config");
		});
		toolbar.insert(button3, -1);

        Gtk.SeparatorToolItem separador2 = new Gtk.SeparatorToolItem();
        separador2.set_draw(false);
        separador2.set_size_request(0, -1);
        separador2.set_expand(true);
        toolbar.insert(separador2, -1);

        Gdk.Pixbuf pixbuf4 = new Gdk.Pixbuf.from_file_at_size("Iconos/button-cancel.svg", 24, 24);
        Gtk.Image img4 = new Gtk.Image.from_pixbuf(pixbuf4);
		Gtk.ToolButton button4 = new Gtk.ToolButton(img4, null);
		button4.set_tooltip_text("Salir");
		button4.clicked.connect (() => {
			this.__emit_accion("salir");
		});
		toolbar.insert(button4, -1);

        Gtk.SeparatorToolItem separador3 = new Gtk.SeparatorToolItem();
        separador3.set_draw(false);
        separador3.set_size_request(3, -1);
        separador3.set_expand(false);
        toolbar.insert(separador3, -1);

        this.add(toolbar);
        this.show_all();
    }

    private void __show_credits(){
        stdout.printf("Button \n");
    }

    private void __show_help(){
        stdout.printf("Button \n");
    }

    private void __emit_accion(string accion){
        stdout.printf("%s\n", accion);
    }
}
