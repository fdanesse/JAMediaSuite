
public class ToolbarEstado : Gtk.EventBox{

    private Gtk.Label label = new Gtk.Label("Status");

    public ToolbarEstado(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();
        //toolbar.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#000000'))

        toolbar.insert(get_separador(false, 3, false), -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        item.set_expand(false);
        this.label.set_property("justify", Gtk.Justification.LEFT);
        // FIXME: Ver como se hace esto en el archivo css
        Gdk.Color color;
        Gdk.Color.parse("#ffffff", out color);
        this.label.modify_fg(Gtk.StateType.NORMAL, color);
        this.label.show();
        item.add(this.label);
        toolbar.insert(item, -1);

        toolbar.insert(get_separador(false, 0, true), -1);

        this.add(toolbar);
        this.show_all();
    }
    /*
    def set_info(self, _dict):
        reng = _dict['renglones']
        carac = _dict['caracteres']
        arch = _dict['archivo']

        text = self.label.get_text()
        new_text = u"Archivo: %s  Lineas: %s  Caracteres: %s" % (
            arch, reng, carac)

        try:
            if text != new_text:
                self.label.set_text(new_text)
        except:
            pass
    */
}


public class ToolbarArchivo : Gtk.EventBox{

    public signal void accion(string _accion);

    public ToolbarArchivo(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        toolbar.insert(get_separador(false, 10, false), - 1);

        //icon_path = make_icon_active(os.path.join(icons, "document-new.svg"))
        Gtk.ToolButton button1 = get_button("Iconos/document-new.svg", false, Gdk.PixbufRotation.NONE, 18, "Nuevo Archivo");
		button1.clicked.connect (() => {
			this.accion("Nuevo Archivo");
		    });
		toolbar.insert(button1, -1);

		//icon_path = make_icon_active(os.path.join(icons, "document-open.svg"))
        Gtk.ToolButton button2 = get_button("Iconos/document-open.svg", false, Gdk.PixbufRotation.NONE, 18, "Abrir Archivo");
		button2.clicked.connect (() => {
			this.accion("Abrir Archivo");
		    });
		toolbar.insert(button2, -1);

        Gtk.ToolButton button3 = get_button("Iconos/document-save.svg", false, Gdk.PixbufRotation.NONE, 18, "Guardar Archivo");
		button3.clicked.connect (() => {
			this.accion("Guardar Archivo");
		    });
		toolbar.insert(button3, -1);

		//icon_path = make_icon_active(os.path.join(icons, "document-save-as.svg"))
        Gtk.ToolButton button4 = get_button("Iconos/document-save-as.svg", false, Gdk.PixbufRotation.NONE, 18, "Guardar Como");
		button4.clicked.connect (() => {
			this.accion("Guardar Como");
		    });
		toolbar.insert(button4, -1);

        toolbar.insert(get_separador(true, 0, false), - 1);

        //icon_path = make_icon_active(os.path.join(icons, "media-playback-start.svg"))
        Gtk.ToolButton button5 = get_button("Iconos/media-playback-start.svg", false, Gdk.PixbufRotation.NONE, 18, "Ejecutar Archivo");
		button5.clicked.connect (() => {
			this.accion("Ejecutar Archivo");
		    });
		toolbar.insert(button5, -1);

        Gtk.ToolButton button6 = get_button("Iconos/media-playback-stop.svg", false, Gdk.PixbufRotation.NONE, 18, "Detener Ejecución");
		button6.clicked.connect (() => {
			this.accion("Detener Ejecución");
		    });
		toolbar.insert(button6, -1);

		toolbar.insert(get_separador(true, 0, false), - 1);

        Gtk.ToolButton button7 = get_button("Iconos/edit-undo.svg", false, Gdk.PixbufRotation.NONE, 18, "Deshacer");
		button7.clicked.connect (() => {
			this.accion("Deshacer");
		    });
		toolbar.insert(button7, -1);

        Gtk.ToolButton button8 = get_button("Iconos/edit-redo.svg", false, Gdk.PixbufRotation.NONE, 18, "Rehacer");
		button8.clicked.connect (() => {
			this.accion("Rehacer");
		    });
		toolbar.insert(button8, -1);

		toolbar.insert(get_separador(true, 0, false), - 1);

        Gtk.ToolButton button9 = get_button("Iconos/edit-copy.svg", false, Gdk.PixbufRotation.NONE, 18, "Copiar");
		button9.clicked.connect (() => {
			this.accion("Copiar");
		    });
		toolbar.insert(button9, -1);

        Gtk.ToolButton button10 = get_button("Iconos/editcut.svg", false, Gdk.PixbufRotation.NONE, 18, "Cortar");
		button10.clicked.connect (() => {
			this.accion("Cortar");
		    });
		toolbar.insert(button10, -1);

        Gtk.ToolButton button11 = get_button("Iconos/editpaste.svg", false, Gdk.PixbufRotation.NONE, 18, "Pegar");
		button11.clicked.connect (() => {
			this.accion("Pegar");
		    });
		toolbar.insert(button11, -1);

        toolbar.insert(get_separador(true, 0, false), - 1);

        Gtk.ToolButton button12 = get_button("Iconos/edit-select-all.svg", false, Gdk.PixbufRotation.NONE, 18, "Seleccionar Todo");
		button12.clicked.connect (() => {
			this.accion("Seleccionar Todo");
		    });
		toolbar.insert(button12, -1);

        toolbar.insert(get_separador(false, 0, true), - 1);

        this.add(toolbar);
        this.show_all();
    }
}


public class ToolbarProyecto : Gtk.EventBox{

