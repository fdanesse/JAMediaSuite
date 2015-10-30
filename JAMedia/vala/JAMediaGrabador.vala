
public class JAMediaGrabador : GLib.Object{

    public signal void endfile();
    public signal void update(string info);

    private Gst.Pipeline pipeline = new Gst.Pipeline("JAMediaGrabador");
    private Gst.Element player = Gst.ElementFactory.make("uridecodebin", "uridecodebin");
    private Gst.Element archivo = Gst.ElementFactory.make("filesink", "filesink");
    private uint actualizador = 0;
    private string patharchivo = null;
    private int control = 0;
    private double tamanio = 0.0;
    private string uri = null;
    private string tipo = null;
    private Gst.Pad audio_sink = null;
    private Gst.Pad video_sink = null;

    public JAMediaGrabador(string uri, string arch, string tipo){

        this.tipo = tipo;
        string archivo = arch;

        if (archivo.has_suffix(".ogg") == false){
            archivo = string.join("", archivo, ".ogg");
            }

        this.patharchivo = archivo.replace(" ", "_");

        this.player.set_property("buffer-size", 40000);
        this.player.set_property("download", true);

        this.pipeline.add(this.player);

        // AUDIO
        Gst.Element audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert");
        Gst.Element audioresample = Gst.ElementFactory.make("audioresample", "audioresample");
        audioresample.set_property("quality", 10);
        Gst.Element vorbisenc = Gst.ElementFactory.make("vorbisenc", "vorbisenc");

        this.pipeline.add(audioconvert);
        this.pipeline.add(audioresample);
        this.pipeline.add(vorbisenc);

        audioconvert.link(audioresample);
        audioresample.link(vorbisenc);

        this.audio_sink = audioconvert.get_static_pad("sink");

        // VIDEO
        Gst.Element videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert");
        Gst.Element videorate = Gst.ElementFactory.make("videorate", "videorate");

        try{
            videorate.set_property("max-rate", 30);
            }
        catch{}

        Gst.Element theoraenc = Gst.ElementFactory.make("theoraenc", "theoraenc");

        if (this.tipo == "video"){
            this.pipeline.add(videoconvert);
            this.pipeline.add(videorate);
            this.pipeline.add(theoraenc);

            videoconvert.link(videorate);
            videorate.link(theoraenc);
            }

        this.video_sink = videoconvert.get_static_pad("sink");

        // MUXOR y ARCHIVO
        Gst.Element oggmux = Gst.ElementFactory.make("oggmux", "oggmux");

        this.pipeline.add(oggmux);
        this.pipeline.add(this.archivo);

        vorbisenc.link(oggmux);

        if (this.tipo == "video"){
            theoraenc.link(oggmux);
            }

        oggmux.link(this.archivo);

        Gst.Bus bus = this.pipeline.get_bus();
        bus.add_watch(100, this.__sync_message);

        this.player.pad_added.connect(this.__pad_added);

        this.load(uri);
    }

    private bool __sync_message(Gst.Bus bus, Gst.Message message){
        switch(message.type){
            case Gst.MessageType.STATE_CHANGED:
                break;

            case Gst.MessageType.LATENCY:
                //FIXME: error: dynamic methods are not supported for `Gst.Element'
                // FIXME: CRITICAL **: vala_variable_get_variable_type: assertion 'self != NULL' failed
                //this.player.recalculate_latency();
                break;

            case Gst.MessageType.ERROR:
                GLib.Error err;
                string debug;
                message.parse_error(out err, out debug);
                //GLib.stdout.printf("Error: %s\n", err.message);
                //GLib.stdout.flush();
                this.__new_handle(false);
                break;

            case Gst.MessageType.EOS:
                this.__new_handle(false);
                this.endfile();
                break;
            }
            return true;
        }

    private void __pad_added(Gst.Element uridecodebin, Gst.Pad pad){
        Gst.Caps caps = pad.get_current_caps();
        string text = caps.to_string();
        if (text.has_prefix("audio")){
            if (this.audio_sink.is_linked() == false){
                pad.link(this.audio_sink);
                }
            }
        else if (text.has_prefix("video")){
            if (this.video_sink.is_linked() == false){
                pad.link(this.video_sink);
                }
            }
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
        GLib.File file = GLib.File.parse_name(this.patharchivo);
        if (file.query_exists()){
            int64 tam = 0;
            tam = file.query_info ("*", FileQueryInfoFlags.NONE).get_size ();
            double tamanio = double.parse(tam.to_string()) / 1024.0 / 1024.0;

            if (this.tamanio != tamanio){
                this.control = 0;
                this.tamanio = tamanio;
                string texto = this.uri;
                // FIXME: Verificar
                //if len(self.uri) > 25:
                //    texto = str(self.uri[0:25]) + " . . . "
                string info = "Grabando: %s %.2f Mb".printf(texto, this.tamanio);
                this.update(info);
                }
            else{
                this.control ++;
                }
            }

        if (this.control > 60){
            this.stop();
            this.endfile();
            return false;
            }
        return true;
        }

    public void play(){
        this.pipeline.set_state(Gst.State.PLAYING);
        this.__new_handle(true);
        }

    public void stop(){
        this.pipeline.set_state(Gst.State.NULL);
        this.__new_handle(false);
        // FIXME: Verificar
        //if os.path.exists(self.patharchivo):
        //    os.chmod(self.patharchivo, 0755)
        }

    public bool load(string uri){
        if (uri == ""){
            return false;
            }
        GLib.stdout.printf("JAMediaGrabador %s\n", uri);
        GLib.stdout.flush();
        if (Gst.URI.is_valid(uri)){
            this.archivo.set_property("location", this.patharchivo);
            this.uri = uri;
            this.player.set_property("uri", this.uri);
            }
        else{
            GLib.stdout.printf("JAMediaGrabador: uri inválida: %s\n", uri);
            GLib.stdout.flush();
            this.endfile();
            }
        return false;
        }
}

/*
def update(grabador, datos):
    print datos


def end(grabador):
    sys.exit(0)
*/

/*
if __name__ == "__main__":
    print "Iniciando Grabador . . ."

    if not len(sys.argv) == 4:
        print "Debes pasar tres parámetros:"
        print "\t Dirección origen, puede ser url o file path."
        print "\t Nombre de archivo final, puede ser path completo o solo el nombre."
        print "\t Tipo de contenido, puede ser audio o video."

        sys.exit(0)

    uri = sys.argv[1]
    archivo = sys.argv[2]
    tipo = sys.argv[3]

    # FIXME: Esto Provoca: Violación de segmento
    grabador = JAMediaGrabador(uri, archivo, tipo)

    grabador.connect("update", update)
    grabador.connect("endfile", end)
*/
