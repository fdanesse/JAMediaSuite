public class BasePanel : Gtk.HPaned{

    //__gsignals__ = {
    //"accion-list": (gobject.SIGNAL_RUN_LAST,
    //    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
    //    gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    public signal void menu_activo();
    public signal void stop_record();
    public signal void add_stream(string title);
    public signal void show_controls(bool zona, bool ocultar);
    public Izquierda izquierda = null;
    public Derecha derecha = new Derecha();

    private Gtk.Window root = null;

    public BasePanel(Gtk.Window window){

        this.set_border_width(2);
        /*
        self._thread = False
        self.player = False
        */

        this.root = window;
        this.izquierda = new Izquierda(this.root);

        this.pack1(this.izquierda, true, true);
        this.pack2(this.derecha, false, false);

        this.show_all();

        this.derecha.cargar_reproducir.connect(this.__cargar_reproducir);
        //self.derecha.connect("accion-list", self.__emit_accion_list)

        this.derecha.menu_activo.connect(this.__emit_menu_activo);
        this.derecha.add_stream.connect(this.__emit_add_stream);
        this.derecha.accion_controls.connect(this.__accion_controls);

        //self.derecha.connect("balance-valor", self.__accion_balance)
        //#self.derecha.connect("add_remove_efecto", self.__add_remove_efecto)
        //#self.derecha.connect("configurar_efecto", self.__config_efecto)

        this.izquierda.show_controls.connect(this.__emit_show_controls);
        this.izquierda.rotar.connect(this.__rotar);
        this.izquierda.stop_record.connect(this.__stop_record);
        //self.izquierda.connect("seek", self.__user_set_progress)
        this.izquierda.volumen.connect(this.__set_volumen);
        this.izquierda.actualizar_streamings.connect(this.__actualizar_streamings);

        GLib.Timeout.add(5000, this.__check_ip);
    }

    private void __stop_record(){
        this.menu_activo();
        this.stop_record();
        }

    private void __actualizar_streamings(){
        GLib.stdout.printf("FIXME: __actualizar_streamings");
        GLib.stdout.flush();
        this.menu_activo();
        //dialog = DialogoDescarga(parent=self.get_toplevel(), force=True)
        //dialog.run()
        //dialog.destroy()
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

    def __accion_balance(self, widget, valor, prop):
        # Setea valores de Balance en el reproductor.
        self.__emit_menu_activo()
        if prop == "saturacion":
            self.player.set_balance(saturacion=valor)
        elif prop == "contraste":
            self.player.set_balance(contraste=valor)
        elif prop == "brillo":
            self.player.set_balance(brillo=valor)
        elif prop == "hue":
            self.player.set_balance(hue=valor)
        elif prop == "gamma":
            self.player.set_balance(gamma=valor)
    */

    private void __emit_add_stream(string title){
        this.add_stream(title);
        }

    private void __emit_menu_activo(){
        this.menu_activo();
        this.izquierda.buffer_info.hide();
        }

    /*
    def __emit_accion_list(self, widget, lista, accion, _iter):
        # borrar, copiar, mover, grabar, etc . . .
        self.emit("accion-list", lista, accion, _iter)
    */

    private void __accion_controls(string accion){
        this.__emit_menu_activo();
        if (accion == "atras"){
            this.derecha.lista.seleccionar_anterior();
            }
        else if (accion == "siguiente"){
            this.derecha.lista.seleccionar_siguiente();
            }
        else if (accion == "stop"){
            //FIXME: Implementar
            //if self.player:
            //    self.player.stop()
            }
        else if (accion == "pausa-play"){
            //if self.player:
            //    self.player.pause_play()
            }
        }

    private void __set_volumen(double valor){
        this.menu_activo();
        //if self.player:
        //    self.player.set_volumen(valor)
        }

    //def __user_set_progress(self, widget, valor):
    //    this.menu_activo();
    //    if self.player:
    //        self.player.set_position(valor)

    private void __emit_show_controls(bool zona, bool ocultar){
        this.show_controls(zona, ocultar);
        }

    private void __cargar_reproducir(string path){
        GLib.stdout.printf("FIXME: Load: %s\n", path);
        GLib.stdout.flush();
        /*
        self.derecha.set_sensitive(False)

        # FIXME: Analizar mantener los siguientes valores:
        # Efectos
        # balanace
        # Gamma
        # Rotacion
        # Volumen

        volumen = 1.0
        if self.player:
            volumen = float("{:.1f}".format(
                self.izquierda.progress.volumen.get_value() * 10))
            self.player.disconnect_by_func(self.__endfile)
            self.player.disconnect_by_func(self.__state_changed)
            self.player.disconnect_by_func(self.__update_progress)
            self.player.disconnect_by_func(self.__set_video)
            self.player.disconnect_by_func(self.__loading_buffer)
            self.player.stop()
            del(self.player)
            self.player = False

        self.izquierda.progress.set_sensitive(False)
        self.__set_video(False, False)

        xid = self.izquierda.video_visor.get_property('window').xid
        self.player = JAMediaReproductor(xid)

        self.player.connect("endfile", self.__endfile)
        self.player.connect("estado", self.__state_changed)
        self.player.connect("newposicion", self.__update_progress)
        self.player.connect("video", self.__set_video)
        self.player.connect("loading-buffer", self.__loading_buffer)

        self.player.load(path)
        self._thread = threading.Thread(target=self.player.play)
        self._thread.start()
        self.player.set_volumen(volumen)
        self.izquierda.progress.volumen.set_value(volumen / 10)
        self.derecha.set_sensitive(True)
        */
        }

    private void __loading_buffer(double buf){
        this.izquierda.buffer_info.set_progress(buf);
        }

    private void __rotar(string rotacion){
        //if self.player:
        //    this.menu_activo();
        //    self.player.rotar(rotacion)
        }

    private void __set_video(bool valor){
        this.izquierda.toolbar_info.set_video(valor);
        //FIXME: this.get_parent().get_parent().toolbar.configurar.set_sensitive(valor);
        }

    private void __update_progress(double valor){
        this.izquierda.progress.set_progress(valor);
        }

    private void __state_changed(string valor){
        // FIXME: Implementar
        //if "playing" in valor:
        //    self.derecha.player_controls.set_playing()
        //    self.izquierda.progress.set_sensitive(True)
        //elif "paused" in valor or "None" in valor:
        //    self.derecha.player_controls.set_paused()
        //else:
        //    print "Estado del Reproductor desconocido:", valor
        //gobject.idle_add(self.__update_balance)
        }

    private bool __update_balance(){
        //FIXME: Implementar
        //config = {}
        //if self.player:
        //    config = self.player.get_balance()
        //self.derecha.balance.set_balance(
        //    brillo=config.get('brillo', 50.0),
        //    contraste=config.get('contraste', 50.0),
        //    saturacion=config.get('saturacion', 50.0),
        //    hue=config.get('hue', 50.0),
        //    gamma=config.get('gamma', 10.0))
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

    public void setup_init(){
        this.izquierda.setup_init();
        this.derecha.setup_init();
        }

    public void salir(){
        // FIXME: Salir
        //if self.player:
        //    self.player.disconnect_by_func(self.__endfile)
        //    self.player.disconnect_by_func(self.__state_changed)
        //    self.player.disconnect_by_func(self.__update_progress)
        //    self.player.disconnect_by_func(self.__set_video)
        //    self.player.disconnect_by_func(self.__loading_buffer)
        //    self.player.stop()
        //    del(self.player)
        //    self.player = False
        }

    public void set_nueva_lista(SList<string> archivos){
        this.derecha.set_nueva_lista(archivos);
        }

    public void checkear_listas(){
        // FIXME: Descargar Streamings
        //dialog = DialogoDescarga(parent=self.get_toplevel(), force=False)
        //dialog.run()
        //dialog.destroy()
        }
}
