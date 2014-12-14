public class Izquierda : Gtk.EventBox{

    //__gsignals__ = {
    //"show-controls": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    //"seek": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_FLOAT, )),
    //"volumen": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    public signal void stop_record();
    public signal void rotar(string rotacion);
    public signal void actualizar_streamings();
    private ToolbarGrabar toolbar_record = new ToolbarGrabar();
    private VideoVisor video_visor = new VideoVisor();
    private BufferInfo buffer_info = new BufferInfo();
    private ToolbarInfo toolbar_info = new ToolbarInfo();

    public Izquierda(){

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        /*
        //self.efectos_aplicados = Efectos_en_Pipe()
        self.progress = ProgressPlayer()
        */

        vbox.pack_start(this.toolbar_record, false, false, 0);
        vbox.pack_start(this.video_visor, true, true, 0);
        //vbox.pack_start(self.efectos_aplicados, False, False, 0)
        vbox.pack_start(this.buffer_info, false, false, 0);
        vbox.pack_start(this.toolbar_info, false, false, 0);

        /*
        vbox.pack_start(self.progress, False, False, 0)
        */
        this.add(vbox);
        this.show_all();

        this.toolbar_record.detener.connect(this.__emit_stop_record);

        //self.video_visor.connect("ocultar_controles",
        //    self.__emit_show_controls)
        //self.video_visor.connect("button_press_event", self.__set_fullscreen)

        this.toolbar_info.rotar.connect(this.__emit_rotar);
        this.toolbar_info.actualizar_streamings.connect(this.__emit_actualizar_streamings);

        //self.progress.connect("seek", self.__emit_seek)
        //self.progress.connect("volumen", self.__emit_volumen)

    }

    private void __emit_stop_record(){
        this.stop_record();
        }

    private void __emit_rotar(string rotacion){
        this.rotar(rotacion);
        }

    private void __emit_actualizar_streamings(){
        this.actualizar_streamings();
        }
}
