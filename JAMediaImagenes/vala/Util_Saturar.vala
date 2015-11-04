

internal class Saturar : Gtk.Window{

    public signal void changed();

    private ImgProcessor processor = null;
    private FrameSaturar saturar = new FrameSaturar(" Saturación: ");

    public Saturar(Gtk.Window top){

        this.set_title("Canales");
        this.window_position = Gtk.WindowPosition.NONE;
        this.set_resizable(false);
        this.set("border_width", 2);
        this.set_transient_for(top);
        this.set_default_size(500, -1);

        this.add(this.saturar);
        this.realize.connect(this.realized);
        this.show_all();

        this.saturar.user_set_value.connect(this.update_image);
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
        this.processor.apply_saturacion((float)valor, false);
        this.changed();
        }

    public void set_processor(ImgProcessor processor){
        this.processor = processor;
        }
    }


internal class FrameSaturar : Gtk.Frame{

    public signal void user_set_value(double valor);

    public SliceSaturar escala = new SliceSaturar();
    private Gtk.Label label = new Gtk.Label("");

    public FrameSaturar(string titulo){

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
        string str2 = valor.to_string();
        string text = @"$str1: $str2";
        this.set_label(text);
        this.user_set_value(valor);
        }
    }


internal class SliceSaturar : Gtk.EventBox{

    public signal void user_set_value(double valor);

    private Gtk.Scale escala;
    public Gtk.Adjustment ajuste = new Gtk.Adjustment(
        1.0, 0.0, 3.1, 0.1, 0.1, 0.1);

    public SliceSaturar(){

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
    }
