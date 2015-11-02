

internal class Canales : Gtk.Window{

    public signal void change_channel(string channel);

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
        }

    public void set_processor(ImgProcessor processor){
        this.red.set_progress(100);
        this.green.set_progress(100);
        this.blue.set_progress(100);
        this.alpha.set_progress(100);
        //this.red.set_processor(processor);
        //this.green.set_processor(processor);
        //this.blue.set_processor(processor);
        //this.alpha.set_processor(processor);
        }
    }


internal class FrameCanal : Gtk.Frame{

    //public signal void user_set_value(double valor);

    private SlicerBalance escala = new SlicerBalance();
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
        if (valor > 99.4){
            valor = 100.0;
            }
        int v = (int) valor;
        string str1 = this.label.get_text();
        string str2 = v.to_string();
        string str3 = "%";
        string text = @"$str1: $str2$str3";
        this.set_label(text);
        //this.user_set_value(valor);
    }

    public void set_progress(double valor){
        this.escala.set_progress(valor);
        }
    }


internal class SlicerBalance : Gtk.EventBox{

    public signal void user_set_value(double valor);

    private Gtk.Scale escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL,
        new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    public Gtk.Adjustment ajuste = new Gtk.Adjustment(
        0.0, 0.0, 101.0, 0.1, 1.0, 1.0);

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
