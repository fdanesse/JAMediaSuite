
// https://wiki.gnome.org/Projects/Vala/StatusIcon
// https://github.com/polymeris/shotwell/blob/master/thumbnailer/shotwell-video-thumbnailer.vala
// https://developer.gnome.org/gdk-pixbuf/stable/gdk-pixbuf-The-GdkPixbuf-Structure.html#image-data
// http://stackoverflow.com/questions/2744118/how-do-i-remove-or-apply-transparency-on-a-gdk-pixbuf
// https://github.com/GNOME/shotwell/blob/master/src/photos/PngSupport.vala
// https://github.com/GNOME/model-examples/blob/master/examples/filesystem/view.vala

/*
uint8 r = array[elem];
uint8 g = array[elem + 1];
uint8 b = array[elem + 2];
//Deteccion de piel = r > 95 and g > 40 and b > 20 and max([r, g, b]) - min([r, g, b]) > 15 and (r - g) > 15 and r > g and r > b
uint8 ma = uint8.max(r, g);
ma = uint8.max(ma, b);
uint8 mi = uint8.min(r, g);
mi = uint8.min(mi, b);
if (r > 95 && g > 40 && b > 20 && ma - mi > 15 && (r - g) > 15 && r > b){
    }
else{
    array[elem + 3] = 0;
    }
*/

/*
public string open(string filepath)
    puede modificar el original si no tiene alpha

public Gdk.Pixbuf rotate_left()
    modifica el original

public Gdk.Pixbuf rotate_right()
    modifica el original

public void apply_average()
    modifica el original
*/


internal class ImgProcessor : GLib.Object{

    public signal void has_change(bool changed);

    private string file_path = "";
    private Gdk.Pixbuf pixbuf = null;
    private double scale_factor = 1.0;
    private bool changed = false;

    internal ImgProcessor(){
        }

    private void emit_change(bool changed){
        this.has_change(changed);
        }

    public void close_file(){
        this.file_path = "";
        this.pixbuf = null;
        this.scale_factor = 1.0;
        this.changed = false;
        this.emit_change(this.changed);
        }

    public string open(string filepath){
        this.file_path = filepath;
        Gdk.Pixbuf pixbuf = new Gdk.Pixbuf.from_file(filepath);
        //Siempre Agregar canal alpha
        if (pixbuf.get_has_alpha()){
            this.pixbuf = pixbuf;
            }
        else{
            this.pixbuf = pixbuf.add_alpha (false, 0, 0, 0);
            this.changed = true;
            this.emit_change(this.changed);
            }
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
        this.pixbuf = this.pixbuf.rotate_simple(Gdk.PixbufRotation.COUNTERCLOCKWISE);
        this.changed = true;
        this.emit_change(this.changed);
        if (this.scale_factor != 1.0){
            return this.scale();
            }
        else{
            return this.pixbuf;
            }
        }

