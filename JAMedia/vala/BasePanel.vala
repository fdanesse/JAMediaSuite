public class BasePanel : Gtk.HPaned{

    public signal void menu_activo();
    public signal void stop_record();
    public signal void add_stream(string title);
    public signal void show_controls(bool zona, bool ocultar);
    public signal void configurar(bool valor);
    public signal void actualizar_streamings();
    public signal void accion_list (Lista lista, string accion, Gtk.TreePath path);

    public Izquierda izquierda = null;
    public Derecha derecha = new Derecha();
    private Gtk.Window root = null;
    private JAMediaReproductor player = null;

    public BasePanel(Gtk.Window window){

        this.set_border_width(2);

        this.root = window;
        this.izquierda = new Izquierda(this.root);

        this.pack1(this.izquierda, true, true);
        this.pack2(this.derecha, false, false);

        this.show_all();

        this.derecha.cargar_reproducir.connect(this.__cargar_reproducir);
        this.derecha.accion_list.connect(this.__emit_accion_list);
        this.derecha.menu_activo.connect(this.__emit_menu_activo);
        this.derecha.add_stream.connect(this.__emit_add_stream);
        this.derecha.accion_controls.connect(this.__accion_controls);

        this.derecha.balance_valor.connect(this.__accion_balance);
        //#self.derecha.connect("add_remove_efecto", self.__add_remove_efecto)
        //#self.derecha.connect("configurar_efecto", self.__config_efecto)

        this.izquierda.show_controls.connect(this.__emit_show_controls);
        this.izquierda.rotar.connect(this.__rotar);
        this.izquierda.stop_record.connect(this.__stop_record);
        this.izquierda.seek.connect(this.__user_set_progress);
        this.izquierda.volumen.connect(this.__set_volumen);
        this.izquierda.actualizar_streamings.connect(this.__emit_actualizar_streamings);

        GLib.Timeout.add(5000, this.__check_ip);
    }

    private void __stop_record(){
        this.menu_activo();
        this.stop_record();
        }

    private void __emit_actualizar_streamings(){
        this.menu_activo();
        this.actualizar_streamings();
        //# FIXME: Recargar Lista actual
        }

    /*
    #def __add_remove_efecto(self, widget, efecto, valor):
    #    # Agrega o quita efecto de video.
    #    self.__emit_menu_activo()
    #    print self.__add_remove_efecto, efecto, valor
    #    # agregar el efecto en el bin y en el widget

    #def __config_efecto(self, widget, efecto, propiedad, valor):
    #    # Configurar efecto de video.
    #    self.__emit_menu_activo()
    #    print self.__config_efecto, efecto, propiedad, valor
    */

    private void __accion_balance(string prop, double valor){
        this.__emit_menu_activo();
        this.player.set_balance(prop, valor);
        }

    private void __emit_add_stream(string title){
        this.add_stream(title);
        }

    private void __emit_menu_activo(){
        this.menu_activo();
        this.izquierda.buffer_info.hide();
        }

    private void __emit_accion_list(Lista lista, string accion, Gtk.TreePath path){
        // borrar, copiar, mover, grabar, etc . . .
        this.accion_list(lista, accion, path);
        }

    private void __accion_controls(string accion){
        this.__emit_menu_activo();
        if (accion == "atras"){
            this.derecha.lista.seleccionar_anterior();
            }
        else if (accion == "siguiente"){
            this.derecha.lista.seleccionar_siguiente();
            }
        else if (accion == "stop"){
            if (this.player != null){
                this.player.stop();
                }
            }
        else if (accion == "pausa-play"){
            if (this.player != null){
                this.player.pause_play();
                }
            }
        }

    private void __set_volumen(double valor){
        this.menu_activo();
        if (this.player != null){
            this.player.set_volumen(valor);
            }
        }

    private void __user_set_progress(double valor){
        this.menu_activo();
        if (this.player != null){
            this.player.set_position((int64) valor);
            }
        }

    private void __emit_show_controls(bool zona, bool ocultar){
        this.show_controls(zona, ocultar);
        }

    private void __cargar_reproducir(string path){
        this.derecha.set_sensitive(false);

        double volumen = this.izquierda.progress._volumen.get_value();
        if (this.player != null){
            this.player.stop();
            this.player.unref();
            this.player = null;
        }

        this.izquierda.progress.set_sensitive(false);
        this.__set_video(false);

        uint* xid = this.izquierda.video_visor.xid;
        this.player = new JAMediaReproductor(xid);

        this.player.endfile.connect(this.__endfile);
        this.player.estado.connect(this.__state_changed);
        this.player.video.connect(this.__set_video);
        this.player.newposicion.connect(this.__update_progress);
        this.player.loading_buffer.connect(this.__loading_buffer);

        this.player.load(path);
        this.player.play();

        this.player.set_volumen(volumen);
        this.izquierda.progress._volumen.set_value(volumen);

        this.derecha.set_sensitive(true);
        }

    private void __loading_buffer(int buf){
        this.izquierda.buffer_info.set_progress(buf);
        }

    private void __rotar(string rotacion){
        if (this.player != null){
            this.menu_activo();
            this.player.rotar(rotacion);
            }
        }

    private void __set_video(bool valor){
        this.izquierda.toolbar_info.set_video(valor);
        this.configurar(valor);
        }

    private void __update_progress(int64 valor){
        this.izquierda.progress.set_progress(valor);
        }

    private void __state_changed(string valor){
        if (valor == "playing"){
            this.derecha.player_controls.set_playing();
            this.izquierda.progress.set_sensitive(true);
            GLib.Idle.add(this.__update_balance);
            }
        else if (valor == "paused" || valor == "None"){
            this.derecha.player_controls.set_paused();
            GLib.Idle.add(this.__update_balance);
            }
        else{
            GLib.stdout.printf("Estado del Reproductor desconocido: %s\n", valor);
            GLib.stdout.flush();
            }
        }

    private bool __update_balance(){
        if (this.player != null){
            this.derecha.balance.set_balance("brillo", this.player.get_balance("brillo"));
            this.derecha.balance.set_balance("contraste", this.player.get_balance("contraste"));
            this.derecha.balance.set_balance("saturacion", this.player.get_balance("saturacion"));
            this.derecha.balance.set_balance("hue", this.player.get_balance("hue"));
            this.derecha.balance.set_balance("gamma", this.player.get_balance("gamma"));
            }
        return false;
        }

    private bool __check_ip(){
        bool valor = get_ip();
        this.izquierda.set_ip(valor);
        this.derecha.set_ip(valor);
        return true;
        }

    public void __endfile(){
        this.derecha.player_controls.set_paused();
        this.derecha.lista.seleccionar_siguiente();
        }

    public void stop(){
        if (this.player != null){
            this.player.stop();
            }
        }

    public void setup_init(){
        this.izquierda.setup_init();
        this.derecha.setup_init();
        }

    public void salir(){
        if (this.player != null){
            this.player.stop();
            this.player.unref();
            this.player = null;
            }
        }

    public void set_nueva_lista(SList<string> archivos){
        this.derecha.set_nueva_lista(archivos);
        }
}
