
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
    }

    public void abrir_archivo(string archivo){
        GLib.stdout.printf("%s\n", archivo);
        GLib.stdout.flush();
        /*
        paginas = self.get_children()
        for pagina in paginas:
            view = pagina.get_child()
            if view.archivo and archivo:
                arch1 = os.path.join(view.archivo)
                arch2 = os.path.join(archivo)
                if arch1 == archivo:
                    return False
        */

        SourceView sourceview = new SourceView(this.fuente, this.tamanio, this.numeracion);

        Gtk.Box hbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
        Gtk.Label label = new Gtk.Label("Sin Título");

        Gtk.ToolButton boton = get_button("Iconos/button-cancel.svg", false, Gdk.PixbufRotation.NONE, 18, "Cerrar");
		//button.clicked.connect (() => {
		//	this.__cerrar();
		//    });

        hbox.pack_start(label, false, false, 0);
        hbox.pack_start(boton, false, false, 0);

        Gtk.ScrolledWindow scroll = new Gtk.ScrolledWindow(null, null);
        scroll.set("hscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll.add(sourceview);
        this.append_page(scroll, hbox);

        sourceview.set_archivo(archivo);

        hbox.show_all();
        this.show_all();

        this.set_current_page(-1);
        this.set_tab_reorderable(scroll, true);
        /*
        """
        # FIXME: Cuando se abre un archivo, se cierra el vacío por default.
        if len(paginas) > 1:
            for pagina in paginas:
                view = pagina.get_child()

                if not view.archivo:
                    buffer = view.get_buffer()
                    inicio, fin = buffer.get_bounds()
                    buf = buffer.get_text(inicio, fin, 0)

                    if not buf:
                        self.remove(pagina)
                        break
        """

        sourceview.connect("update", self.__re_emit_update)
        sourceview.connect("force-select", self.__re_emit_force_select)
        */
        }
}