    public Gdk.Pixbuf rotate_right(){
        //Afecta lo que se va a guardar
        this.pixbuf = this.pixbuf.rotate_simple(Gdk.PixbufRotation.CLOCKWISE);
        this.changed = true;
        this.emit_change(this.changed);
        if (this.scale_factor != 1.0){
            return this.scale();
            }
        else{
            return this.pixbuf;
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
        //Gdk.Pixbuf pixbuf = this.pixbuf.copy();
        //FIXME: Gdk.InterpType.HYPER maxima calidad, bajo rendimiento
        int new_width = (int)(pixbuf.get_width() * this.scale_factor);
        int new_height = (int)(pixbuf.get_height() * this.scale_factor);
        Gdk.Pixbuf preview = this.pixbuf.scale_simple(new_width,
            new_height, Gdk.InterpType.HYPER);
        return preview;
        }

    public Gdk.Pixbuf get_pixbuf(){
        //Lo que se va a guardar y a tamaño original
        this.scale_factor = 1.0;
        return this.pixbuf;
        }

    private uint8 average(uint8[] list){
        uint8 ret;
        int sum = 0;
        foreach(uint8 number in list){
            sum += (int)number;
            }
        ret = (uint8)(sum / list.length);
        return ret;
        }

    private uint8 percentual(uint8[] list){
        double a = (double)list[0];
        double b = (double)list[1];
        double c = (double)list[2];
        uint8 ret = (uint8)(a * 0.3 + b * 0.59 + c * 0.11);
        return ret;
        }

    private uint8 luminosity(uint8[] list){
        double a = (double)list[0];
        double b = (double)list[1];
        double c = (double)list[2];
        uint8 ret = (uint8)(0.21 * a + 0.72 * b + 0.07 * c);
        return ret;
        }

    private uint8 lightness(uint8[] list){
        uint8 ma = uint8.max(list[0], list[1]);
        ma = uint8.max(ma, list[2]);
        uint8 mi = uint8.min(list[0], list[1]);
        mi = uint8.min(mi, list[2]);
        uint8 ret = (uint8)(1.0 / 2.0 * ((double)ma + (double)mi));
        return ret;
        }

    public Gdk.Pixbuf pixbuf_to_canales(Gdk.Pixbuf pixbuf, double r, double g, double b, double a){
        //Modifica en porcentajes los niveles de cada canal.
        int width = pixbuf.get_width();
        int height = pixbuf.get_height();
        int rowstride = pixbuf.get_rowstride();
        int channels = pixbuf.get_n_channels();
        unowned uint8[] array = pixbuf.get_pixels();
        for (int row = 0; row < height; row++){
            for (int elem = rowstride * row; elem < rowstride * row + rowstride; elem += channels){
                array[elem] = (uint8)((double)array[elem] * r / 100.0);
                array[elem + 1] = (uint8)((double)array[elem + 1] * g / 100.0);
                array[elem + 2] = (uint8)((double)array[elem + 2] * b / 100.0);
                array[elem + 3] = (uint8)((double)array[elem + 3] * a / 100.0);
                }
            }
        return pixbuf;
        }

    public Gdk.Pixbuf pixbuf_to_gris(Gdk.Pixbuf pixbuf, string channel){
        //Convierte un pixbuf a escala de grises
        int width = pixbuf.get_width();
        int height = pixbuf.get_height();
        int rowstride = pixbuf.get_rowstride();
        int channels = pixbuf.get_n_channels();
        unowned uint8[] array = pixbuf.get_pixels();
        for (int row = 0; row < height; row++){
            for (int elem = rowstride * row; elem < rowstride * row + rowstride; elem += channels){
                uint8 ret = 0;
                if (channel == "average"){
                    ret = average(array[elem:elem + 3]);
                    }
                else if (channel == "percentual"){
                    ret = percentual(array[elem:elem + 3]);
                    }
                else if (channel == "luminosity"){
                    ret = luminosity(array[elem:elem + 3]);
                    }
                else if (channel == "lightness"){
                    ret = lightness(array[elem:elem + 3]);
                    }
                array[elem] = ret;
                array[elem + 1] = ret;
                array[elem + 2] = ret;
                }
            }
        return pixbuf;
        }

    public void apply_canales(double r, double g, double b, double a){
        string info = this.open(this.get_file_path()); //Es necesario eliminar cambios previos por eso reabrimos.
        Gdk.Pixbuf pixbuf = this.pixbuf_to_canales(this.pixbuf, r, g, b, a);
        this.changed = true;
        this.emit_change(this.changed);
        }

    public void apply_gris(string channel){
        string info = this.open(this.get_file_path()); //Es necesario eliminar cambios previos por eso reabrimos.
        Gdk.Pixbuf pixbuf = this.pixbuf_to_gris(this.pixbuf, channel);
        this.changed = true;
        this.emit_change(this.changed);
        }

    public void apply_saturacion(float saturar, bool pixelar){
        string info = this.open(this.get_file_path()); //Es necesario eliminar cambios previos por eso reabrimos.
        this.pixbuf.saturate_and_pixelate(this.pixbuf, saturar, pixelar);
        this.changed = true;
        this.emit_change(this.changed);
        }

    public void apply_escala(int w, int h){
        //GLib.stdout.printf("%i x %i\n", w, h);
        string info = this.open(this.get_file_path()); //Es necesario eliminar cambios previos por eso reabrimos.
        this.pixbuf = this.pixbuf.scale_simple(w, h, Gdk.InterpType.HYPER);
        this.changed = true;
        this.emit_change(this.changed);
        }

    public void apply_invertir(){
        string info = this.open(this.get_file_path()); //Es necesario eliminar cambios previos por eso reabrimos.
        int w = this.pixbuf.get_width();
        int h = this.pixbuf.get_height();
        int rowstride = this.pixbuf.get_rowstride();
        int channels = this.pixbuf.get_n_channels();
        unowned uint8[] array = this.pixbuf.get_pixels();
        for (int row = 0; row < h; row++){
            for (int elem = rowstride * row; elem < rowstride * row + rowstride; elem += channels){
                array[elem] = 255 - array[elem];
                array[elem + 1] = 255 - array[elem + 1];
                array[elem + 2] = 255 - array[elem + 2];
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
        //Gdk.Pixbuf pix = new Gdk.Pixbuf.with_unowned_data(
        //    this.pixels, Gdk.Colorspace.RGB, this.pixbuf.has_alpha,
        //    this.pixbuf.bits_per_sample, this.pixbuf.width,
        //    this.pixbuf.height, this.pixbuf.rowstride, null);
        this.pixbuf.save(filepath, "png", null);
        this.file_path = filepath;
        this.changed = false;
        this.emit_change(this.changed);
        }

    public bool get_changed(){
        return this.changed;
        }

    public GLib.List get_resolucion(){
        GLib.List<int> res = new GLib.List<int>();
        res.append(this.pixbuf.get_width());
        res.append(this.pixbuf.get_height());
        return res;
        }
    }
