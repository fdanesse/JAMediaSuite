
public class ToolbarGrabar : Gtk.EventBox{

    public signal void detener();
    private Gtk.Label label = new Gtk.Label("ToolbarGrabar");

    public ToolbarGrabar(){

        // FIXME: Agregar Colores
        //self.colors = [get_colors("window"), get_colors("naranaja")]
        //self.color = self.colors[0]

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 3, false);
        toolbar.insert(separador1, -1);

        Gtk.ToolButton button1 = get_button("Iconos/stop.svg", false, 24, "Detener");
		button1.clicked.connect (() => {
			this.__emit_stop();
		});
		toolbar.insert(button1, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 3, false);
        toolbar.insert(separador2, -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        label.show();
        item.add(this.label);
        toolbar.insert(item, -1);

        this.add(toolbar);
        this.show_all();
    }

    private void __emit_stop(){
        this.stop();
        this.detener();
    }

    private void __update(){
        //if this.color == this.colors[0]:
        //    this.color = this.colors[1]
        //elif this.color == this.colors[1]:
        //    this.color = this.colors[0]
        //this.label.modify_fg(0, this.color)
        //if not this.get_visible():
        //    this.show()
    }

    public void stop(){
        //this.color = self.colors[0]
        //this.label.modify_fg(0, self.color)
        this.label.set_text("Grabador Detenido.");
        this.hide();
    }

    public void set_info(string datos){
        this.label.set_text(datos);
        this.__update();
    }
}


public class VideoVisor : Gtk.DrawingArea{
    /*
    __gsignals__ = {
    "ocultar_controles": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}
    */
    public VideoVisor(){
        /*
        self.add_events(
            gtk.gdk.KEY_PRESS_MASK |
            gtk.gdk.KEY_RELEASE_MASK |
            gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_MOTION_MASK |
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK
        )
        */
        this.show_all();
    }
    /*
    def do_motion_notify_event(self, event):
        """
        Cuando se mueve el mouse sobre el visor.
        """
        x, y = (int(event.x), int(event.y))
        rect = self.get_allocation()
        xx, yy, ww, hh = (rect.x, rect.y, rect.width, rect.height)

        if x in range(ww - 60, ww) or y in range(yy, yy + 60) \
            or y in range(hh - 60, hh):
            self.emit("ocultar_controles", False)
            return
        else:
            self.emit("ocultar_controles", True)
            return
    */
}
