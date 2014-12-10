
public class Toolbar : Gtk.EventBox{

    public signal void credits();
    public signal void help();

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
			this.__emit_credits();
		});
		toolbar.insert(button1, -1);

        Gdk.Pixbuf pixbuf2 = new Gdk.Pixbuf.from_file_at_size("Iconos/JAMedia-help.svg", 24, 24);
        Gtk.Image img2 = new Gtk.Image.from_pixbuf(pixbuf2);
		Gtk.ToolButton button2 = new Gtk.ToolButton(img2, null);
		button2.set_tooltip_text("Ayuda");
		button2.clicked.connect (() => {
			this.__emit_help();
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

    private void __emit_credits(){
        this.credits();
    }

    private void __emit_help(){
        this.help();
    }

    private void __emit_accion(string accion){
        stdout.printf("%s\n", accion);
    }
}


public class Creditos : Gtk.Dialog{

    public Creditos(Gtk.Window parent, string title){

        this.set("title", title);
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set("border_width", 15);
        this.set_decorated(false);
        this.set_resizable(false);

        Gtk.Image imagen = new Gtk.Image();
        imagen.set_from_file("Iconos/JAMediaCredits.svg");

        Gtk.Box Box = this.get_content_area ();
        Box.pack_start(imagen, true, true, 0);
        Box.show_all();

        this.add_button ("Cerrar", Gtk.ResponseType.OK);
    }
}


public class Help : Gtk.Dialog{

    private SList<Gtk.Image> archivos = new SList<Gtk.Image> ();
    private int _index = 0;

    public Help(Gtk.Window parent, string title){

        this.set("title", title);
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set("border_width", 15);
        this.set_decorated(false);
        this.set_resizable(false);

        Gtk.Grid grid = new Gtk.Grid();
        Gtk.Box box = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
        grid.attach(box, 0, 0, 5, 1);

        Gdk.Pixbuf pix = new Gdk.Pixbuf.from_file_at_size("Iconos/play.svg", 24, 24);
        Gdk.Pixbuf pixbuf1 = pix.flip(true);
        Gtk.Image img1 = new Gtk.Image.from_pixbuf(pixbuf1);
		Gtk.ToolButton anterior = new Gtk.ToolButton(img1, null);
		anterior.set_tooltip_text("Anterior");
		anterior.clicked.connect (() => {
			this.__show("Anterior");
		});
        box.pack_start(anterior, false, false, 0);

        Gdk.Pixbuf pixbuf2 = new Gdk.Pixbuf.from_file_at_size("Iconos/play.svg", 24, 24);
        Gtk.Image img2 = new Gtk.Image.from_pixbuf(pixbuf2);
		Gtk.ToolButton siguiente = new Gtk.ToolButton(img2, null);
		siguiente.set_tooltip_text("Siguiente");
		siguiente.clicked.connect (() => {
			this.__show("Siguiente");
		});
        box.pack_end(siguiente, false, false, 0);

        //SList<Gtk.Image> archivos = new SList<Gtk.Image> ();
        Gdk.Pixbuf help1 = new Gdk.Pixbuf.from_file("Iconos/help-1.svg");
        Gtk.Image Ig1 = new Gtk.Image.from_pixbuf(help1);
        this.archivos.append(Ig1);
        grid.attach(Ig1, 0, 1, 5, 2);

        Gdk.Pixbuf help2 = new Gdk.Pixbuf.from_file("Iconos/help-2.svg");
        Gtk.Image Ig2 = new Gtk.Image.from_pixbuf(help2);
        this.archivos.append(Ig2);
        grid.attach(Ig2, 0, 1, 5, 2);

        Gdk.Pixbuf help3 = new Gdk.Pixbuf.from_file("Iconos/help-3.svg");
        Gtk.Image Ig3 = new Gtk.Image.from_pixbuf(help3);
        this.archivos.append(Ig3);
        grid.attach(Ig3, 0, 1, 5, 2);

        Gdk.Pixbuf help4 = new Gdk.Pixbuf.from_file("Iconos/help-4.svg");
        Gtk.Image Ig4 = new Gtk.Image.from_pixbuf(help4);
        this.archivos.append(Ig4);
        grid.attach(Ig4, 0, 1, 5, 2);

        Gtk.Box thisbox = this.get_content_area ();
        thisbox.pack_start(grid, true, true, 0);
        thisbox.show_all();

        this.add_button ("Cerrar", Gtk.ResponseType.OK);

        this.__set_item(this._index);

        }

    private void __switch(int index){
        for (int i = 0; i < this.archivos.length (); i++) {
            Gtk.Image img = this.archivos.nth_data(i);
            img.hide();
        img = this.archivos.nth_data(index);
        img.show();
        }
    }

    private void __show(string valor){
        if (valor == "Anterior") {
            this._index --;
            }
        else if (valor == "Siguiente"){
            this._index ++;
            }
        else {
            this._index = 0;
            }
        this.__set_item((int) this.archivos.length());
        this.__switch(this._index);
    }

    private void __set_item(int items){
        items --;
        if (this._index > items){
            this._index = 0;
        }
        else if (this._index < 0){
            this._index = items;
        }
    }
}
