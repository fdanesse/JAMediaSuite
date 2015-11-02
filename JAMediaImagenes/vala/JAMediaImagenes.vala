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
using Gee;


public class JAMediaImagenes : Gtk.Window{

    private MenuPrincipal menu = new MenuPrincipal();
    private ToolbarPrincipal toolbar = new ToolbarPrincipal();
    private Gtk.Image image = new Gtk.Image();
    private Gtk.Statusbar statusbar = new Gtk.Statusbar();
    private ImgProcessor processor = new ImgProcessor();
    private Grises grises = null;
    private Canales canales = null;

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
        this.key_press_event.connect ((event) => {
            this.do_key_press_event(event);
            return true;
            });

        GLib.stdout.printf("JAMediaImagenes process: %i\n", Posix.getpid());
        GLib.stdout.flush();

        this.close_file();
        }

    private void do_key_press_event(Gdk.EventKey event){
        string filepath = this.processor.get_file_path();
        if (filepath != ""){
            if (event.keyval == 65307){
                if (this.processor.get_changed()){
                    this.confirmar_guardar();
                    }
                ExitDialog dialog = new ExitDialog(
                this.get_toplevel() as Gtk.Window);
                int run = dialog.run();
                dialog.destroy();
                if (run == Gtk.ResponseType.ACCEPT){
                    this.salir();
                    }
                }
            else if (event.keyval == 65361){
                this.toolbar_accion("Ver imagen anterior");
                }
            else if (event.keyval == 65363){
                this.toolbar_accion("Ver imagen siguiente");
                }
            else if (event.keyval == 65535){
                RemoveDialog dialog = new RemoveDialog(
                this.get_toplevel() as Gtk.Window);
                int run = dialog.run();
                dialog.destroy();
                if (run == Gtk.ResponseType.ACCEPT){
                    Gee.ArrayList<string> items = this.list_dir();
                    int index = items.index_of(filepath);
                    if (items.size > 1){
                        if (index < items.size - 1){
                            index++;
                            }
                        else{
                            index = 0;
                            }
                        string newfilepath = items[index];
                        this.open_file(newfilepath);
                        }
                    else{
                        this.close_file();
                        }
                    //GLib.FileUtils.remove(filepath);
                    GLib.File file = GLib.File.parse_name(filepath);
                    try{
                        file.trash();
                        }
                    catch(Error e) {
                        GLib.stderr.printf("ERROR al borrar un archivo: %s\n", e.message);
                        GLib.stderr.flush();
                        }
                    }
                }
            }
        else{
            if (event.keyval == 65307){
                this.salir();
                }
            }
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
            if (this.processor.get_file_path() != ""){
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_zoom_in();
                this.image.set_from_pixbuf(pixbuf);
                }
            }
        else if (accion == "Alejar"){
            if (this.processor.get_file_path() != ""){
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_zoom_out();
                this.image.set_from_pixbuf(pixbuf);
                }
            }
        else if (accion == "Ver tamaño original"){
            if (this.processor.get_file_path() != ""){
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf();
                this.image.set_from_pixbuf(pixbuf);
                }
            }
        else if (accion == "Ocupar todo el espacio"){
            if (this.processor.get_file_path() != ""){
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(
                    this.image.get_parent().get_allocated_width(),
                    this.image.get_parent().get_allocated_height());
                this.image.set_from_pixbuf(pixbuf);
                }
            }
        else if (accion == "Rotar a la izquierda"){
            if (this.processor.get_file_path() != ""){
                Gdk.Pixbuf pixbuf = this.processor.rotate_left();
                this.image.set_from_pixbuf(pixbuf);
                }
            }
        else if (accion == "Rotar a la derecha"){
            if (this.processor.get_file_path() != ""){
                Gdk.Pixbuf pixbuf = this.processor.rotate_right();
                this.image.set_from_pixbuf(pixbuf);
                }
            }
        else if (accion == "Ver imagen anterior"){
            string filepath = this.processor.get_file_path();
            if (filepath != ""){
                if (this.processor.get_changed()){
                    this.confirmar_guardar();
                    }
                Gee.ArrayList<string> items = this.list_dir();
                int index = items.index_of(this.processor.get_file_path());
                if (index > 0){
                    index--;
                    }
                else{
                    index = items.size - 1;
                    }
                string newfilepath = items[index];
                this.open_file(newfilepath);
                }
            }
        else if (accion == "Ver imagen siguiente"){
            string filepath = this.processor.get_file_path();
            if (filepath != ""){
                if (this.processor.get_changed()){
                    this.confirmar_guardar();
                    }
                Gee.ArrayList<string> items = this.list_dir();
                int index = items.index_of(this.processor.get_file_path());
                if (index < items.size - 1){
                    index++;
                    }
                else{
                    index = 0;
                    }
                string newfilepath = items[index];
                this.open_file(newfilepath);
                }
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

    private void confirmar_guardar(){
        CheckDialog dialog = new CheckDialog(
            this.get_toplevel() as Gtk.Window);
        int run = dialog.run();
        dialog.destroy();
        if (run == Gtk.ResponseType.ACCEPT){
            try{
                this.processor.save_file(this.processor.get_file_path());
                }
            catch(GLib.Error e){
                GLib.stdout.printf("ERROR al Guardar: %s\n", e.message);
                GLib.stdout.flush();
                }
            }
        }

    private Gee.ArrayList<string> list_dir(){
        Gee.ArrayList<string> items = new Gee.ArrayList<string> ();
        string dirpath = this.processor.get_dir_path();
        int index = 0;
        try{
            GLib.Dir dir = GLib.Dir.open(dirpath, 0);
            string? name = null;
            while ((name = dir.read_name()) != null) {
                string path = GLib.Path.build_filename(dirpath, name);
                GLib.File file = GLib.File.parse_name(path);
                var file_info = file.query_info ("*", GLib.FileQueryInfoFlags.NONE);
                string tipo = file_info.get_content_type();
                if ("image" in tipo){
                    items.insert(index, path);
                    index++;
                    }
                }
            }
        catch (GLib.FileError err) {
            GLib.stderr.printf(err.message);
            }
        items.sort(GLib.strcmp);
        return items;
        }

    private void menu_accion(string accion){
        if (accion == "Abrir..."){
            this.toolbar_accion("Abrir");
            }
        else if (accion == "Guardar"){
            this.toolbar_accion("Guardar");
            }
        else if (accion == "Guardar Como..."){
            this.toolbar_accion("Guardar Como");
            }
        else if (accion == "Cerrar"){
            this.close_file();
            }
        else if (accion == "Grises..."){
            if (this.grises == null){
                this.grises = new Grises(this.get_toplevel() as Gtk.Window);
                this.grises.set_processor(this.processor);
                this.grises.change_channel.connect(this.change_channel);
                this.grises.destroy.connect ((source) => {
                    this.util_exit("Grises");
                 });
                }
            }
        else if (accion == "Canales..."){
            if (this.canales == null){
                this.canales = new Canales(this.get_toplevel() as Gtk.Window);
                this.canales.set_processor(this.processor);
                //this.canales.change_channel.connect(this.change_channel);
                this.canales.destroy.connect ((source) => {
                    this.util_exit("Canales");
                 });
                }
            }
        else{
            GLib.stdout.printf("Menu Accion: %s\n", accion);
            GLib.stdout.flush();
            }
        }

    private void change_channel(string channel){
        string filepath = this.processor.get_file_path();
        if (filepath != ""){
            if ("Original" in channel){
                this.open_file(filepath);
                }
            else if ("Average" in channel){
                this.processor.apply_channel("average");
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(
                    this.image.get_parent().get_allocated_width(),
                    this.image.get_parent().get_allocated_height());
                this.image.set_from_pixbuf(pixbuf);
                }
            else if ("Percentual" in channel){
                this.processor.apply_channel("percentual");
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(
                    this.image.get_parent().get_allocated_width(),
                    this.image.get_parent().get_allocated_height());
                this.image.set_from_pixbuf(pixbuf);
                }
            else if ("Luminosity" in channel){
                this.processor.apply_channel("luminosity");
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(
                    this.image.get_parent().get_allocated_width(),
                    this.image.get_parent().get_allocated_height());
                this.image.set_from_pixbuf(pixbuf);
                }
            else if ("Lightness" in channel){
                this.processor.apply_channel("lightness");
                Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(
                    this.image.get_parent().get_allocated_width(),
                    this.image.get_parent().get_allocated_height());
                this.image.set_from_pixbuf(pixbuf);
                }
            }
        }

    private void close_file(){
        this.processor.close_file();
        this.menu.has_file(false);
        this.toolbar.has_file(false);
        this.update_status_bar("Img:");
        this.image.clear();
        if (this.grises != null){
            this.grises.set_processor(this.processor);
            }
        }

    private void open_file(string filepath){
        //FIXME: Agregar control de permisos para luego activar o desactivar opciones guardar
        this.close_file();
        string info = this.processor.open(filepath);
        //acceso = os.access(filepath, os.W_OK)
        this.menu.has_file(true);
        this.update_status_bar(info);
        this.toolbar.has_file(true);
        Gdk.Pixbuf pixbuf = this.processor.get_pixbuf_scale(
            this.image.get_parent().get_allocated_width(),
            this.image.get_parent().get_allocated_height());
        this.image.set_from_pixbuf(pixbuf);
        if (this.grises != null){
            this.grises.set_processor(this.processor);
            }
        }

    private void update_status_bar(string info){
        this.statusbar.push(0, info);
        }

    private void util_exit(string util){
        if (util == "Grises"){
            this.grises = null;
            }
        else if (util == "Canales"){
            this.canales = null;
            }
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
