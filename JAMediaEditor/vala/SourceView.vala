
public class SourceView : Gtk.SourceView{

    private Gtk.SourceLanguageManager lenguaje_manager = new Gtk.SourceLanguageManager();

    public SourceView(){

        this.set_insert_spaces_instead_of_tabs(true);
        this.set_tab_width(4);
        this.set_show_right_margin(true);
        this.set_auto_indent(true);
        //this.set_smart_home_end(true);
        this.set_highlight_current_line(true);

        this.show_all();
    }
}
