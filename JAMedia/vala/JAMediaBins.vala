
public class JAMedia_Audio_Pipeline : Gst.Pipeline{

    public JAMedia_Audio_Pipeline(){

        this.set_name("jamedia_audio_pipeline");

        Gst.Element convert = Gst.ElementFactory.make("audioconvert", "convert");
        Gst.Element sink = Gst.ElementFactory.make("autoaudiosink", "sink");

        this.add(convert);
        this.add(sink);

        convert.link(sink);

        Gst.GhostPad ghost_pad = new Gst.GhostPad("sink", convert.get_static_pad("sink"));
        ghost_pad.set_target(convert.get_static_pad("sink"));
        this.add_pad(ghost_pad);
    }
}


public class JAMedia_Video_Pipeline : Gst.Pipeline{

    public double saturacion = 50.0;
    public double contraste = 50.0;
    public double brillo = 50.0;
    public double hue = 50.0;
    public double gamma = 10.0;
    public double rotacion = 0;

    public JAMedia_Video_Pipeline(){

        this.set_name("jamedia_video_pipeline");

        Gst.Element convert = Gst.ElementFactory.make("videoconvert", "videoconvert");
        Gst.Element rate = Gst.ElementFactory.make("videorate", "rate");
        Gst.Element videobalance = Gst.ElementFactory.make("videobalance", "videobalance");
        Gst.Element gamma = Gst.ElementFactory.make("gamma", "gamma");
        Gst.Element videoflip = Gst.ElementFactory.make("videoflip", "videoflip");
        Gst.Element pantalla = Gst.ElementFactory.make("xvimagesink", "pantalla");
        pantalla.set_property("force-aspect-ratio", true);

        //var xoverlay = pantalla as Gst.XOverlay;
        //xoverlay.set_xwindow_id (ventana_id);

        try{ //# FIXME: xo no posee esta propiedad
            rate.set_property("max-rate", 30);
            }
        catch{}

        this.add(convert);
        this.add(rate);
        this.add(videobalance);
        this.add(gamma);
        this.add(videoflip);
        this.add(pantalla);

        convert.link(rate);
        rate.link(videobalance);
        videobalance.link(gamma);
        gamma.link(videoflip);
        videoflip.link(pantalla);

        Gst.GhostPad ghost_pad = new Gst.GhostPad("sink", convert.get_static_pad("sink"));
        ghost_pad.set_target(convert.get_static_pad("sink"));
        this.add_pad(ghost_pad);
        }

    public void rotar(string valor){
        GLib.Value r = 0;
        this.get_by_name("videoflip").get_property("method", ref r);
        int rot = r.get_int();
        if (valor == "Derecha"){
            if (rot < 3){
                rot += 1;
                }
            else{
                rot = 0;
                }
            }
        else if (valor == "Izquierda"){
            if (rot > 0){
                rot -= 1;
                }
            else{
                rot = 3;
                }
            }
        this.get_by_name("videoflip").set_property("method", rot);
        }

    public void set_balance(string prop, double valor){
        if (prop == "brillo"){
            this.brillo = valor;
            double val = (2.0 * valor / 100.0) - 1.0;
            this.get_by_name("videobalance").set_property("brightness", val);
            }
        else if (prop == "contraste"){
            this.contraste = valor;
            double val = 2.0 * valor / 100.0;
            this.get_by_name("videobalance").set_property("contrast", val);
            }
        else if (prop == "saturacion"){
            this.saturacion = valor;
            double val = 2.0 * valor / 100.0;
            this.get_by_name("videobalance").set_property("saturation", val);
            }
        else if (prop == "hue"){
            this.hue = valor;
            double val = (2.0 * valor / 100.0) - 1.0;
            this.get_by_name("videobalance").set_property("hue", val);
            }
        else if (prop == "gamma"){
            this.gamma = valor;
            double val = (10.0 * valor / 100.0);
            this.get_by_name("gamma").set_property("gamma", val);
            }
        }

    public double get_balance(string prop){
        if (prop == "brillo"){
            return this.brillo;
            }
        else if (prop == "contraste"){
            return this.contraste;
            }
        else if (prop == "saturacion"){
            return this.saturacion;
            }
        else if (prop == "hue"){
            return this.hue;
            }
        else if (prop == "gamma"){
            return this.gamma;
            }
        else{
            return 0.0;
            }
        }
}
