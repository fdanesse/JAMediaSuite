

internal class Escala : Gtk.Window{

    public signal void changed(GLib.List<int> res);

    private FrameEscala escala = null;

    public Escala(Gtk.Window top, GLib.List<int> res){

        this.set_title("Escala");
        this.window_position = Gtk.WindowPosition.NONE;
        this.set_resizable(false);
        this.set("border_width", 2);
        this.set_transient_for(top);

        this.escala = new FrameEscala(" Tamaño de la Imagen ", res);
        this.add(this.escala);

        this.realize.connect(this.realized);
        this.show_all();

        this.escala.user_set_value.connect((source, res) => {
            this.changed(res);
            });
        }

    private void realized(){
        Gtk.Allocation rect;
        this.get_allocation(out rect);
        Gdk.Screen screen = Gdk.Screen.get_default();
        int w = screen.get_width();
        int h = screen.get_height();
        this.move(w - rect.width, 0);
        }
    }


internal class FrameEscala : Gtk.Frame{

    public signal void user_set_value(GLib.List<int> res);

    private double escale_factor = 0.0;
    private bool bloquear = false;
    private Gtk.SpinButton ancho = new Gtk.SpinButton.with_range(1.0, 50000.0, 1.0);
    private Gtk.SpinButton alto = new Gtk.SpinButton.with_range(1.0, 50000.0, 1.0);
    private Gtk.CheckButton button = new Gtk.CheckButton();

    public FrameEscala(string titulo, GLib.List<int> _res){

        this.set_label(titulo);
        this.set_border_width(4);

        this.ancho.set_value((double)_res.nth_data(0));
        this.alto.set_value((double)_res.nth_data(1));
        this.escale_factor = (double)_res.nth_data(0) / (double)_res.nth_data(1);

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

        this.button.set_label("Mantener Proporción");
        this.button.set_active(true);
        grid.attach(this.button, 1, 2, 1, 2);

        this.add(grid);
        this.show_all();

        this.ancho.value_changed.connect (() => {
            if (this.bloquear == false){
                this.bloquear = true;
                unowned int w = this.ancho.get_value_as_int();
                unowned int h = this.alto.get_value_as_int();
                if (this.button.get_active()){
                    h = (int)(this.ancho.get_value() / this.escale_factor);
                    this.alto.set_value((double)h);
                    }
                GLib.List<int> res = new GLib.List<int>();
                res.append(w);
                res.append(h);
                this.user_set_value(res);
                this.bloquear = false;
                }
            });

        this.alto.value_changed.connect (() => {
            if (this.bloquear == false){
                this.bloquear = true;
                unowned int w = this.ancho.get_value_as_int();
                unowned int h = this.alto.get_value_as_int();
                if (this.button.get_active()){
                    w = (int)(this.alto.get_value() * this.escale_factor);
                    this.ancho.set_value((double)w);
                    }
                GLib.List<int> res = new GLib.List<int>();
                res.append(w);
                res.append(h);
                this.user_set_value(res);
                this.bloquear = false;
                }
            });

        this.button.toggled.connect (() => {
            if (this.button.get_active()) {
                unowned double h = this.alto.get_value();
                h = this.ancho.get_value() / this.escale_factor;
                if (this.alto.get_value() != h){
                    this.alto.set_value(h);
                    }
                }
            });

        }
    }