    public signal void accion(string _accion);

    public ToolbarProyecto(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        //icon_path = make_icon_active(os.path.join(icons, "document-new.svg"))
        Gtk.ToolButton button1 = get_button("Iconos/document-new.svg", false, Gdk.PixbufRotation.NONE, 18, "Nuevo Proyecto");
		button1.clicked.connect (() => {
			this.accion("Nuevo Proyecto");
		    });
		toolbar.insert(button1, -1);

        //icon_path = make_icon_active(os.path.join(icons, "document-open.svg"))
        Gtk.ToolButton button2 = get_button("Iconos/document-open.svg", false, Gdk.PixbufRotation.NONE, 18, "Abrir Proyecto");
		button2.clicked.connect (() => {
			this.accion("Abrir Proyecto");
		    });
		toolbar.insert(button2, -1);

        Gtk.ToolButton button3 = get_button("Iconos/gtk-edit.svg", false, Gdk.PixbufRotation.NONE, 18, "Editar Proyecto");
		button3.clicked.connect (() => {
			this.accion("Editar Proyecto");
		    });
		toolbar.insert(button3, -1);

        Gtk.ToolButton button4 = get_button("Iconos/document-save.svg", false, Gdk.PixbufRotation.NONE, 18, "Guardar Proyecto");
		button4.clicked.connect (() => {
			this.accion("Guardar Proyecto");
		    });
		toolbar.insert(button4, -1);

        Gtk.ToolButton button5 = get_button("Iconos/button-cancel.svg", false, Gdk.PixbufRotation.NONE, 18, "Cerrar Proyecto");
		button5.clicked.connect (() => {
			this.accion("Cerrar Proyecto");
		    });
		toolbar.insert(button5, -1);

        toolbar.insert(get_separador(true, 0, false), - 1);

        Gtk.ToolButton button6 = get_button("Iconos/media-playback-start.svg", false, Gdk.PixbufRotation.NONE, 18, "Ejecutar Proyecto");
		button6.clicked.connect (() => {
			this.accion("Ejecutar Proyecto");
		    });
		toolbar.insert(button6, -1);

        Gtk.ToolButton button7 = get_button("Iconos/media-playback-stop.svg", false, Gdk.PixbufRotation.NONE, 18, "Detener Ejecución");
		button7.clicked.connect (() => {
			this.accion("Detener Ejecución");
		    });
		toolbar.insert(button7, -1);

        toolbar.insert(get_separador(false, 0, true), - 1);

        this.add(toolbar);
        this.show_all();

        //self.activar_proyecto(False)
        //self.activar_ejecucion(None)

        this.set_size_request(270, -1);
    }
}


public class ToolbarBusquedas : Gtk.EventBox{

    private Gtk.Entry entry = new Gtk.Entry();

    public ToolbarBusquedas(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.ToolButton button1 = get_button("Iconos/go-next-rtl.svg", false, Gdk.PixbufRotation.NONE, 18, "Anterior");
		//button1.clicked.connect (() => {
		//	this.accion("Anterior");
		//    });
		toolbar.insert(button1, -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        item.set_expand(true);
        this.entry.show();
        item.add(this.entry);
        toolbar.insert(item, - 1);

        Gtk.ToolButton button2 = get_button("Iconos/go-next.svg", false, Gdk.PixbufRotation.NONE, 18, "Siguiente");
		//button2.clicked.connect (() => {
		//	this.accion("Anterior");
		//    });
		toolbar.insert(button2, -1);

        Gtk.ToolButton button3 = get_button("Iconos/go-next.svg", false, Gdk.PixbufRotation.CLOCKWISE, 18, "Obtener Informe");
		//button3.clicked.connect (() => {
		//	this.accion("Obtener Informe");
		//    });
		toolbar.insert(button3, -1);

        //self.entry.connect("changed", self.__emit_buscar)
        this.add(toolbar);
        this.show_all();

        //self.anterior.set_sensitive(False)
        //self.siguiente.set_sensitive(False)
    }
}
