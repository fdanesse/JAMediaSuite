
public class MenuUbuntuRadio : Gtk.MenuBar {
    /* Menú Principal de la aplicación */

    public signal void salir();

    public MenuUbuntuRadio () {

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label ("Menú");

		Gtk.Menu menu = new Gtk.Menu ();
		item1.set_submenu(menu);

		Gtk.MenuItem item2 = new Gtk.MenuItem.with_label ("Radios");
        //item2.activate.connect(this.listar_radios);
        menu.append(item2);

        Gtk.MenuItem item3 = new Gtk.MenuItem.with_label ("Configurar...");
        //item3.activate.connect(this.configurar);
        menu.append(item3);

        Gtk.MenuItem item4 = new Gtk.MenuItem.with_label ("Creditos...");
        //item4.activate.connect(this.creditos);
        menu.append(item4);

        Gtk.MenuItem item5 = new Gtk.MenuItem.with_label ("Actualizar Lista");
        //item5.activate.connect(this.emit_actualizar);
        menu.append(item5);

        Gtk.MenuItem item6 = new Gtk.MenuItem.with_label ("Salir");
        item6.activate.connect(this.emit_salir);
        menu.append(item6);

		this.add (item1);
        this.show_all();
    }

    private void emit_salir(){
        this.salir();
    }
}


public class ItemPlayer : Gtk.Frame {
    /* Widget con Reproductor de Streaming */

    private Gtk.Button stop_button = new Gtk.Button();
    private Gtk.Image image_button = new Gtk.Image();

    public ItemPlayer () {

        this.set_label(" Reproduciendo . . . ");

        Gtk.EventBox eventbox = new Gtk.EventBox();
        eventbox.set_border_width(5);
        Gtk.Box hbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
        eventbox.add(hbox);
        this.add(eventbox);

        Gtk.VolumeButton control_volumen = new Gtk.VolumeButton();

        hbox.pack_start(new Gtk.Label(""),
            false, true, 0);
        hbox.pack_end(this.stop_button,
            false, true, 0);
        hbox.pack_end(control_volumen,
            false, true, 0);

        this.image_button.set_from_stock(
            Gtk.Stock.MEDIA_PLAY, Gtk.IconSize.BUTTON);
        this.stop_button.set_image(this.image_button);

        control_volumen.set_value(0.10);

        this.show_all();

        this.stop_button.clicked.connect(this.play_stop);
    }

    private void play_stop(){
        /* Cuando se hace click en el botón stop */
    }

}
