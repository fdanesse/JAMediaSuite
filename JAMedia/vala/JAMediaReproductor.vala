
public class JAMediaReproductor : GLib.Object{
    /*
    __gsignals__ = {
    "loading-buffer": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_INT, )),
        }
    */
    //# Estados: playing, paused, None

    public signal void endfile();
    public signal void estado(string estado);
    public signal void video(bool valor);
    public signal void newposicion(int64 posicion);

    private dynamic Gst.Element player = Gst.ElementFactory.make("playbin", "play");
    private double _volumen = 0.10;
    private string _uri = "";
    private Gst.State _estado = Gst.State.NULL;
    private uint* _ventana_id;

    private JAMedia_Video_Pipeline video_bin;
    private JAMedia_Audio_Pipeline audio_bin;
    private bool progressbar = true;
    private bool _video = false;
    private uint actualizador = 0;
    private int64 duracion = 0;
    private int64 posicion = 0;

    public JAMediaReproductor(uint* ventana_id){

        this._ventana_id = ventana_id;

        this.player.set_property("buffer-size", 50000);

        this.audio_bin = new JAMedia_Audio_Pipeline();
        this.video_bin = new JAMedia_Video_Pipeline();

        this.player.set_property("video-sink", this.video_bin);
        this.player.set_property("audio-sink", this.audio_bin);
        //this.player.set_window_handle(this._ventana_id); //FIXME: error: dynamic methods are not supported for `Gst.Element'

        Gst.Bus bus = this.player.get_bus();
        bus.add_watch(100, this.__sync_message);
    }

    private bool __sync_message(Gst.Bus bus, Gst.Message message){
        switch(message.type){
            case Gst.MessageType.ELEMENT:
                if (message.get_structure().get_name() == "prepare-window-handle"){
                    Gst.Video.Overlay overlay = message.src as Gst.Video.Overlay;
			        assert (overlay != null);
                    overlay.set_window_handle(this._ventana_id);
                    }
                break;

            case Gst.MessageType.STATE_CHANGED:
                Gst.State oldstate;
                Gst.State newstate;
                Gst.State pending;

                message.parse_state_changed(out oldstate, out newstate, out pending);

                if (this._estado != newstate){
                    //FIXME: Se pueden reducir señales afinando esto
                    this._estado = newstate;
                    if (oldstate == Gst.State.PAUSED && newstate == Gst.State.PLAYING){
                        if (this._estado == Gst.State.PLAYING){
                            this.estado("playing");
                            this.__new_handle(true);
                            }
                    }
                    else if (oldstate == Gst.State.READY && newstate == Gst.State.PAUSED){
                        if (this._estado == Gst.State.PAUSED){
                            this.estado("paused");
                            this.__new_handle(false);
                            }
                    }
                    else if (oldstate == Gst.State.READY && newstate == Gst.State.NULL){
                        if (this._estado == Gst.State.NULL){
                            this.estado("None");
                            this.__new_handle(false);
                            }
                    }
                    else if (oldstate == Gst.State.PLAYING && newstate == Gst.State.PAUSED){
                        if (this._estado == Gst.State.PAUSED){
                            this.estado("paused");
                            this.__new_handle(false);
                        }
                    }
                    }
                break;

            case Gst.MessageType.TAG:
                Gst.TagList taglist;
                message.parse_tag(out taglist);
                //GLib.stdout.printf("%s\n", taglist.to_string());
                //GLib.stdout.flush();
                string datos = taglist.to_string();
                if ("video-codec" in datos){
                  if (this._video == false){
                      this._video = true;
                      this.video(this._video);
                      }
                    }
                break;

            case Gst.MessageType.LATENCY:
                //FIXME: error: dynamic methods are not supported for `Gst.Element'
                GLib.stdout.printf("FIXME: Gst.MessageType.LATENCY\n");
                GLib.stdout.flush();
                //this.player.recalculate_latency();
                break;

            case Gst.MessageType.ERROR:
                GLib.Error err;
                string debug;
                message.parse_error(out err, out debug);
                //GLib.stdout.printf("Error: %s\n", err.message);
                //GLib.stdout.flush();
                //this.endfile();
                this.__new_handle(false);
                break;

            case Gst.MessageType.BUFFERING:
                GLib.Value buf = message.get_structure().get_value("buffer-percent");
                GLib.stdout.printf("Buffer: %s\n", (string) buf);
                GLib.stdout.flush();
                break;

            case Gst.MessageType.EOS:
                this.__new_handle(false);
                this.endfile();
                break;
            }
            return true;
        }

