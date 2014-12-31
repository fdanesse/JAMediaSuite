
public class ToolbarGrabar : Gtk.EventBox{

    public signal void detener();
    private Gtk.Label label = new Gtk.Label("ToolbarGrabar");
    private Gdk.Color color1;
    private Gdk.Color color2;
    private Gdk.Color color;

    public ToolbarGrabar(){

        Gdk.Color.parse("#ffffff", out this.color1);
        Gdk.Color.parse("#ff6600", out this.color2);
        this.color = this.color1;

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
        if (this.color == this.color1){
            this.color = this.color2;
            }
        else if (this.color == this.color2){
            this.color = this.color1;
            }
        this.label.modify_fg(Gtk.StateType.NORMAL, this.color);
        if (this.get_visible() == false){
            this.show();
            }
        }

    public void stop(){
        this.color = this.color1;
        this.label.modify_fg(Gtk.StateType.NORMAL, this.color);
        this.label.set_text("Grabador Detenido.");
        this.hide();
        }

    public void set_info(string datos){
        this.label.set_text(datos);
        this.__update();
        }
}


public class VideoVisor : Gtk.DrawingArea{

    public signal void ocultar_controles(bool valor);
    public uint* xid;

    public VideoVisor(){

        this.add_events(
            Gdk.EventMask.KEY_PRESS_MASK |
            Gdk.EventMask.KEY_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.POINTER_MOTION_HINT_MASK |
            Gdk.EventMask.BUTTON_MOTION_MASK |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK
            );

        this.realize.connect(this.__realize);

        this.show_all();

        this.motion_notify_event.connect ((event) => {
			this.__do_motion_notify_event(event);
			return true;
		});
    }

    private void __realize(){
        this.xid = (uint*)Gdk.X11Window.get_xid(this.get_window());
        }

    private void __do_motion_notify_event(Gdk.EventMotion event){
        int x = (int) event.x;
        int y = (int) event.y;
        //Gdk.Allocation allocation;
        //this.get_allocation(out allocation);
        int ww = (int) this.get_allocated_width();
        int hh = (int) this.get_allocated_height();

        int minw = ww - 60;
        int minh = hh - 60;

        if ((x > minw && x < ww) || (y > 0 && y < 60) || (y < hh && y > minh)){
            this.ocultar_controles(false);
            }
        else{
            this.ocultar_controles(true);
            }
        }
}


public class BufferInfo : Gtk.EventBox{

    private ProgressBar escala = new ProgressBar();
    private double valor = 0.0;
    private Gtk.Frame frame = new Gtk.Frame(" Cargando Buffer ... ");

    public BufferInfo(){

        this.set_border_width(4);

        this.frame.set_border_width(4);
        this.frame.set_label_align((float) 0.0, (float) 0.5);

        this.frame.add(this.escala);
        this.add(this.frame);
        this.show_all();
        this.set_sensitive(false);
    }

    public void set_progress(int valor){

        if (this.valor != valor){
            this.frame.set_label(string.join(" ", " Cargando Buffer:", valor.to_string(), "%"));
            this.valor = valor;
            this.escala.ajuste.set_value(valor);
            this.escala.queue_draw();
            }

        if (this.valor == 100){
            this.frame.set_label(" Cargando Buffer ... ");
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
    /*
    private bool __expose(Cairo.Context gc){
        //https://wiki.gnome.org/Projects/Vala/CairoSample
        GLib.stdout.printf ("%f\n", this.escala.get_value());
        GLib.stdout.flush();
        return true;
        }
    */
}
