
public class ToolbarEstado : Gtk.EventBox{

    private Gtk.Label label = new Gtk.Label("Status");

    public ToolbarEstado(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();
        //toolbar.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#000000'))

        toolbar.insert(get_separador(false, 3, false), -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        item.set_expand(false);
        this.label.set_property("justify", Gtk.Justification.LEFT);
        // FIXME: Ver como se hace esto en el archivo css
        Gdk.Color color;
        Gdk.Color.parse("#ffffff", out color);
        this.label.modify_fg(Gtk.StateType.NORMAL, color);
        this.label.show();
        item.add(this.label);
        toolbar.insert(item, -1);

        toolbar.insert(get_separador(false, 0, true), -1);

        this.add(toolbar);
        this.show_all();
    }
    /*
    def set_info(self, _dict):
        reng = _dict['renglones']
        carac = _dict['caracteres']
        arch = _dict['archivo']

        text = self.label.get_text()
        new_text = u"Archivo: %s  Lineas: %s  Caracteres: %s" % (
            arch, reng, carac)

        try:
            if text != new_text:
                self.label.set_text(new_text)
        except:
            pass
    */
}