    private void __pause(){
        this.player.set_state(Gst.State.PAUSED);
        }

    private void __new_handle(bool reset){
        if (this.actualizador > 0){
            GLib.Source.remove(this.actualizador);
            this.actualizador = 0;
            }
        if (reset == true){
            this.actualizador = GLib.Timeout.add(500, this.__handle);
            }
        }

    private bool __handle(){
        if (! this.progressbar == true){
            return true;
            }
        int64 duracion;
        int64 posicion;
        this.player.query_duration(Gst.Format.TIME, out duracion);
        this.player.query_position(Gst.Format.TIME, out posicion);
        duracion = duracion / Gst.SECOND;
        posicion = posicion / Gst.SECOND;
        int64 pos = posicion * 100 / duracion;
        if (this.duracion != duracion){
            this.duracion = duracion;
            }
        if (pos != this.posicion){
            this.posicion = pos;
            this.newposicion(this.posicion);
            }
        return true;
        }

    public void play(){
        if (this._uri != ""){
            this.player.set_state(Gst.State.PLAYING);
            }
        }

    public void pause_play(){
        if (this._estado == Gst.State.PAUSED || this._estado == Gst.State.NULL || this._estado == Gst.State.READY){
            this.play();
            }
        else if (this._estado == Gst.State.PLAYING){
            this.__pause();
            }
        }

    public void rotar(string valor){
        this.video_bin.rotar(valor);
        }

    public void set_balance(string prop, double valor){
        this.video_bin.set_balance(prop, valor);
        }

    //def get_balance(self):
    //    return self.video_bin.get_balance()

    public void stop(){
        this.__new_handle(false);
        this.player.set_state(Gst.State.NULL);
        this.newposicion(0);
        }

    public bool load(string uri){
        if (uri == ""){
            return false;
            }
        this.duracion = 0;
        this.posicion = 0;
        this.newposicion(this.posicion);
        //self.emit("loading-buffer", 100)

        this._uri = uri;
        GLib.File file = GLib.File.parse_name(uri);
        if(file.query_exists()){
            this._uri = file.get_uri();
            this.progressbar = true;
            }
        else{
            this.progressbar = false;
            }
        this.player.set_property("uri", this._uri);
        return false;
        }

    /*
    def set_position(self, posicion):
        if not self.progressbar:
            return
        if self.duracion < posicion:
            return
        if self.duracion == 0 or posicion == 0:
            return
        posicion = self.duracion * posicion / 100

        # http://pygstdocs.berlios.de/pygst-reference/gst-constants.html
        #self.player.set_state(gst.STATE_PAUSED)
        # http://nullege.com/codes/show/
        #   src@d@b@dbr-HEAD@trunk@src@reproductor.py/72/gst.SEEK_TYPE_SET
        #self.player.seek(
        #    1.0,
        #    gst.FORMAT_TIME,
        #    gst.SEEK_FLAG_FLUSH,
        #    gst.SEEK_TYPE_SET,
        #    posicion,
        #    gst.SEEK_TYPE_SET,
        #    self.duracion)
        # http://nullege.com/codes/show/
        #   src@c@o@congabonga-HEAD@congaplayer@congalib@engines@gstplay.py/
        #   104/gst.SEEK_FLAG_ACCURATE

        event = gst.event_new_seek(
            1.0, gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
            gst.SEEK_TYPE_SET, posicion * 1000000000,
            gst.SEEK_TYPE_NONE, self.duracion * 1000000000)
        self.player.send_event(event)
        #self.player.set_state(gst.STATE_PLAYING)
        */

    public void set_volumen(double volumen){
        this.player.set_property("volume", volumen);
        }

    // FIXME: No se usa, además no funciona: error: Argument 2: Cannot pass out argument to non-output parameter
    //public double get_volumen(){
    //    GLib.Value vol;
    //    this.player.get_property("volume", out vol);
    //    return vol.get_double();
    //    }
}
