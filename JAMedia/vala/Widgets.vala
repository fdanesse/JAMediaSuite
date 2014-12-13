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

    private Gtk.ToolButton anterior = get_button("Iconos/play.svg", true, Gdk.PixbufRotation.NONE, 24, "Anterior");
    private Gtk.ToolButton siguiente = get_button("Iconos/play.svg", false, Gdk.PixbufRotation.NONE, 24, "Siguiente");
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

		this.anterior.clicked.connect (() => {
			this.__show("Anterior");
		});
        box.pack_start(this.anterior, false, false, 0);

		this.siguiente.clicked.connect (() => {
			this.__show("Siguiente");
		});
        box.pack_end(this.siguiente, false, false, 0);

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

        this.__switch(this._index);
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
            this._index = items;
        }
        else if (this._index < 0){
            this._index = 0;
        }
    }
}
