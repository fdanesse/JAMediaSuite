public class Izquierda : Gtk.EventBox{

    //__gsignals__ = {
    //"show-controls": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    //'rotar': (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    //'actualizar_streamings': (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, []),
    //'stop-record': (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, []),
    //"seek": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_FLOAT, )),
    //"volumen": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    public Izquierda(){

        /*
        vbox = gtk.VBox()

        self.toolbar_record = ToolbarGrabar()
        self.video_visor = VideoVisor()
        #self.efectos_aplicados = Efectos_en_Pipe()
        self.buffer_info = BufferInfo()
        self.toolbar_info = ToolbarInfo()
        self.progress = ProgressPlayer()

        vbox.pack_start(self.toolbar_record, False, False, 0)
        vbox.pack_start(self.video_visor, True, True, 0)
        #vbox.pack_start(self.efectos_aplicados, False, False, 0)
        vbox.pack_start(self.buffer_info, False, False, 0)
        vbox.pack_start(self.toolbar_info, False, False, 0)
        vbox.pack_start(self.progress, False, False, 0)

        this.add(vbox);
        */

        this.show_all();

        /*
        self.toolbar_record.connect("stop", self.__emit_stop_record)

        self.video_visor.connect("ocultar_controles",
            self.__emit_show_controls)
        self.video_visor.connect("button_press_event", self.__set_fullscreen)

        self.toolbar_info.connect("rotar", self.__emit_rotar)
        self.toolbar_info.connect("actualizar_streamings",
            self.__emit_actualizar_streamings)

        self.progress.connect("seek", self.__emit_seek)
        self.progress.connect("volumen", self.__emit_volumen)
        */
    }
}
