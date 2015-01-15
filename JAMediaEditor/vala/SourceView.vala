
public class SourceView : Gtk.SourceView{

    private Gtk.SourceLanguageManager lenguaje_manager = new Gtk.SourceLanguageManager();
    private string archivo = null;
    private string fuente = "Monospace";
    private int tamanio = 10;
    private bool numeracion = true;
    private Gtk.SourceLanguage lenguaje = null;

    public SourceView(string fuente, int tamanio, bool numeracion){

        this.fuente = fuente;
        this.tamanio = tamanio;
        this.numeracion = numeracion;

        //self.actualizador = False
        //self.control = False
        //self.tab = "    "

        this.set_property("show_line_numbers", this.numeracion);

        //self.lenguajes = {}
        //for _id in self.lenguaje_manager.get_language_ids():
        //    lang = self.lenguaje_manager.get_language(_id)
        //    self.lenguajes[_id] = lang.get_mime_types()

        this.set_insert_spaces_instead_of_tabs(true);
        this.set_tab_width(4);
        this.set_show_right_margin(true);
        this.set_auto_indent(true);
        //this.set_smart_home_end(true);
        this.set_highlight_current_line(true);

        //font = "%s %s" % (config['fuente'], config['tamanio'])
        //self.modify_font(Pango.FontDescription(font))

        this.show_all();

        //self.connect("key-press-event", self.__key_press_event)
    }

    public void set_archivo(string archivo){
        this.archivo = archivo;

        if (archivo != null){
            GLib.File file = GLib.File.parse_name(this.archivo);
            if (file.query_exists()){
                try {
		            string texto;
                    GLib.FileUtils.get_contents(this.archivo, out texto);
                    this.set_buffer(new Gtk.SourceBuffer(null));
                    // FIXME: self.get_buffer().begin_not_undoable_action()
                    this.__set_lenguaje(this.archivo);
                    this.get_buffer().set_text(texto);

                    //nombre = os.path.basename(self.archivo)
                    //if len(nombre) > 13:
                    //    nombre = nombre[0:13] + " . . . "
                    //GLib.idle_add(self.__set_label, nombre)
                    // FIXME: self.control = os.path.getmtime(self.archivo)
		            }
                catch (Error e){}
                }
            }
        else{
            this.set_buffer(new Gtk.SourceBuffer(null));
            //self.get_buffer().begin_not_undoable_action()
            }

        //self.get_buffer().end_not_undoable_action()
        this.get_buffer().set_modified(false);

        //self.new_handle(True)
        }

    private void __set_lenguaje(string archivo){
        this.get_buffer().set_property("highlight_syntax", true);
        this.lenguaje = lenguaje_manager.guess_language(archivo, null);
        this.get_buffer().set_property("language", this.lenguaje);
        // FIXME: GLib.timeout_add(3, self.__force_emit_new_select)
        }
}
