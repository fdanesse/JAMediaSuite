

internal class Grises : Gtk.Window{

    public signal void change_channel(string channel);

    private Gtk.Grid grid = new Gtk.Grid();
    private FrameGris lightness = new FrameGris(" Lightness: ");
    private FrameGris luminosity = new FrameGris(" Luminosity: ");
    private FrameGris average = new FrameGris(" Average: ");
    private FrameGris percentual = new FrameGris(" Percentual: ");

    public Grises(Gtk.Window top){

        this.set_title("Grises");
        this.window_position = Gtk.WindowPosition.CENTER;
        this.set_resizable(false);
        this.set("border_width", 2);
        this.set_transient_for(top);
        this.grid.set_property("column_homogeneous", true);
        this.grid.set_property("row_homogeneous", true);
        this.grid.attach(this.lightness, 0, 0, 1, 1);
        this.grid.attach(this.luminosity, 1, 0, 1, 1);
        this.grid.attach(this.average, 2, 0, 1, 1);
        this.grid.attach(this.percentual, 3, 0, 1, 1);
        this.add(this.grid);
        this.show_all();

        this.lightness.toggled.connect(this.do_toggled);
        this.luminosity.toggled.connect(this.do_toggled);
        this.average.toggled.connect(this.do_toggled);
        this.percentual.toggled.connect(this.do_toggled);
        }

    public void set_processor(ImgProcessor processor){
        this.lightness.set_processor(processor);
        this.luminosity.set_processor(processor);
        this.average.set_processor(processor);
        this.percentual.set_processor(processor);
        }

    private void do_toggled(string label, bool valor){
        Gee.ArrayList<FrameGris> items = new Gee.ArrayList<FrameGris>();
        items.add(this.lightness);
        items.add(this.luminosity);
        items.add(this.average);
        items.add(this.percentual);
        if (valor){
            foreach (FrameGris frame in items){
                if (label != frame.get_label()){
                    frame.toggle(false);
                    }
                }
            this.change_channel(label);
            }
        else{
            bool active = false;
            foreach (FrameGris frame in items){
                if (frame.get_active()){
                    active = frame.get_active();
                    break;
                    }
                }
            if (active == false){
                this.change_channel("Original");
                }
            }
        }
    }


internal class FrameGris : Gtk.Frame{

    public signal void toggled(string label, bool valor);

    private Gtk.ToggleButton button = new Gtk.ToggleButton();
    private Gtk.Image image = new Gtk.Image();

    public FrameGris(string text){
        this.set_border_width(4);
        this.set_label(text);
        this.image.set_size_request(100, 75);
        this.button.set_image(this.image);
        this.add(this.button);
        this.show_all();

        this.button.toggled.connect((source) => {
            this.do_toggled();
         });
        }

    public void set_processor(ImgProcessor processor){
        this.button.set_active(false);
        if (processor.get_file_path() != ""){
            Gdk.Pixbuf pixbuf = processor.get_pixbuf_scale(100, 100);
            if ("Average" in this.get_label()){
                Gdk.Pixbuf newpixbuf = processor.pixbuf_to_channel(pixbuf, "average");
                this.image.set_from_pixbuf(newpixbuf);
                }
            else if ("Percentual" in this.get_label()){
                Gdk.Pixbuf newpixbuf = processor.pixbuf_to_channel(pixbuf, "percentual");
                this.image.set_from_pixbuf(newpixbuf);
                }
            else if ("Luminosity" in this.get_label()){
                Gdk.Pixbuf newpixbuf = processor.pixbuf_to_channel(pixbuf, "luminosity");
                this.image.set_from_pixbuf(newpixbuf);
                }
            else if ("Lightness" in this.get_label()){
                Gdk.Pixbuf newpixbuf = processor.pixbuf_to_channel(pixbuf, "lightness");
                this.image.set_from_pixbuf(newpixbuf);
                }
            else{
                this.image.set_from_pixbuf(pixbuf);
                }
            }
        else{
            this.image.clear();
            }
        }

    public bool get_active(){
        return this.button.get_active();
        }

    public void toggle(bool valor){
        this.button.set_active(valor);
        }

    private void do_toggled(){
        this.toggled(this.get_label(), this.button.get_active());
        }
    }
