

public class Menu : Gtk.MenuBar{

    public Gtk.AccelGroup accel_group;

    public Menu(Gtk.AccelGroup _accel_group){

        this.accel_group = _accel_group;

        Gtk.MenuItem item_proyectos = new Gtk.MenuItem.with_label("Proyecto");
        MenuProyectos menu_proyectos = new MenuProyectos(this.accel_group);
        item_proyectos.set_submenu(menu_proyectos);
        this.append(item_proyectos);

        this.show_all();
    }
}


public class MenuProyectos : Gtk.Menu{

    public MenuProyectos(Gtk.AccelGroup _accel_group){

        /*
        item = Gtk.MenuItem('Nuevo . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Nuevo Proyecto")
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('N'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)
        */
        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Nuevo . . .");
        //item1.activate.connect (() => {
		//	this.__emit_accion_proyecto("Nuevo Proyecto");
		//    });
        this.append(item1);

        this.show_all();
    }
}
