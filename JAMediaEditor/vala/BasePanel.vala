
public class BasePanel : Gtk.HPaned{

    private WorkPanel workpanel = new WorkPanel();
    private Gtk.Box infonotebook_box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
    private ToolbarProyecto toolbarproyecto = new ToolbarProyecto();
    private ToolbarArchivo toolbararchivo = new ToolbarArchivo();

    public BasePanel(){

        this.set("border_width", 5);

        //self.infonotebook = InfoNotebook()
        //self.seleccionado_actual = 0

        //self.toolbararchivo = ToolbarArchivo()
        ToolbarBusquedas toolbarbusquedas = new ToolbarBusquedas();

        this.infonotebook_box.pack_start(this.toolbarproyecto, false, false, 0);
        //self.infonotebook_box.pack_start(self.infonotebook, True, True, 0)
        this.infonotebook_box.pack_end(toolbarbusquedas, false, false, 0);

        Gtk.Box workpanel_box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        workpanel_box.pack_start(this.toolbararchivo, false, false, 0);
        workpanel_box.pack_end(this.workpanel, true, true, 0);

        this.pack1(this.infonotebook_box, false, false);
        this.pack2(workpanel_box, true, true);

        this.show_all();

        //self.infonotebook_box.set_size_request(280, -1)

        //self.workpanel.connect('new_select', self.__set_introspeccion)
        //self.workpanel.connect('ejecucion', self.__re_emit_ejecucion)
        //self.workpanel.connect('update', self.__re_emit_update)

        //self.toolbararchivo.connect('accion', self.set_accion_archivo)
        this.toolbararchivo.accion.connect ((_accion) => {
			//this.__accion("Nuevo Archivo");
            GLib.stdout.printf("__accion_toolbararchivo: %s\n", _accion);
            GLib.stdout.flush();
		    });
        //self.toolbarproyecto.connect('accion', self.set_accion_proyecto)
        this.toolbarproyecto.accion.connect ((_accion) => {
			//this.__accion("Nuevo Archivo");
            GLib.stdout.printf("__accion_toolbarproyecto: %s\n", _accion);
            GLib.stdout.flush();
		    });

        //toolbarbusquedas.connect("buscar", self.__buscar)
        //toolbarbusquedas.connect("accion", self.__buscar_mas)
        //toolbarbusquedas.connect("informe", self.__informar)

        //self.infonotebook.connect('new_select', self.__set_linea)
        //self.infonotebook.connect('open', self.__abrir_archivo)
        //self.infonotebook.connect('search_on_grep', self.__search_grep)
        //self.infonotebook.connect('remove_proyect', self.__remove_proyect)
    }
}
