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
    public BufferInfo buffer_info = new BufferInfo();
    private ToolbarInfo toolbar_info = new ToolbarInfo();
    private ProgressPlayer progress = new ProgressPlayer();

    public Izquierda(){

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        //self.efectos_aplicados = Efectos_en_Pipe()

        vbox.pack_start(this.toolbar_record, false, false, 0);
        vbox.pack_start(this.video_visor, true, true, 0);
        //vbox.pack_start(self.efectos_aplicados, False, False, 0)
        vbox.pack_start(this.buffer_info, false, false, 0);
        vbox.pack_start(this.toolbar_info, false, false, 0);
        vbox.pack_start(this.progress, false, false, 0);

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

    /*
    def __emit_volumen(self, widget, valor):
        self.emit('volumen', valor)

    def __emit_seek(self, widget, valor):
        self.emit("seek", valor)
    */

    private void __emit_stop_record(){
        this.stop_record();
        }

    private void __emit_rotar(string rotacion){
        this.rotar(rotacion);
        }

    private void __emit_actualizar_streamings(){
        this.actualizar_streamings();
        }

    /*
    def __set_fullscreen(self, widget, event):
        if event.type.value_name == "GDK_2BUTTON_PRESS":
            win = self.get_toplevel()
            widget.set_sensitive(False)
            screen = win.get_screen()
            w, h = win.get_size()
            ww, hh = (screen.get_width(), screen.get_height())
            if ww == w and hh == h:
                win.set_border_width(2)
                gobject.idle_add(self.__set_full, win, False)
            else:
                win.set_border_width(0)
                gobject.idle_add(self.__set_full, win, True)
            widget.set_sensitive(True)

    def __set_full(self, win, valor):
        if valor:
            win.fullscreen()
        else:
            win.unfullscreen()

    def __emit_show_controls(self, widget, valor):
        zona, ocultar = (valor, self.toolbar_info.ocultar_controles)
        self.emit("show-controls", (zona, ocultar))

    */

    public void setup_init(){
        this.toolbar_record.hide();
        this.buffer_info.hide();
        //this.efectos_aplicados.hide();
        this.toolbar_info.set_video(false);
        this.progress.set_sensitive(false);
        }

    /*
    def set_ip(self, valor):
        self.toolbar_info.set_ip(valor)
    */
}
