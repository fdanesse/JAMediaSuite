
public class UbuntuRadioPlayer : GLib.Object{
    /*
    Reproductor Gstreamer Básico de la Aplicación.
    */

    private GLib.MainLoop loop = new GLib.MainLoop();
    private dynamic Gst.Element player = Gst.ElementFactory.make(
        "playbin", "play");

    public double _volumen = 0.10;
    public string _uri = "";
    public string _estado = "None";

    public signal void endfile();
    public signal void estado(string estado);

    public UbuntuRadioPlayer (){

        Gst.Bus bus = this.player.get_bus();
        bus.enable_sync_message_emission();

        bus.sync_message.connect(this.sync_message);

        this.set_volumen(this._volumen);
    }

    public void set_volumen (double valor){

        this._volumen = valor;
        this.player.volume = this._volumen;
    }

    public void load(string uri){
        /*
        if os.path.exists(uri):
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)

        else:
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
        */
        this.stop();
        this._uri = uri;
        this.player.uri = this._uri;
        this.play();
    }

    public void play(){
        /* Reproduce un Streaming */

        if (this._uri != ""){
            this.player.set_state(Gst.State.PLAYING);
            loop.run();
        }
    }

    public void stop(){

        this.player.set_state(Gst.State.NULL);
        loop.quit();
    }

    private void sync_message (Gst.Message message){
        /* Manejo de Señales del Bus */

        switch(message.type){

            case Gst.MessageType.ERROR:
                GLib.Error err;
                string debug;
                message.parse_error(out err, out debug);
                stdout.printf("Error: %s\n", err.message);
                this.endfile();
                this.stop();
                break;

            case Gst.MessageType.LATENCY:
                //FIXME: dynamic methods are not supported for `Gst.Element'
                //this.player.recalculate_latency();
                break;

            case Gst.MessageType.EOS:
                this.endfile();
                this.stop();
                break;

            case Gst.MessageType.STATE_CHANGED:
                Gst.State oldstate;
                Gst.State newstate;
                Gst.State pending;

                message.parse_state_changed(
                    out oldstate, out newstate, out pending);

                if (oldstate == Gst.State.PAUSED && newstate == Gst.State.PLAYING){
                    if (this._estado != "playing"){
                        this._estado = "playing";
                        this.estado("playing");
                        }
                }
                else if (oldstate == Gst.State.READY && newstate == Gst.State.PAUSED){
                    if (this._estado != "paused"){
                        this._estado = "paused";
                        this.estado("paused");
                        }
                }
                else if (oldstate == Gst.State.READY && newstate == Gst.State.NULL){
                    if (this._estado != "None"){
                        this._estado = "None";
                        this.estado("None");
                        }
                }
                else if (oldstate == Gst.State.PLAYING && newstate == Gst.State.PAUSED){
                    if (this._estado != "paused"){
                        this._estado = "paused";
                        this.estado("paused");
                    }
                }

                break;

            default:
                break;
        }
    }
}
