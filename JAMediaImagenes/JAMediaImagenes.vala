
// https://wiki.gnome.org/Projects/Vala/StatusIcon
// https://github.com/polymeris/shotwell/blob/master/thumbnailer/shotwell-video-thumbnailer.vala
// https://developer.gnome.org/gdk-pixbuf/stable/gdk-pixbuf-The-GdkPixbuf-Structure.html#image-data
// http://stackoverflow.com/questions/2744118/how-do-i-remove-or-apply-transparency-on-a-gdk-pixbuf

/*
valac --pkg glib-2.0 --pkg gio-2.0 --pkg gtk+-3.0 --pkg gdk-3.0 --pkg gdk-x11-3.0 --pkg gee-1.0
*/

using Gtk;
using Gdk;
using Gee;


public class JAMediaImagenes{

    private Gdk.Pixbuf pixbuf;
    private unowned uint8[] array;
    private uint8[] pixels;

    public JAMediaImagenes(){

        try {
            string path = "/home/flavio/Pruebas_imagenes/autumn_in_japan-1280x800.png";
            this.pixbuf = new Gdk.Pixbuf.from_file(path);
            }
        catch(Error e) {
            GLib.stderr.printf("No se pudo cargar la imagen: %s\n", e.message);
            GLib.stderr.flush();
            }

        int width = this.pixbuf.get_width();
        int height = this.pixbuf.get_height();
        int rowstride = this.pixbuf.get_rowstride(); //Elementos por fila en imagen de 20 * 10 con [rgbh] = 80 (20*4) 20 elementos de 4 componentes
        int channels = this.pixbuf.get_n_channels();
        this.array = this.pixbuf.get_pixels ();
        this.pixels = new uint8[rowstride * height]; //this.pixbuf.get_pixels ();//new uint8[rowstride * height];

        stdout.printf("Resolución: %i %i %i\n", width, height, rowstride * height);
        stdout.printf("Elementos por fila: %i Canales: %i\n", this.pixbuf.get_rowstride(), this.pixbuf.get_n_channels());
        stdout.printf("this.array.length: %u\n", this.array.length);

        for (int row = 0; row < height; row++){
            for (int elem = rowstride*row; elem < rowstride*row+rowstride; elem += channels){
                    //stdout.printf("row: %i, elem: %i\n", row, elem);
                    //uint8 prom = uint8(((float)this.array[elem] + (float)this.array[elem+1] + (float)this.array[elem+2])/3.0);
                    uint8 prom = average(this.array[elem:elem+3]);
                    this.pixels[elem] = prom; //this.array[elem];
                    this.pixels[elem+1] = prom; //this.array[elem+1];
                    this.pixels[elem+2] = prom; //this.array[elem+2];
                }
            }

        try {
            //Gdk.Colorspace.RGB from_data
            Gdk.Pixbuf pix = new Gdk.Pixbuf.with_unowned_data(
                this.pixels, Gdk.Colorspace.RGB, this.pixbuf.has_alpha,
                this.pixbuf.bits_per_sample, this.pixbuf.width,
                this.pixbuf.height, this.pixbuf.rowstride, null);

            pix.save ("/home/flavio/test.png", "png");
            }
        catch(Error e) {
            GLib.stderr.printf("ERROR: %s\n", e.message);
            GLib.stderr.flush();
            }
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

    }


public static int main (string[] args) {
    Gtk.init(ref args);
    JAMediaImagenes app = new JAMediaImagenes();
    return 0;
}
