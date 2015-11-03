

internal class Canales : Gtk.Window{

    public signal void canal_changed(double r, double g, double b, double h);

    private ImgProcessor processor = null;
    private FrameCanal red = new FrameCanal(" Red ");
    private FrameCanal green = new FrameCanal(" Green ");
    private FrameCanal blue = new FrameCanal(" Blue ");
    private FrameCanal alpha = new FrameCanal(" Alpha (Transparencia) ");
    private Gtk.Image image = new Gtk.Image();

    public Canales(Gtk.Window top){

        this.set_title("Canales");
        this.window_position = Gtk.WindowPosition.NONE;
        this.set_resizable(false);
        this.set("border_width", 2);
        this.set_transient_for(top);
        this.set_default_size(500, 100);

        Gtk.Box box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
        this.image.set_size_request(300, 20);
        box.pack_start(this.image, false, false, 0);
        box.pack_start(this.red, false, false, 0);
        box.pack_start(this.green, false, false, 0);
        box.pack_start(this.blue, false, false, 0);
        box.pack_start(this.alpha, false, false, 0);

        Gtk.Frame frame = new Gtk.Frame("");
        //frame.set_border_width(4);
        Gtk.TextView view = new Gtk.TextView();
        view.set_wrap_mode (Gtk.WrapMode.WORD);
        view.set_property("editable", false);
        string text = "En cada pixel, pinta el porcentaje elegido del valor que posee en ese canal.\n\n";
        text += "Por ejemplo:\n\tEn un pixel que tiene 200 en el canal rojo, cuando seleccionas 10 por ciento en ese canal, pasará a tener 20.\n\n";
        text += "Esta operación se repite en cada pixel de la imagen.";
        view.buffer.text = text;
        view.set_border_width(4);
        frame.add(view);
        box.pack_start(frame, false, false, 0);

        this.add(box);
        this.realize.connect(this.realized);
        this.show_all();

        this.red.user_set_value.connect(this.update_image);
        this.green.user_set_value.connect(this.update_image);
        this.blue.user_set_value.connect(this.update_image);
        this.alpha.user_set_value.connect(this.update_image);
        }

    private void realized(){
        Gtk.Allocation rect;
        this.get_allocation(out rect);
        Gdk.Screen screen = Gdk.Screen.get_default();
        int w = screen.get_width();
        int h = screen.get_height();
        this.move(w - rect.width, 0);
        }

    private void update_image(double valor){
        if (this.processor != null){
            if (this.processor.get_file_path() != ""){
                double r = this.red.escala.ajuste.get_value() * 100.0 / 255.0;
                double g = this.green.escala.ajuste.get_value() * 100.0 / 255.0;
                double b = this.blue.escala.ajuste.get_value() * 100.0 / 255.0;
                double a = this.alpha.escala.ajuste.get_value() * 100.0 / 255.0;
                this.canal_changed(r, g, b, a);

                uint16 rr = (uint16)(65535 * r / 100);
                uint16 gg = (uint16)(65535 * g / 100);
                uint16 bb = (uint16)(65535 * b / 100);

                Gdk.Color color = Gdk.Color();
                color.pixel = 8;
                color.red = rr;
                color.green = gg;
                color.blue = bb;
                this.image.modify_bg(Gtk.StateType.NORMAL, color);
                }
            }
        }

    public void set_processor(ImgProcessor processor){
        this.processor = null;
        this.red.set_progress(255);
        this.green.set_progress(255);
        this.blue.set_progress(255);
        this.alpha.set_progress(255);
        this.processor = processor;
        Gdk.Color color = Gdk.Color();
        color.pixel = 8;
        color.red = 65535;
        color.green = 65535;
        color.blue = 65535;
        this.image.modify_bg(Gtk.StateType.NORMAL, color);
        }
    }


internal class FrameCanal : Gtk.Frame{

    public signal void user_set_value(double valor);

    public SlicerBalance escala = new SlicerBalance();
    private Gtk.Label label = new Gtk.Label("");

    public FrameCanal(string titulo){

        this.set("label_widget", this.label);
        this.label.set_text(titulo);
        this.set("label_xalign", 0.5);
        this.set("label_yalign", 0.5);
        this.set_border_width(4);

        this.add(this.escala);
        this.show_all();

        this.escala.user_set_value.connect(this.__user_set_value);
        }

    public void __user_set_value(double valor){
        string str1 = this.label.get_text();
        int p = (int)(valor * 100.0 / 255.0);
        string str2 = p.to_string();
        string str3 = "%";
        string text = @"$str1: $str2$str3";
        this.set_label(text);
        this.user_set_value(valor);
        }

    public void set_progress(double valor){
        this.escala.set_progress(valor);
        }
    }


internal class SlicerBalance : Gtk.EventBox{

    public signal void user_set_value(double valor);

    private Gtk.Scale escala;
    public Gtk.Adjustment ajuste = new Gtk.Adjustment(
        0.0, 0.0, 256.0, 0.1, 1.0, 1.0);

    public SlicerBalance(){

        this.set("border_width", 4);
        this.escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, this.ajuste);
        this.escala.set_digits(0);
        this.escala.set_draw_value(false);

        this.add(this.escala);
        this.show_all();

        this.escala.value_changed.connect (() => {
            this.user_set_value(this.ajuste.get_value());
        });
    }

    public void set_progress(double valor){
        this.ajuste.set_value(valor);
        this.escala.queue_draw();
        }
    }
