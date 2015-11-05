

internal class Escala : Gtk.Window{

    //public signal void canal_changed(double r, double g, double b, double h);

    //private ImgProcessor processor = null;
    private FrameEscala escala = new FrameEscala(" Tamaño de la Imagen ");

    public Escala(Gtk.Window top){

        this.set_title("Escala");
        this.window_position = Gtk.WindowPosition.NONE;
        this.set_resizable(false);
        this.set("border_width", 2);
        this.set_transient_for(top);
        //this.set_size_request(500, 100);

        this.add(this.escala);
        this.realize.connect(this.realized);
        this.show_all();

        //this.escala.user_set_value.connect(this.update_image);
        }

    private void realized(){
        Gtk.Allocation rect;
        this.get_allocation(out rect);
        Gdk.Screen screen = Gdk.Screen.get_default();
        int w = screen.get_width();
        int h = screen.get_height();
        this.move(w - rect.width, 0);
        }

    /*
    private void update_image(double valor){
        if (this.processor != null){
            if (this.processor.get_file_path() != ""){
                double r = this.escala.escala.ajuste.get_value() * 100.0 / 255.0;
                double g = this.green.escala.ajuste.get_value() * 100.0 / 255.0;
                double b = this.blue.escala.ajuste.get_value() * 100.0 / 255.0;
                double a = this.alpha.escala.ajuste.get_value() * 100.0 / 255.0;
                this.canal_changed(r, g, b, a);

                uint16 rr = (uint16)(65535 * r / 100);
                uint16 gg = (uint16)(65535 * g / 100);
                uint16 bb = (uint16)(65535 * b / 100);

                Gdk.Color color = Gdk.Color();
                color.pixel = 8;
                color.escala = rr;
                color.green = gg;
                color.blue = bb;
                this.image.modify_bg(Gtk.StateType.NORMAL, color);
                }
            }
        }
    */

    public void set_processor(ImgProcessor processor){
        /*
        this.processor = processor;
        Gdk.Color color = Gdk.Color();
        color.pixel = 8;
        color.escala = 65535;
        color.green = 65535;
        color.blue = 65535;
        this.image.modify_bg(Gtk.StateType.NORMAL, color);
        */
        }
    }


internal class FrameEscala : Gtk.Frame{

    //public signal void user_set_value(double valor);

    private Gtk.SpinButton ancho = new Gtk.SpinButton.with_range(1.0, 50000.0, 1.0);
    private Gtk.SpinButton alto = new Gtk.SpinButton.with_range(1.0, 50000.0, 1.0);

    public FrameEscala(string titulo){

        this.set_label(titulo);
        this.set_border_width(4);

        Gtk.Grid grid = new Gtk.Grid();
        grid.set_property("column_homogeneous", true);
        grid.set_property("row_homogeneous", true);
        grid.set_border_width(4);

        Gtk.Frame frame1 = new Gtk.Frame(" Ancho: ");
        frame1.set_border_width(4);
        Gtk.EventBox event1 = new Gtk.EventBox();
        event1.set_border_width(4);
        event1.add(this.ancho);
        frame1.add(event1);
        grid.attach(frame1, 0, 0, 1, 3);

        Gtk.Frame frame2 = new Gtk.Frame(" Alto: ");
        frame2.set_border_width(4);
        Gtk.EventBox event2 = new Gtk.EventBox();
        event2.set_border_width(4);
        event2.add(this.alto);
        frame2.add(event2);
        grid.attach(frame2, 0, 3, 1, 3);

        Gtk.CheckButton button = new Gtk.CheckButton();
        button.set_label("Mantener Proporción");
        grid.attach(button, 1, 2, 1, 2);

        this.add(grid);
        this.show_all();

        //this.escala.user_set_value.connect(this.__user_set_value);
        }

    /*
    public void __user_set_value(double valor){
        string str1 = this.label.get_text();
        int p = (int)(valor * 100.0 / 255.0);
        string str2 = p.to_string();
        string str3 = "%";
        string text = @"$str1: $str2$str3";
        this.set_label(text);
        //this.user_set_value(valor);
        }
    */
    }
