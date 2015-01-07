

public class Menu : Gtk.MenuBar{

    public signal void accion(string _accion);

    public Gtk.AccelGroup accel_group;

    public Menu(Gtk.AccelGroup _accel_group){

        this.accel_group = _accel_group;

        Gtk.MenuItem item_proyectos = new Gtk.MenuItem.with_label("Proyecto");
        MenuProyectos menu_proyectos = new MenuProyectos(this.accel_group);
        item_proyectos.set_submenu(menu_proyectos);
        menu_proyectos.accion.connect((_accion) => {
			this.accion(_accion);
		    });
        this.append(item_proyectos);

        this.show_all();
    }
}


public class MenuProyectos : Gtk.Menu{

    public signal void accion(string _accion);

    public MenuProyectos(Gtk.AccelGroup _accel_group){

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Nuevo . . .");
        item1.activate.connect (() => {
			this.accion("Nuevo Proyecto");
		    });
        this.append(item1);
        item1.add_accelerator("activate", _accel_group,
            'N', Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        this.show_all();
    }
}
