

public class Menu : Gtk.MenuBar{

    public signal void accion(string _accion, bool valor);

    public Gtk.AccelGroup accel_group;

    public Menu(Gtk.AccelGroup _accel_group){

        this.accel_group = _accel_group;

        Gtk.MenuItem item_proyectos = new Gtk.MenuItem.with_label("Proyecto");
        MenuProyectos menu_proyectos = new MenuProyectos();
        item_proyectos.set_submenu(menu_proyectos);
        menu_proyectos.accion.connect((_accion, valor) => {
			this.accion(_accion, valor);
		    });
        this.append(item_proyectos);

        Gtk.MenuItem item_archivos = new Gtk.MenuItem.with_label("Archivo");
        MenuArchivos menu_archivos = new MenuArchivos(this.accel_group);
        item_archivos.set_submenu(menu_archivos);
        menu_archivos.accion.connect((_accion, valor) => {
			this.accion(_accion, valor);
		    });
        this.append(item_archivos);

        Gtk.MenuItem item_edicion = new Gtk.MenuItem.with_label("Edición");
        MenuEdicion menu_edicion = new MenuEdicion(this.accel_group);
        item_edicion.set_submenu(menu_edicion);
        menu_edicion.accion.connect((_accion, valor) => {
			this.accion(_accion, valor);
		    });
        this.append(item_edicion);

        Gtk.MenuItem item_ver = new Gtk.MenuItem.with_label("Ver");
        MenuVer menu_ver = new MenuVer();
        item_ver.set_submenu(menu_ver);
        menu_ver.accion.connect((_accion, valor) => {
			this.accion(_accion, valor);
		    });
        this.append(item_ver);

        Gtk.MenuItem item_codigo = new Gtk.MenuItem.with_label("Código");
        MenuCodigo menu_codigo = new MenuCodigo(this.accel_group);
        item_codigo.set_submenu(menu_codigo);
        menu_codigo.accion.connect((_accion, valor) => {
			this.accion(_accion, valor);
		    });
        this.append(item_codigo);

        Gtk.MenuItem item_ayuda = new Gtk.MenuItem.with_label("Ayuda");
        MenuAyuda menu_ayuda = new MenuAyuda();
        item_ayuda.set_submenu(menu_ayuda);
        menu_ayuda.accion.connect((_accion, valor) => {
			this.accion(_accion, valor);
		    });
        this.append(item_ayuda);

        this.show_all();
    }
}


public class MenuProyectos : Gtk.Menu{

    public signal void accion(string _accion, bool valor);

    public MenuProyectos(){

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Nuevo...");
        item1.activate.connect (() => {
			this.accion("Nuevo Proyecto", false);
		    });
        this.append(item1);

        Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("Abrir...");
        item2.activate.connect (() => {
			this.accion("Abrir Proyecto", false);
		    });
        this.append(item2);

        Gtk.MenuItem item3 = new Gtk.MenuItem.with_label("Editar...");
        item3.activate.connect (() => {
			this.accion("Editar Proyecto", false);
		    });
        this.append(item3);

        Gtk.MenuItem item4 = new Gtk.MenuItem.with_label("Cerrar");
        item4.activate.connect (() => {
			this.accion("Cerrar Proyecto", false);
		    });
        this.append(item4);

        Gtk.MenuItem item5 = new Gtk.MenuItem.with_label("Guardar");
        item5.activate.connect (() => {
			this.accion("Guardar Proyecto", false);
		    });
        this.append(item5);

        Gtk.MenuItem item6 = new Gtk.MenuItem.with_label("Ejecutar");
        item6.activate.connect (() => {
			this.accion("Ejecutar Proyecto", false);
		    });
        this.append(item6);

        Gtk.MenuItem item7 = new Gtk.MenuItem.with_label("Construir...");
        item7.activate.connect (() => {
			this.accion("Construir Proyecto", false);
		    });
        this.append(item7);

        this.show_all();
    }
}


public class MenuArchivos : Gtk.Menu{

    public signal void accion(string _accion, bool valor);

