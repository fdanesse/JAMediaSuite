

internal class ImgProcessor : GLib.Object{

    public signal void has_change(bool changed);

    private string file_path = "";
    private Gdk.Pixbuf pixbuf = null;       //Lo que se va a guardar
    private Gdk.Pixbuf pixbuf_view = null;  //Lo que se muestra
    private double scale_factor = 1.0;
    //private unowned uint8[] array;
    private bool changed = false;

    internal ImgProcessor(){
        }

    private void emit_change(bool changed){
        this.has_change(changed);
        }

    public void close_file(){
        this.file_path = "";
        //this.array = null;
        this.pixbuf = null;
        this.pixbuf_view = null;
        this.scale_factor = 1.0;
        this.changed = false;
        this.emit_change(this.changed);
        //self.__file_info = {}
        }

    public string open(string filepath){
        this.file_path = filepath;
        pixbuf = new Gdk.Pixbuf.from_file(filepath);
        pixbuf_view = new Gdk.Pixbuf.from_file(filepath);
        //Siempre Agregar canal alpha
        if (this.pixbuf.get_has_alpha()){
            this.pixbuf = pixbuf;
            this.pixbuf_view = pixbuf_view;
            }
        else{
            this.pixbuf = pixbuf.add_alpha (false, 0, 0, 0);
            this.pixbuf_view = pixbuf_view.add_alpha (false, 0, 0, 0);
            this.changed = true;
            this.emit_change(this.changed);
            }
        //this.array = this.pixbuf.get_pixels();
        GLib.File file = GLib.File.new_for_path(filepath);
        var file_info = file.query_info ("*", GLib.FileQueryInfoFlags.NONE);
        int64 size = file_info.get_size();
        string tipo = file_info.get_content_type();
        int w = this.pixbuf.get_width();
        int h = this.pixbuf.get_height();
        int rowstride = this.pixbuf.get_rowstride();
        int channels = this.pixbuf.get_n_channels();
        /*
        GLib.stdout.printf("Abriendo Archivo: %s\n", filepath);
        GLib.stdout.printf("\tResolución: %i %i Pixeles Totales: %i\n", w, h, rowstride * h);
        GLib.stdout.printf("\tElementos por fila: %i Canales: %i\n", rowstride, channels);
        //GLib.stdout.printf("this.array.length: %u\n", this.array.length);
        GLib.stdout.flush();
        */
        string info = "Img: ";
        info += filepath;
        info += " ";
        info += tipo;
        info += " ";
        info += w.to_string();
        info += " x ";
        info += h.to_string();
        info += " pixeles: ";
        info += (w * h).to_string();
        info += " Canales: ";
        info += channels.to_string();
        info += " bytes ";
        info += size.to_string();
        return info;
        }

    public Gdk.Pixbuf rotate_left(){
        //Afecta lo que se va a guardar
        Gdk.Pixbuf pixbuf = this.pixbuf.copy();
        this.pixbuf = pixbuf.rotate_simple(Gdk.PixbufRotation.COUNTERCLOCKWISE);
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
        Gdk.Pixbuf pixbuf = this.pixbuf.copy();
        double x_ratio = (double) w / (double) pixbuf.get_width();
        double y_ratio = (double) h / (double) pixbuf.get_height();
        if (y_ratio < x_ratio){
            this.scale_factor = y_ratio;
            }
        else{
            this.scale_factor = x_ratio;
            }
        return this.scale();
        }

    private Gdk.Pixbuf scale(){
        Gdk.Pixbuf pixbuf = this.pixbuf.copy();
        //FIXME: Gdk.InterpType.HYPER maxima calidad, bajo rendimiento
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

    private uint8 average(uint8[] list){
        uint8 mean;
        int sum = 0;
        foreach(uint8 number in list){
            sum += (int)number;
            }
        mean = (uint8)(sum / list.length);
        return mean;
        }

    public Gdk.Pixbuf pixbuf_to_average(Gdk.Pixbuf pixbuf){
        //Convierte un pixbuf a escala de grises usando Average.
        int width = pixbuf.get_width();
        int height = pixbuf.get_height();
        int rowstride = pixbuf.get_rowstride(); //Elementos por fila en imagen de 20 * 10 con [rgbh] = 80 (20*4) 20 elementos de 4 componentes
        int channels = pixbuf.get_n_channels();
        unowned uint8[] array = pixbuf.get_pixels ();
        for (int row = 0; row < height; row++){
            for (int elem = rowstride * row; elem < rowstride * row + rowstride; elem += channels){
                    uint8 prom = average(array[elem:elem + 3]);
                    array[elem] = prom;
                    array[elem + 1] = prom;
                    array[elem + 2] = prom;
                }
            }
        return pixbuf;
        }

    public void apply_average(){
        //Convierte el pixbuf principal a escala de grises usando Average.
        int width = this.pixbuf.get_width();
        int height = this.pixbuf.get_height();
        int rowstride = this.pixbuf.get_rowstride(); //Elementos por fila en imagen de 20 * 10 con [rgbh] = 80 (20*4) 20 elementos de 4 componentes
        int channels = this.pixbuf.get_n_channels();
        unowned uint8[] array = this.pixbuf.get_pixels ();
        for (int row = 0; row < height; row++){
            for (int elem = rowstride * row; elem < rowstride * row + rowstride; elem += channels){
                    uint8 prom = average(array[elem:elem + 3]);
                    array[elem] = prom;
                    array[elem + 1] = prom;
                    array[elem + 2] = prom;
                }
            }
        this.changed = true;
        this.emit_change(this.changed);
        }

    public string get_dir_path(){
        if (this.file_path != ""){
            return GLib.Path.get_dirname(this.file_path);
            }
        else{
            return GLib.Environment.get_variable("HOME");
            }
        }

    public string get_file_path(){
        return this.file_path;
        }

    public void save_file(string filepath) throws GLib.Error{
        //FIXME: Asegurar extensión para el archivo
        this.pixbuf.save(filepath, "png", null);
        }

    public bool get_changed(){
        return this.changed;
        }
    }
