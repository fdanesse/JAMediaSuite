
public class InfoNotebook : Gtk.Notebook{

    public InfoNotebook(){

        //self.estructura_proyecto = Estructura_Proyecto()
        //self.introspeccion = Introspeccion()

        Gtk.ScrolledWindow scroll1 = new Gtk.ScrolledWindow(null, null);
        scroll1.set("hscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll1.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        //scroll1.add(this.introspeccion);
        this.append_page(scroll1, new Gtk.Label("Introspección"));

        Gtk.ScrolledWindow scroll2 = new Gtk.ScrolledWindow(null, null);
        scroll2.set("hscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll2.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        //scroll2.add(this.estructura_proyecto);
        this.append_page(scroll2, new Gtk.Label("Proyecto"));

        this.show_all();
    }
}
