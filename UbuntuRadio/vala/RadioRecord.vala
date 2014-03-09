
//http://references.valadoc.org/#!api=gstreamer-1.0/Gst.Element

public class UbuntuRadioRecord : GLib.Object{
    /*
    Reproductor Gstreamer Básico de la Aplicación.
    */

    //private GLib.MainLoop loop = new GLib.MainLoop();

    private Gst.Pipeline pipeline = new Gst.Pipeline("Record");
    private dynamic Gst.Element player = Gst.ElementFactory.make(
        "uridecodebin", "uridecodebin");
    private Gst.Pad audio_sink;
    private Gst.Element archivo = Gst.ElementFactory.make(
        "filesink", "filesink");

    public string _name = "";
    public string patharchivo = "";
    public string _uri = "";
    public string _estado = "None";
    public string _formato = "ogg";
    private uint actualizador = 0;

    public signal void endfile();
    public signal void estado(string estado);
    public signal void update(string info);

    public UbuntuRadioRecord (string _name, string uri, string formato){

        this._name = _name;
        this._uri = uri;
        this._formato = formato;

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
        Gst.Bus bus = this.pipeline.get_bus();
        bus.enable_sync_message_emission();

        bus.sync_message.connect(this.sync_message);

        this.player.pad_added.connect(this.on_pad_added);

        if (this._uri != "" && this._name != "" && this._formato != ""){
            this.load(this._uri);
            }
        else{
            this.stop();
        }
    }

    private void on_pad_added(Gst.Element src, Gst.Pad pad){
        /*
        Agregar elementos en forma dinámica según
        sean necesarios.
        */

        Gst.Caps new_pad_caps = pad.query_caps (null);
		weak Gst.Structure new_pad_struct = new_pad_caps.get_structure (0);
		string new_pad_type = new_pad_struct.get_name ();

		if (new_pad_type.has_prefix ("audio/")){
            Gst.PadLinkReturn ret = pad.link (this.audio_sink);
		    if (ret != Gst.PadLinkReturn.OK) {
			    stdout.printf ("Pad Tipo %s - link ha fallado.\n", new_pad_type);
		    } else {
			    stdout.printf ("Linkeado pad de Tipo: %s\n", new_pad_type);
		    }
        }
    }

    private void load(string uri){
        /*
        if os.path.exists(uri):
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)

        else:
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
        */

        if (this._estado == "None"){
            this.player.set("uri", this._uri);
            this.play();
        }
        else{
            stdout.printf("Grabador activo");
        }
    }

    public void play(){

        /*
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
        */

        string _path = this._name.replace(" ", "_") + "." + this._formato;
        string home = GLib.Environment.get_variable("HOME");
        this.patharchivo = GLib.Path.build_filename(
            home, "JAMediaDatos2", "MisArchivos", _path);

        this.archivo.set("location", this.patharchivo);
        if (this._uri != ""){
            Gst.StateChangeReturn ret = this.pipeline.set_state(Gst.State.PLAYING);
            if (ret == Gst.StateChangeReturn.SUCCESS) {
                this._estado = "playing";
                this.estado(this._estado);
                this.new_handle(true);
                //this.loop.run();
		            }
            else{
                stderr.puts ("No se ha podido Reproducir el streaming.\n");
                this._estado = "None";
                this.estado(this._estado);
                this.new_handle(false);
                //FIXME: Agregar eliminar el archivo ?
                }
            }
    }

    public void stop(){

        this._estado = "None";
        this.estado(this._estado);
        this.new_handle(false);
        this.pipeline.set_state(Gst.State.NULL);
        //this.loop.quit();
    }

    private void new_handle(bool reset){

        if (this.actualizador > 0){
            GLib.Source.remove(this.actualizador);
            this.actualizador = 0;
            }

        if (reset == true){
            this.actualizador = GLib.Timeout.add(
                500, this.handle);
            }
        }

    private bool handle(){
        /*
        Consulta el estado y progreso de
        la grabacion.
        */
        /*
        if os.path.exists(self.patharchivo):
            tamanio = float(os.path.getsize(
                self.patharchivo) / 1024.0 / 1024.0)

            texto = str(self.uri)

            if len(self.uri) > 25:
                texto = str(self.uri[0:25]) + " . . . "

            info = "Grabando: %s %.2f Mb" % (
                texto, tamanio)

            if self.info != info:
                self.control = 0
                self.info = info
                self.emit('update', self.info)

            else:
                self.control += 1

        if self.control > 60:
            self.stop()
            #self.emit("endfile")
            return False
        */
        return true;
    }

    private void sync_message (Gst.Message message){
        // Manejo de Señales del Bus

        switch(message.type){

            case Gst.MessageType.ERROR:
                GLib.Error err;
                string debug;
                message.parse_error(out err, out debug);
                stdout.printf("Error: %s\n", err.message);
                this._estado = "None";
                this.estado(this._estado);
                this.endfile();
                this.new_handle(false);
                //this.stop();
                break;

            case Gst.MessageType.LATENCY:
                //FIXME: dynamic methods are not supported for `Gst.Element'
                //this.player.recalculate_latency();
                break;

            case Gst.MessageType.EOS:
                this._estado = "None";
                this.estado(this._estado);
                this.endfile();
                this.new_handle(false);
                //this.stop();
                break;

            default:
                break;
        }
    }
}
