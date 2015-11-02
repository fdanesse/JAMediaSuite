

internal class Canales : Gtk.Window{

    public signal void change_channel(string channel);

    private ImgProcessor processor = null;
    private Gtk.Image image = new Gtk.Image();
    private Gtk.Grid grid = new Gtk.Grid();
    private FrameCanal red = new FrameCanal(" Red ");
    private FrameCanal green = new FrameCanal(" Green ");
    private FrameCanal blue = new FrameCanal(" Blue ");
    private FrameCanal alpha = new FrameCanal(" Alpha ");

    public Canales(Gtk.Window top){

        this.set_title("Canales");
        this.window_position = Gtk.WindowPosition.CENTER;
        this.set_resizable(false);
        this.set("border_width", 2);
        this.set_transient_for(top);

        this.image.set_size_request(320, 240);

        Gtk.Box box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
        box.pack_start(this.image, false, false, 0);
        box.pack_start(this.grid, false, false, 0);

        this.grid.set_property("column_homogeneous", true);
        this.grid.set_property("row_homogeneous", true);

        this.grid.attach(this.red, 0, 0, 1, 1);
        this.grid.attach(this.green, 0, 1, 1, 1);
        this.grid.attach(this.blue, 0, 2, 1, 1);
        this.grid.attach(this.alpha, 0, 3, 1, 1);

        this.add(box);
        this.show_all();

        this.red.user_set_value.connect(this.update_image);
        this.green.user_set_value.connect(this.update_image);
        this.blue.user_set_value.connect(this.update_image);
        this.alpha.user_set_value.connect(this.update_image);
        }

    private void update_image(double valor){
        if (this.processor != null){
            if (this.processor.get_file_path() != ""){
                double r = this.red.escala.ajuste.get_value() * 100.0 / 255.0;
                double g = this.green.escala.ajuste.get_value() * 100.0 / 255.0;
                double b = this.blue.escala.ajuste.get_value() * 100.0 / 255.0;
                double a = this.alpha.escala.ajuste.get_value() * 100.0 / 255.0;
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(320, 240);
                Gdk.Pixbuf newpixbuf = this.processor.pixbuf_to_levels(pixbuf, r, g, b, a);
                this.image.set_from_pixbuf(newpixbuf);
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
        if (this.processor.get_file_path() != ""){
            Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(320, 240);
            this.image.set_from_pixbuf(pixbuf);
            }
        else{
            this.image.clear();
            }
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

        Gtk.EventBox event = new Gtk.EventBox();
        event.set_border_width(4);
        event.add(this.escala);
        this.add(event);

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
