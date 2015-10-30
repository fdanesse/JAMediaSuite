public class Izquierda : Gtk.EventBox{

    public signal void volumen(double valor);
    public signal void stop_record();
    public signal void rotar(string rotacion);
    public signal void actualizar_streamings();
    public signal void show_controls(bool zona, bool ocultar);
    public signal void seek(double valor);

    public ToolbarGrabar toolbar_record = new ToolbarGrabar();
    public VideoVisor video_visor = new VideoVisor();
    public BufferInfo buffer_info = new BufferInfo();
    public ToolbarInfo toolbar_info = new ToolbarInfo();
    public ProgressPlayer progress = new ProgressPlayer();

    private Gtk.Window root = null;

    public Izquierda(Gtk.Window window){

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        this.root = window;

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

        this.video_visor.ocultar_controles.connect(this.__emit_show_controls);
        this.video_visor.button_press_event.connect ((event) => {
			this.__set_fullscreen(event);
			return true;
		});

        this.toolbar_info.rotar.connect(this.__emit_rotar);
        this.toolbar_info.actualizar_streamings.connect(this.__emit_actualizar_streamings);

        this.progress.seek.connect(this.__emit_seek);
        this.progress.volumen.connect(this.__emit_volumen);
    }

    private void __emit_volumen(double valor){
        this.volumen(valor);
        }

    private void __emit_seek(double valor){
        this.seek(valor);
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

    private void __set_fullscreen(Gdk.EventButton event){
        if (event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS){
            this.set_sensitive(false);
            var screen = this.root.get_screen();
            int w = (int) this.root.get_allocated_width();
            int h = (int) this.root.get_allocated_height();
            int ww = (int) screen.get_width ();
            int hh = (int) screen.get_height ();
            if (ww == w && hh == h){
                this.root.set_border_width(2);
                GLib.Idle.add(this.__unfullscreen);
                }
            else{
                this.root.set_border_width(0);
                GLib.Idle.add(this.__fullscreen);
                }
            this.set_sensitive(true);
            }
        }

    private bool __fullscreen(){
        this.root.fullscreen();
        return false;
        }

    private bool __unfullscreen(){
        this.root.unfullscreen();
        return false;
        }

    private void __emit_show_controls(bool valor){
        bool zona = valor;
        bool ocultar = this.toolbar_info.ocultar_controles;
        this.show_controls(zona, ocultar);
        }

    public void setup_init(){
        this.toolbar_record.hide();
        this.buffer_info.hide();
        //this.efectos_aplicados.hide();
        this.toolbar_info.set_video(false);
        this.progress.set_sensitive(false);
        }

    public void set_ip(bool valor){
        this.toolbar_info.set_ip(valor);
        }
}
