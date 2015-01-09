
public class Terminal : Gtk.Notebook{

    public Terminal(){

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        //self.notebook = NoteBookTerminal()
        //self.toolbar = ToolbarTerminal()

        //vbox.pack_start(self.notebook, True, True, 0)
        //vbox.pack_start(self.toolbar, False, False, 0)

        this.add(vbox);
        this.show_all();
    }
}