    public MenuArchivos(Gtk.AccelGroup _accel_group){

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Nuevo");
        item1.activate.connect (() => {
			this.accion("Nuevo Archivo", false);
		    });
        this.append(item1);
        item1.add_accelerator("activate", _accel_group,
            'N', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("Abrir...");
        item2.activate.connect (() => {
			this.accion("Abrir Archivo", false);
		    });
        this.append(item2);
        item2.add_accelerator("activate", _accel_group,
            'O', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item3 = new Gtk.MenuItem.with_label("Guardar");
        item3.activate.connect (() => {
			this.accion("Guardar Archivo", false);
		    });
        this.append(item3);
        item3.add_accelerator("activate", _accel_group,
            'S', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item4 = new Gtk.MenuItem.with_label("Guardar Como...");
        item4.activate.connect (() => {
			this.accion("Guardar Como", false);
		    });
        this.append(item4);

        this.show_all();
    }
}


public class MenuEdicion : Gtk.Menu{

    public signal void accion(string _accion, bool valor);

    public MenuEdicion(Gtk.AccelGroup _accel_group){

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Deshacer");
        item1.activate.connect (() => {
			this.accion("Deshacer", false);
		    });
        this.append(item1);
        item1.add_accelerator("activate", _accel_group,
            'Z', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("Rehacer");
        item2.activate.connect (() => {
			this.accion("Rehacer", false);
		    });
        this.append(item2);
        item2.add_accelerator("activate", _accel_group,
            'Z', Gdk.ModifierType.CONTROL_MASK |
            Gdk.ModifierType.SHIFT_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item3 = new Gtk.MenuItem.with_label("Cortar");
        item3.activate.connect (() => {
			this.accion("Cortar", false);
		    });
        this.append(item3);
        item3.add_accelerator("activate", _accel_group,
            'X', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item4 = new Gtk.MenuItem.with_label("Copiar");
        item4.activate.connect (() => {
			this.accion("Copiar", false);
		    });
        this.append(item4);
        item4.add_accelerator("activate", _accel_group,
            'C', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item5 = new Gtk.MenuItem.with_label("Pegar");
        item5.activate.connect (() => {
			this.accion("Pegar", false);
		    });
        this.append(item5);
        item5.add_accelerator("activate", _accel_group,
            'V', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item6 = new Gtk.MenuItem.with_label("Seleccionar Todo");
        item6.activate.connect (() => {
			this.accion("Seleccionar Todo", false);
		    });
        this.append(item6);
        item6.add_accelerator("activate", _accel_group,
            'A', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        this.show_all();
    }
}


public class MenuVer : Gtk.Menu{

    public signal void accion(string _accion, bool valor);

    public MenuVer(){

        Gtk.MenuItem item1 = new Gtk.MenuItem();
        Gtk.HBox hbox1 = new Gtk.HBox(false, 0);
        Gtk.CheckButton button1 = new Gtk.CheckButton();
        button1.set_active(true);
        hbox1.pack_start(button1, false, false, 0);
        Gtk.Label label1 = new Gtk.Label("Numeros de línea");
        hbox1.pack_start(label1, false, false, 5);
        item1.add(hbox1);
        item1.activate.connect (() => {
            bool valor = button1.get_active() == false;
            button1.set_active(valor);
			this.accion("Ver Numeración", valor);
		    });
        this.append(item1);

        Gtk.MenuItem item2 = new Gtk.MenuItem();
        Gtk.HBox hbox2 = new Gtk.HBox(false, 0);
        Gtk.CheckButton button2 = new Gtk.CheckButton();
        button2.set_active(true);
        hbox2.pack_start(button2, false, false, 0);
        Gtk.Label label2 = new Gtk.Label("Panel Inferior");
        hbox2.pack_start(label2, false, false, 5);
        item2.add(hbox2);
        item2.activate.connect (() => {
            bool valor = button2.get_active() == false;
            button2.set_active(valor);
			this.accion("Ver Panel Inferior", valor);
		    });
        this.append(item2);

        Gtk.MenuItem item3 = new Gtk.MenuItem();
        Gtk.HBox hbox3 = new Gtk.HBox(false, 0);
        Gtk.CheckButton button3 = new Gtk.CheckButton();
        button3.set_active(true);
        hbox3.pack_start(button3, false, false, 0);
        Gtk.Label label3 = new Gtk.Label("Panel Izquierdo");
        hbox3.pack_start(label3, false, false, 5);
        item3.add(hbox3);
        item3.activate.connect (() => {
            bool valor = button3.get_active() == false;
            button3.set_active(valor);
			this.accion("Ver Panel Izquierdo", valor);
		    });
        this.append(item3);

        Gtk.MenuItem item4 = new Gtk.MenuItem();
        Gtk.HBox hbox4 = new Gtk.HBox(false, 0);
        Gtk.CheckButton button4 = new Gtk.CheckButton();
        button4.set_active(true);
        hbox4.pack_start(button4, false, false, 0);
        Gtk.Label label4 = new Gtk.Label("Panel Derecho");
        hbox4.pack_start(label4, false, false, 5);
        item4.add(hbox4);
        item4.activate.connect (() => {
            bool valor = button4.get_active() == false;
            button4.set_active(valor);
			this.accion("Ver Panel Derecho", valor);
		    });
        this.append(item4);

        this.show_all();
    }
}


public class MenuCodigo : Gtk.Menu{

    public signal void accion(string _accion, bool valor);

    public MenuCodigo(Gtk.AccelGroup _accel_group){

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Formato de Texto...");
        item1.activate.connect (() => {
			this.accion("Formato de Texto", false);
		    });
        this.append(item1);
        item1.add_accelerator("activate", _accel_group,
            'T', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("De Identar");
        item2.activate.connect (() => {
			this.accion("De Identar", false);
		    });
        this.append(item2);
        item2.add_accelerator("activate", _accel_group,
            'I', Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item3 = new Gtk.MenuItem.with_label("Buscar Texto...");
        item3.activate.connect (() => {
			this.accion("Buscar Texto", false);
		    });
        this.append(item3);
        item3.add_accelerator("activate", _accel_group,
            'B', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item4 = new Gtk.MenuItem.with_label("Reemplazar Texto...");
        item4.activate.connect (() => {
			this.accion("Reemplazar Texto", false);
		    });
        this.append(item4);
        item4.add_accelerator("activate", _accel_group,
            'R', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

        Gtk.MenuItem item5 = new Gtk.MenuItem.with_label("Chequear sintaxis");
        item5.activate.connect (() => {
			this.accion("Chequear sintaxis", false);
		    });
        this.append(item5);

        this.show_all();
    }
}

public class MenuAyuda : Gtk.Menu{

    public signal void accion(string _accion, bool valor);

    public MenuAyuda(){

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Créditos");
        item1.activate.connect (() => {
			this.accion("Créditos", false);
		    });
        this.append(item1);

        Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("JAMediaPyGiHack");
        item2.activate.connect (() => {
			this.accion("JAMediaPyGiHack", false);
		    });
        this.append(item2);

        this.show_all();
    }
}
