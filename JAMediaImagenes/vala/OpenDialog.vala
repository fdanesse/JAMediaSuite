

internal class OpenDialog : Gtk.FileChooserDialog{

    private Gtk.FileFilter filtro = new Gtk.FileFilter();

    public OpenDialog(Gtk.Window parent, string dir_path){

        this.add_button("Abrir", Gtk.ResponseType.ACCEPT);
        this.add_button("Cancelar", Gtk.ResponseType.CANCEL);
        this.set_title("Abrir Archivo");
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set_resizable(true);
        this.set_size_request(320, 240);

        this.set_current_folder(dir_path);
        this.set_property("action", Gtk.FileChooserAction.OPEN);
        this.set_select_multiple(false);

        this.filtro.set_name("Imagen");
        this.filtro.add_mime_type("image/*");
        this.add_filter(this.filtro);
        }
    }
