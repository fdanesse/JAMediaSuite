

internal class ImgProcessor : GLib.Object{

    public signal void has_change(bool changed);

    private string file_path = "";
    private Gdk.Pixbuf pixbuf = null;       //Lo que se va a guardar
    private Gdk.Pixbuf pixbuf_view = null;  //Lo que se muestra
    private double scale_factor = 1.0;
    private unowned uint8[] array;
    private bool changed = false;

    internal ImgProcessor(){

        }

    private void emit_change(bool changed){
        this.has_change(changed);
        }

    public void close_file(){
        this.file_path = "";
        this.array = null;
        this.pixbuf = null;
        this.pixbuf_view = null;
        this.scale_factor = 1.0;
        this.changed = false;
        this.emit_change(this.changed);
        //self.__file_info = {}
        }

    public string open(string filepath){
        this.file_path = filepath;
        this.pixbuf = new Gdk.Pixbuf.from_file(filepath);
        this.pixbuf_view = new Gdk.Pixbuf.from_file(filepath);
        this.array = this.pixbuf.get_pixels();

        stdout.printf("Abriendo Archivo: %s\n", filepath);
        stdout.printf("\tResolución: %i %i Pixeles Totales: %i\n", this.pixbuf.get_width(), this.pixbuf.get_height(), this.pixbuf.get_rowstride() * this.pixbuf.get_height());
        stdout.printf("\tElementos por fila: %i Canales: %i\n", this.pixbuf.get_rowstride(), this.pixbuf.get_n_channels());
        //stdout.printf("this.array.length: %u\n", this.array.length);

        return "";  // Retorna info del archivo
        }

    public Gdk.Pixbuf rotate_left(){
        //Afecta lo que se va a guardar
        Gdk.Pixbuf pixbuf = this.pixbuf.copy();
        this.pixbuf = pixbuf.rotate_simple(Gdk.PixbufRotation.COUNTERCLOCKWISE);
        this.pixbuf_view = this.pixbuf.copy();
        this.changed = true;
        this.emit_change(this.changed);
        if (scale_factor != 1.0){
            return this.scale();
            }
        else{
            return this.pixbuf_view;
            }
        }

    public Gdk.Pixbuf rotate_right(){
        //Afecta lo que se va a guardar
        Gdk.Pixbuf pixbuf = this.pixbuf.copy();
        this.pixbuf = pixbuf.rotate_simple(Gdk.PixbufRotation.CLOCKWISE);
        this.pixbuf_view = this.pixbuf.copy();
        this.changed = true;
        this.emit_change(this.changed);
        if (this.scale_factor != 1.0){
            return this.scale();
            }
        else{
            return this.pixbuf_view;
            }
        }

    public Gdk.Pixbuf get_pixbuf_zoom_in(){
        //zoom sobre lo que se ve
        this.scale_factor = this.scale_factor * 1.25;
        return this.scale();
        }

    public Gdk.Pixbuf get_pixbuf_zoom_out(){
        //zoom sobre lo que se ve
        this.scale_factor = this.scale_factor * 0.8;
        return this.scale();
        }

    public Gdk.Pixbuf get_pixbuf_scale(int w, int h){
    //zoom sobre lo que se ve
        double x_ratio = (double) w / (double) this.pixbuf.get_width();
        double y_ratio = (double) h / (double) this.pixbuf.get_height();
        if (y_ratio < x_ratio){
            this.scale_factor = y_ratio;
            }
        else{
            this.scale_factor = x_ratio;
            }
        return this.scale();
        }

    private Gdk.Pixbuf scale(){
        //zoom sobre lo que se ve
        //FIXME: Gdk.InterpType.HYPER maxima calidad, bajo rendimiento
        Gdk.Pixbuf pixbuf = this.pixbuf.copy();
        int new_width = (int)(pixbuf.get_width() * this.scale_factor);
        int new_height = (int)(pixbuf.get_height() * this.scale_factor);
        this.pixbuf_view = pixbuf.scale_simple(new_width,
            new_height, Gdk.InterpType.HYPER);
        return this.pixbuf_view;
        }

    public Gdk.Pixbuf get_pixbuf(){
        //Lo que se va a guardar y a tamaño original
        this.scale_factor = 1.0;
        this.pixbuf_view = this.pixbuf.copy();
        return this.pixbuf_view;
        }

    /*
    public Gdk.Pixbuf get_pixbuf_channles(Gtk.Widget widget, string mode_view, string channels){
        if (mode_view == "REAL" && "Original" in channels){
            //return this.pixbuf;
            pixbuf = this.scale_full(widget, this.pixbuf);
            return pixbuf;
            }
        else{
            return this.pixbuf;
            }
        }
    */
    /*
    private Gdk.Pixbuf scale_full(Gtk.Widget widget, Gdk.Pixbuf pixbuf){
        //rect = widget.get_allocation()
        //src_width, src_height = pixbuf.get_width(), pixbuf.get_height()
        //scale = min(float(rect.width) / src_width,
        //    float(rect.height) / src_height)
        //new_width = int(scale * src_width)
        //new_height = int(scale * src_height)
        //pixbuf = pixbuf.scale_simple(new_width,
        //    new_height, gtk.gdk.INTERP_BILINEAR)
        return pixbuf;
        }
    */
    public string get_dir_path(){
        if (this.file_path != ""){
            return GLib.Path.get_dirname(this.file_path);
            }
        else{
            return GLib.Environment.get_variable("HOME");
            }
        }
    }
