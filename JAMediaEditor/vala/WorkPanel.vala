
public class WorkPanel : Gtk.VPaned{

    private WorkPanel2 workpanel2 = new WorkPanel2();
    private Terminal terminal = new Terminal();

    public WorkPanel(){

        //# Terminal en ejecución.
        //self.ejecucion = False
        //# Tipo: proyecto o archivo.
        //self.ejecucion_activa = False

        this.pack1(this.workpanel2, true, false);
        this.pack2(this.terminal, false, true);

        this.show_all();
        this.terminal.set_size_request(-1, 170);

        //self.terminal.connect("ejecucion", self.__set_ejecucion)
        //self.terminal.connect("reset", self.detener_ejecucion)
        //GLib.idle_add(self.terminal.hide)
    }

    public void abrir_archivos(SList<string> archivos){
        this.workpanel2.abrir_archivos(archivos);
        }
}


public class WorkPanel2 : Gtk.HPaned{

    // FIXME: Contenedor de guias, ejemplos y tutoriales.
    private Notebook_SourceView notebook_sourceview = new Notebook_SourceView();

    public WorkPanel2(){

        this.pack1(this.notebook_sourceview, true, false);
        //this.pack2(Guias y Ejemplos, true, false);

        //self.notebook_sourceview.connect('new_select', self.__re_emit_new_select)
        //self.notebook_sourceview.connect('update', self.__re_emit_update)

        this.show_all();
    }

    public void abrir_archivos(SList<string> archivos){
        foreach (unowned string archivo in archivos){
            notebook_sourceview.abrir_archivo(archivo);
            }
        }
}


public class Notebook_SourceView : Gtk.Notebook{

    private string fuente = "Monospace";
    private int tamanio = 10;
    private bool numeracion = true;

    public Notebook_SourceView(){

        this.set_scrollable(true);
        //self.ultimo_view_activo = False
        this.show_all();
        //self.connect('switch_page', self.__switch_page)
        //GLib.Idle.add(this.abrir_archivo, null);
        this.abrir_archivo("None");
    }

    private void __update_label(SourceView sourceview, string archivo){
        /*
        """
        Setea la etiqueta en notebook cuando cambia el nombre del archivo.
        """
        paginas = self.get_n_pages()
        for indice in range(paginas):
            pag = self.get_children()[indice]
            if pag.get_children()[0] == sourceview:
                label = self.get_tab_label(pag).get_children()[0]
                if (archivo != "None"){
                    GLib.File file = GLib.File.parse_name(archivo);
                    if (file.query_exists()){
                        //FIXME: Arreglar
                        //if len(nombre) > 13:
                        //    nombre = nombre[0:13] + " . . . "
                        label.set_text(GLib.Path.get_basename(archivo));
                        }
                    else{
                        label.set_text("Sin Título")
                        }
                    }
                break
        */
        }

    public bool abrir_archivo(string archivo){
        /*
        # Si el archivo ya está abierto, se selecciona
        paginas = self.get_children()
        for pagina in paginas:
            view = pagina.get_child()
            if view.archivo and archivo:
                arch1 = view.archivo
                arch2 = archivo
                if arch1 == archivo:
                    self.set_current_page(paginas.index(pagina))
                    return False
        */

        // Crear la lengüeta
        Gtk.Box hbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
        Gtk.Label label = new Gtk.Label("Sin Título");

        Gtk.ToolButton boton = get_button("Iconos/button-cancel.svg", false, Gdk.PixbufRotation.NONE, 18, "Cerrar");
        //button.clicked.connect (() => {
        //    this.__cerrar();
        //    });
        hbox.pack_start(label, false, false, 0);
        hbox.pack_start(boton, false, false, 0);

        SourceView sourceview = new SourceView(this.fuente, this.tamanio, this.numeracion);
        Gtk.ScrolledWindow scroll = new Gtk.ScrolledWindow(null, null);
        scroll.set("hscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll.add(sourceview);
        this.append_page(scroll, hbox);

        hbox.show_all();
        this.show_all();

        this.set_current_page(-1);
        this.set_tab_reorderable(scroll, true);

        //sourceview.connect("update", self.__re_emit_update)
        //sourceview.connect("force-select", self.__re_emit_force_select)
        sourceview.update_label.connect ((source, arch) => {
             this.__update_label(source, arch);
            });
        sourceview.set_archivo(archivo);
        return false;
        }
}
