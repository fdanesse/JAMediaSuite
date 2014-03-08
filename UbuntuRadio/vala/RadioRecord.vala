
public class UbuntuRadioRecord : GLib.Object{
    /*
    Reproductor Gstreamer Básico de la Aplicación.
    */

    private GLib.MainLoop loop = new GLib.MainLoop();

    private Gst.Pipeline pipeline = new Gst.Pipeline("Record");
    private Gst.Element player = Gst.ElementFactory.make(
        "uridecodebin", "uridecodebin");
    private Gst.Pad audio_sink;
    private Gst.Element archivo = Gst.ElementFactory.make(
        "filesink", "filesink");

    public string _uri = "";
    public string _estado = "None";
    public string _formato = "ogg";

    public signal void endfile();
    public signal void estado(string estado);
    public signal void update(string info);

    public UbuntuRadioRecord (){

        this.pipeline.add(this.player);

        Gst.Element audioconvert = Gst.ElementFactory.make(
            "audioconvert", "audioconvert");
        Gst.Element audioresample = Gst.ElementFactory.make(
            "audioresample", "audioresample");
        audioresample.set_property("quality", 10);

        this.pipeline.add(audioconvert);
        this.pipeline.add(audioresample);

        audioconvert.link(audioresample);

        this.audio_sink = audioconvert.get_static_pad("sink");

        this.pipeline.add(this.archivo);

        if (this._formato == "ogg"){
            Gst.Element vorbisenc = Gst.ElementFactory.make(
                "vorbisenc", "vorbisenc");
            Gst.Element oggmux = Gst.ElementFactory.make(
                "oggmux", "oggmux");

            this.pipeline.add(vorbisenc);
            this.pipeline.add(oggmux);

            audioresample.link(vorbisenc);
            vorbisenc.link(oggmux);
            oggmux.link(this.archivo);
            }
        /*
        elif self.formato == "mp3":
            lamemp3enc = Gst.ElementFactory.make(
                "lamemp3enc", "lamemp3enc")

            self.pipeline.add(lamemp3enc)

            audioresample.link(lamemp3enc)
            lamemp3enc.link(self.archivo)

        elif self.formato == "wav":
            wavenc = Gst.ElementFactory.make(
                "wavenc", "wavenc")

            self.pipeline.add(wavenc)

            audioresample.link(wavenc)
            wavenc.link(self.archivo)
        */
        Gst.Bus bus = this.player.get_bus();
        bus.enable_sync_message_emission();

        bus.sync_message.connect(this.sync_message);
        this.player.pad_added.connect(this.on_pad_added);
    }

    private void on_pad_added(Gst.Pad pad){
        /*
        Agregar elementos en forma dinámica según
        sean necesarios.
        */
        /*
        string = pad.query_caps(None).to_string()

        if string.startswith('audio/'):
            pad.link(self.audio_sink)
        */
        pad.link(this.audio_sink);
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
        //this.player.uri = this._uri;
        //FIXME: activarlo no devuelve el control a Gtk.
        this.play();
    }

    public void play(){
        /*
        if (this._uri != ""){
            this.player.set_state(Gst.State.PLAYING);
            this.loop.run();
        }
        */
        /*
    def play(self, name):

        import time
        import datetime

        hora = time.strftime("%H-%M-%S")
        fecha = str(datetime.date.today())

        from Globales import get_my_files_directory

        archivo = "%s-%s-%s.%s" % (
            name.replace(" ", "_"),
            fecha, hora, self.formato)
        self.patharchivo = os.path.join(
            get_my_files_directory(), archivo)

        self.archivo.set_property(
            "location", self.patharchivo)

        if not self.estado == Gst.State.PLAYING:
            self.estado = Gst.State.PLAYING
            self.emit("estado", "playing")
            self.pipeline.set_state(Gst.State.PLAYING)

        self.__new_handle(True)
        */
    }

    public void stop(){

        this.player.set_state(Gst.State.NULL);
        this.loop.quit();
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
