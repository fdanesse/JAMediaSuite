/*
Instalaciones previas:
valac libgtk-3-dev
*/

/*
Compilar con:
    valac --pkg posix --pkg glib-2.0 --pkg gtk+-3.0 --pkg gdk-3.0
*/


//using GLib;   Se importa siempre por default
using Gtk;
using Gdk;
using Posix;


public class JAMediaImagenes : Gtk.Window{

    private MenuPrincipal menu = new MenuPrincipal();
    private ToolbarPrincipal toolbar = new ToolbarPrincipal();
    private Gtk.Image image = new Gtk.Image();
    private Gtk.Statusbar statusbar = new Gtk.Statusbar();
    private ImgProcessor processor = new ImgProcessor();

    public JAMediaImagenes(){

        this.set_title("JAMediaImagenes");
        this.window_position = Gtk.WindowPosition.CENTER;
        this.set_default_size(640, 480);
        this.set_resizable(true);
        this.set("border_width", 2);

        try {
            Gtk.Window.set_default_icon_from_file("Iconos/JAMediaImagenes.svg");
            }
        catch(Error e) {
            GLib.stderr.printf("No se Encontró el Ícono: %s\n", e.message);
            GLib.stderr.flush();
            }

        Gtk.Box box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        Gtk.ScrolledWindow scroll = new Gtk.ScrolledWindow(null, null);
        scroll.set("hscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll.add_with_viewport(this.image);

        box.pack_start(this.menu, false, false, 0);
        box.pack_start(this.toolbar, false, false, 0);
        box.pack_start(scroll, true, true, 0);
        box.pack_end(this.statusbar, false, false, 0);

        this.add(box);
        this.show_all();

        this.processor.has_change.connect ((changed) => {
            this.has_change_in_file(changed);
         });
        this.menu.accion.connect ((accion) => {
            this.menu_accion(accion);
         });
        this.toolbar.accion.connect ((accion) => {
            this.toolbar_accion(accion);
         });
        this.destroy.connect(this.salir);

        GLib.stdout.printf("JAMediaImagenes process: %i\n", Posix.getpid());
        GLib.stdout.flush();

        this.close_file();
        }

    private void has_change_in_file(bool changed){
        this.menu.has_change(changed);
        this.toolbar.has_change(changed);
        }

    private void toolbar_accion(string accion){
        if (accion == "Abrir"){
            OpenDialog dialog = new OpenDialog(
                this.get_toplevel() as Gtk.Window,
                this.processor.get_dir_path());
            int run = dialog.run();
            string filepath = dialog.get_filename();
            dialog.destroy();
            if (run == Gtk.ResponseType.ACCEPT){
                this.open_file(filepath);
                }
            }
        else if (accion == "Acercar"){
            Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_zoom_in();
            this.image.set_from_pixbuf(pixbuf);
            }
        else if (accion == "Alejar"){
            Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_zoom_out();
            this.image.set_from_pixbuf(pixbuf);
            }
        else if (accion == "Ver tamaño original"){
            Gdk.Pixbuf pixbuf = this.processor.get_pixbuf();
            this.image.set_from_pixbuf(pixbuf);
            }
        else if (accion == "Ocupar todo el espacio"){
            Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(
                this.image.get_parent().get_allocated_width(),
                this.image.get_parent().get_allocated_height());
            this.image.set_from_pixbuf(pixbuf);
            }
        else if (accion == "Rotar a la izquierda"){
            Gdk.Pixbuf pixbuf = this.processor.rotate_left();
            this.image.set_from_pixbuf(pixbuf);
            }
        else if (accion == "Rotar a la derecha"){
            Gdk.Pixbuf pixbuf = this.processor.rotate_right();
            this.image.set_from_pixbuf(pixbuf);
            }
        else if (accion == "Ver imagen anterior"){
            }
        else if (accion == "Ver imagen siguiente"){
            }
        else if (accion == "Guardar"){
            string filepath = this.processor.get_file_path();
            try{
                this.processor.save_file(filepath);
                this.open_file(filepath);
                }
            catch(GLib.Error e){
                GLib.stdout.printf("ERROR al Guardar: %s\n", e.message);
                GLib.stdout.flush();
                }
            }
        else if (accion == "Guardar Como"){
            SaveDialog dialog = new SaveDialog(
                this.get_toplevel() as Gtk.Window,
                this.processor.get_dir_path());
            int run = dialog.run();
            string filepath = dialog.get_filename();
            dialog.destroy();
            if (run == Gtk.ResponseType.ACCEPT){
                try{
                    this.processor.save_file(filepath);
                    this.open_file(filepath);
                    }
                catch(GLib.Error e){
                    GLib.stdout.printf("ERROR al Guardar: %s\n", e.message);
                    GLib.stdout.flush();
                    }
                }
            }
        else{
            GLib.stdout.printf("Toolbar Accion: %s\n", accion);
            GLib.stdout.flush();
            }
        }

    private void menu_accion(string accion){
        if (accion == "Abrir..."){
            OpenDialog dialog = new OpenDialog(
                this.get_toplevel() as Gtk.Window,
                this.processor.get_dir_path());
            int run = dialog.run();
            if (run == Gtk.ResponseType.ACCEPT){
                this.open_file(dialog.get_filename());
                }
            dialog.destroy();
            }
        else if (accion == "Cerrar"){
            this.close_file();
            }
        else{
            GLib.stdout.printf("Menu Accion: %s\n", accion);
            GLib.stdout.flush();
            }
        }

    private void close_file(){
        this.processor.close_file();
        this.menu.has_file(false);
        this.toolbar.has_file(false);
        this.update_status_bar("");
        this.image.clear();
        }

    private void open_file(string filepath){
        //FIXME: Agregar control de permisos para luego activar o desactivar opciones guardar
        this.close_file();
        string info = this.processor.open(filepath);
        //acceso = os.access(filepath, os.W_OK)
        this.menu.has_file(true);
        this.update_status_bar(info);
        this.toolbar.has_file(true);
        Gdk.Pixbuf pixbuf = this.processor.get_pixbuf();
        this.image.set_from_pixbuf(pixbuf);
        }

    private void update_status_bar(string info){
        string text = "Img: ";
        //if info:
        //    text = "%s %s   Size: %s   Ext: %s   Mime: %s   Kb: %.2f" % (
        //        text, info.get("path", ""), info.get("size", ""),
        //        info.get("name", ""), info.get("mime_types", ""),
        //        info.get("mb", 0.0) / 1024.0)
        this.statusbar.push(0, text);
        }

    private void salir(){
        Gtk.main_quit();
        }
    }


public static int main (string[] args) {
    Gtk.init(ref args);
    JAMediaImagenes app = new JAMediaImagenes();
    app.show_all();
    Gtk.main();
    return 0;
}
