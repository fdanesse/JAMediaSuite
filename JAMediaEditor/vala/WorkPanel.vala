
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
}


public class WorkPanel2 : Gtk.HPaned{

    private Notebook_SourceView notebook_sourceview = new Notebook_SourceView();

    public WorkPanel2(){

        this.pack1(this.notebook_sourceview, true, false);
        //this.pack2(Guias y Ejemplos, true, false);

        //self.notebook_sourceview.connect('new_select', self.__re_emit_new_select)
        //self.notebook_sourceview.connect('update', self.__re_emit_update)

        this.show_all();
    }
}


public class Notebook_SourceView : Gtk.Notebook{

    public Notebook_SourceView(){
        //self.config = {
        //    'fuente': 'Monospace',
        //    'tamanio': 10,
        //    'numeracion': True,
        //    }

        this.set_scrollable(true);
        //self.ultimo_view_activo = False

        this.show_all();

        //self.connect('switch_page', self.__switch_page)

        //GLib.idle_add(self.abrir_archivo, False)
    }
}
