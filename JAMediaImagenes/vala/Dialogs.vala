
//FIXME: Mejorar Filtros para seleccionar tipos específicos de imagen?.

internal class OpenDialog : Gtk.FileChooserDialog{

    private Gtk.FileFilter filtro = new Gtk.FileFilter();
    private Preview preview = new Preview();

    public OpenDialog(Gtk.Window parent, string dir_path){

        this.add_button("Abrir", Gtk.ResponseType.ACCEPT);
        this.add_button("Cancelar", Gtk.ResponseType.CANCEL);
        this.set_title("Abrir Archivo");
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set_resizable(true);
        this.set_size_request(320, 240);
        this.set_preview_widget(this.preview);
        this.set_use_preview_label(false);
        this.set_current_folder(dir_path);
        this.set_property("action", Gtk.FileChooserAction.OPEN);
        this.set_select_multiple(false);

        this.filtro.set_name("Imagen");
        this.filtro.add_mime_type("image/*");
        this.add_filter(this.filtro);

        //FIXME: Hay un Error acá
        //this.update_preview.connect (() => {
        //    this.run_update_preview();
        //    });
        }

    //private void run_update_preview(){
    //    string filepath = this.get_filename();
    //    this.preview.update(filepath);
    //    }

    }


internal class SaveDialog : Gtk.FileChooserDialog{

    private Gtk.FileFilter filtro = new Gtk.FileFilter();
    private Preview preview = new Preview();

    public SaveDialog(Gtk.Window parent, string dir_path){

        this.add_button("Guardar", Gtk.ResponseType.ACCEPT);
        this.add_button("Cancelar", Gtk.ResponseType.CANCEL);
        this.set_title("Guardar Archivo Como...");
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set_resizable(true);
        this.set_size_request(320, 240);
        this.set_do_overwrite_confirmation(true);
        this.set_preview_widget(this.preview);
        this.set_use_preview_label(false);
        this.set_current_folder(dir_path);
        this.set_property("action", Gtk.FileChooserAction.SAVE);
        this.set_select_multiple(false);

        this.filtro.set_name("Imagen");
        this.filtro.add_mime_type("image/*");
        this.add_filter(this.filtro);

        //FIXME: Hay un Error acá
        //this.update_preview.connect (() => {
        //    this.run_update_preview();
        //    });
        }

    //private void run_update_preview(){
    //    string filepath = this.get_filename();
    //    this.preview.update(filepath);
    //    }
    }


internal class CheckDialog : Gtk.Dialog{

    public CheckDialog(Gtk.Window parent){

        this.add_button("Guardar", Gtk.ResponseType.ACCEPT);
        this.add_button("Cancelar", Gtk.ResponseType.CANCEL);
        this.set_modal(true);
        this.set("border_width", 10);
        this.set_transient_for(parent);
        Gtk.Label label1 = new Gtk.Label(
            "El archivo actual contiene cambios sin guardar.");
        Gtk.Label label2 = new Gtk.Label("¿Deseas Guardarlos?");
        Gtk.Box Box = this.get_content_area();
        Box.pack_start(label1, false, false, 5);
        Box.pack_start(label2, false, false, 5);
        Box.show_all();

        }
    }


internal class ExitDialog : Gtk.Dialog{

    public ExitDialog(Gtk.Window parent){

        this.add_button("Guardar", Gtk.ResponseType.ACCEPT);
        this.add_button("Cancelar", Gtk.ResponseType.CANCEL);
        this.set_modal(true);
        this.set("border_width", 10);
        this.set_transient_for(parent);
        string text = "¿Confirmas salir de la aplicación?";
        Gtk.Label label = new Gtk.Label(text);
        Gtk.Box Box = this.get_content_area();
        Box.pack_start(label, false, false, 0);
        Box.show_all();

        }
    }


//FIXME: Arreglar estética
internal class Preview : Gtk.Frame{

    private Gtk.Image image = new Gtk.Image();

    public Preview(){
        this.image.set_size_request(100, 100);
        this.set_label(" Preview: ");
        this.add(this.image);
        this.show_all();
        }

    public void update(string filepath){
        try {
            Gdk.Pixbuf pixbuf = new Gdk.Pixbuf.from_file_at_scale(
                filepath, 100, 100, true);
            this.image.set_from_pixbuf(pixbuf);
            }
        catch(Error e) {
            this.image.clear();
            }
        }
    }
