
public class Multiple_FileChooser : Gtk.FileChooserDialog{

    private Gtk.FileFilter filtro = new Gtk.FileFilter();

    public Multiple_FileChooser(string title, Gtk.Window parent,
        Gtk.FileChooserAction action, SList<string> filter_type,
        SList<string> mime, string path){

        this.set_title(title);
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set_resizable(true);
        this.set_size_request(320, 240);

        this.set_current_folder(path);
        this.set_property("action", action);
        this.set_select_multiple(true);

        this.add_button("Abrir", Gtk.ResponseType.ACCEPT);
        this.add_button("Cancelar", Gtk.ResponseType.CANCEL);

        this.filtro.set_name("Filtro");
        foreach (unowned string fil in filter_type){
            filtro.add_pattern(fil);
            }
        foreach (unowned string mi in mime){
            filtro.add_mime_type(mi);
            }
        this.add_filter(this.filtro);

        this.realize.connect(this.__resize);
    }

    private void __resize(){
        this.resize(437, 328);
        }
}
