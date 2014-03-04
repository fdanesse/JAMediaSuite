
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
