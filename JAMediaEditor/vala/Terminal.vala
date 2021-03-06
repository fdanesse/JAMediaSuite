
public class Terminal : Gtk.EventBox{

    private NoteBookTerminal notebook = new NoteBookTerminal();
    private ToolbarTerminal toolbar = new ToolbarTerminal();

    public Terminal(){

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        vbox.pack_start(this.notebook, true, true, 0);
        vbox.pack_end(this.toolbar, false, false, 0);

        this.add(vbox);
        this.show_all();
    }
}


public class NoteBookTerminal : Gtk.Notebook{

    public NoteBookTerminal(){

        this.set_scrollable(true);
        //self.fuente = Pango.FontDescription("Monospace %s" % 10)

        Gtk.ScrolledWindow scroll1 = new Gtk.ScrolledWindow(null, null);
        scroll1.set("hscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll1.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        this.append_page(scroll1, new Gtk.Label("Ejemplo"));

        this.show_all();
        //self.connect('switch_page', self.__switch_page)
    }
}
