
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

        Gtk.ToolButton button1 = get_button("Iconos/stop.svg", false, Gdk.PixbufRotation.NONE, 24, "Detener");
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
    //FIXME: Agregar eventos del mouse
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


public class BufferInfo : Gtk.EventBox{

    private ProgressBar escala = new ProgressBar();
    private double valor = 0.0;

    public BufferInfo(){

        this.set_border_width(4);

        Gtk.Frame frame = new Gtk.Frame(" Cargando Buffer ... ");
        frame.set_border_width(4);
        frame.set_label_align((float) 0.0, (float) 0.5);

        frame.add(this.escala);
        this.add(frame);
        this.show_all();
        this.set_sensitive(false);
    }

    public void set_progress(double valor){
        if (this.valor == valor){
            }
        else{
            this.valor = valor;
            this.escala.ajuste.set_value(valor);
            this.escala.queue_draw();
            }

        if (this.valor == 100.0){
            this.hide();
            }
        else{
            this.show();
            }
    }
}


public class ToolbarInfo : Gtk.EventBox{

    public signal void rotar(string rotacion);
    public signal void actualizar_streamings();

    private Gtk.ToolButton boton_izquierda = get_button("Iconos/rotar.svg", false, Gdk.PixbufRotation.NONE, 24, "Izquierda");
    private Gtk.ToolButton boton_derecha = get_button("Iconos/rotar.svg", true, Gdk.PixbufRotation.NONE, 24, "Derecha");
    private Gtk.ToolButton descarga = get_button("Iconos/iconplay.svg", true, Gdk.PixbufRotation.COUNTERCLOCKWISE, 24, "Actualizar Streamings");
    public bool ocultar_controles = false;

    public ToolbarInfo(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 0, true);
        toolbar.insert(separador1, -1);

		this.boton_izquierda.clicked.connect (() => {
			this.__emit_rotar("Izquierda");
		});
		toolbar.insert(this.boton_izquierda, -1);

		this.boton_derecha.clicked.connect (() => {
			this.__emit_rotar("Derecha");
		});
		toolbar.insert(this.boton_derecha, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 0, true);
        toolbar.insert(separador2, -1);

        Gtk.ToolItem item1 = new Gtk.ToolItem();
        Gtk.Label label = new Gtk.Label("Ocultar Controles:");
        label.show();
        item1.add(label);
        toolbar.insert(item1, -1);

        Gtk.SeparatorToolItem separador3 = get_separador(false, 3, false);
        toolbar.insert(separador3, -1);

        Gtk.ToolItem item2 = new Gtk.ToolItem();
        Gtk.CheckButton check = new Gtk.CheckButton();
        check.show();
        check.clicked.connect (() => {
			this.__set_controles_view(check);
		});
        item2.add(check);
        toolbar.insert(item2, -1);

        this.descarga.clicked.connect (() => {
			this.__emit_actualizar_streamings();
		});
		toolbar.insert(this.descarga, -1);

        this.add(toolbar);
        this.show_all();
        }

    private void __emit_actualizar_streamings(){
        this.actualizar_streamings();
        }

    private void __emit_rotar(string rotacion){
        this.rotar(rotacion);
        }

    private void __set_controles_view(Gtk.CheckButton widget){
        this.ocultar_controles = widget.active;
        }

    public void set_video(bool valor){
        this.boton_izquierda.set_sensitive(valor);
        this.boton_derecha.set_sensitive(valor);
        }

    public void set_ip(bool valor){
        this.descarga.set_sensitive(valor);
        }
}


public class ProgressBar : Gtk.EventBox{

    private Gtk.Scale escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    public Gtk.Adjustment ajuste = new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0);
    //private int ancho = 10;
    //private int borde = 10;

    public ProgressBar(){

        this.set_border_width(4);
        this.escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, this.ajuste);
        this.escala.set_digits(0);
        this.escala.set_draw_value(false);

        // FIXME: Implementar Dibujo con cairo
        //this.escala.draw.connect ((context) => {
        //    this.__expose(context);
		//});
        /*
		this.escala.draw.connect ((context) => {
			// Get necessary data:
			weak Gtk.StyleContext style_context = this.escala.get_style_context ();
			int height = this.escala.get_allocated_height ();
			int width = this.escala.get_allocated_width ();
			Gdk.RGBA color = style_context.get_color (0);

			// Draw an arc:
			double xc = width / 2.0;
			double yc = height / 2.0;
			double radius = int.min (width, height) / 2.0;
			double angle1 = 0;
			double angle2 = 2*Math.PI;

			context.arc (xc, yc, radius, angle1, angle2);
			Gdk.cairo_set_source_rgba (context, color);
			context.fill ();

			return true;
		});
        */
        this.add(this.escala);
        this.show_all();
    }

    private bool __expose(Cairo.Context gc){
        //https://wiki.gnome.org/Projects/Vala/CairoSample
        stdout.printf ("%f\n", this.escala.get_value());
        return true;
        }

}
