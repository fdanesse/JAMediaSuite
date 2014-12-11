public class BasePanel : Gtk.HPaned{

    //__gsignals__ = {
    //"show-controls": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    //"accion-list": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
    //    gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    //"menu_activo": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, []),
    //"add_stream": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    //'stop-record': (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, [])}

    private Izquierda izquierda = new Izquierda();
    private Derecha derecha = new Derecha();

    public BasePanel(){

        this.set_border_width(2);
        /*
        self._thread = False
        self.player = False
        */

        this.pack1(this.izquierda, true, true);
        this.pack2(this.derecha, false, false);

        this.show_all();

        /*
        self.derecha.connect("cargar-reproducir", self.__cargar_reproducir)
        self.derecha.connect("accion-list", self.__emit_accion_list)
        self.derecha.connect("menu_activo", self.__emit_menu_activo)
        self.derecha.connect("add_stream", self.__emit_add_stream)
        self.derecha.connect("accion-controls", self.__accion_controls)
        self.derecha.connect("balance-valor", self.__accion_balance)
        #self.derecha.connect("add_remove_efecto", self.__add_remove_efecto)
        #self.derecha.connect("configurar_efecto", self.__config_efecto)

        self.izquierda.connect("show-controls", self.__emit_show_controls)
        self.izquierda.connect("rotar", self.__rotar)
        self.izquierda.connect("stop-record", self.__stop_record)
        self.izquierda.connect("seek", self.__user_set_progress)
        self.izquierda.connect("volumen", self.__set_volumen)
        self.izquierda.connect("actualizar_streamings",
            self.__actualizar_streamings)

        gobject.timeout_add(5000, self.__check_ip)
        */
    }
}
