
public class BalanceWidget : Gtk.EventBox{

    public signal void balance_valor(string prop, double valor);

    private ToolbarcontrolValores brillo = new ToolbarcontrolValores("Brillo");
    private ToolbarcontrolValores contraste = new ToolbarcontrolValores("Contraste");
    private ToolbarcontrolValores saturacion = new ToolbarcontrolValores("Saturación");
    private ToolbarcontrolValores hue = new ToolbarcontrolValores("Matíz");
    private ToolbarcontrolValores gamma = new ToolbarcontrolValores("Gamma");

    public BalanceWidget(){

        Gtk.AttachOptions flags = Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL;
        Gtk.Table tabla = new Gtk.Table(5, 1, true);

        tabla.attach(this.brillo, 0, 1, 0, 1, flags, flags, 0, 0);
        tabla.attach(this.contraste, 0, 1, 1, 2, flags, flags, 0, 0);
        tabla.attach(this.saturacion, 0, 1, 2, 3, flags, flags, 0, 0);
        tabla.attach(this.hue, 0, 1, 3, 4, flags, flags, 0, 0);
        tabla.attach(this.gamma, 0, 1, 4, 5, flags, flags, 0, 0);

        this.add(tabla);
        this.show_all();

        this.set_size_request(150, -1);

        this.brillo.user_set_value.connect ((valor) => {
			this.__emit_senial(valor, "brillo");
		});
        this.contraste.user_set_value.connect ((valor) => {
			this.__emit_senial(valor, "contraste");
		});
        this.saturacion.user_set_value.connect ((valor) => {
			this.__emit_senial(valor, "saturacion");
		});
        this.hue.user_set_value.connect ((valor) => {
			this.__emit_senial(valor, "hue");
		});
        this.gamma.user_set_value.connect ((valor) => {
			this.__emit_senial(valor, "gamma");
		});
    }

    private void __emit_senial(double valor, string prop){
        this.balance_valor(prop, valor);
        }

    public void set_balance(string prop, double valor){
        if (prop == "saturacion"){
            this.saturacion.set_progress(valor);
            }
        else if (prop == "contraste"){
            this.contraste.set_progress(valor);
            }
        else if (prop == "brillo"){
            this.brillo.set_progress(valor);
            }
        else if (prop == "hue"){
            this.hue.set_progress(valor);
            }
        else if (prop == "gamma"){
            this.gamma.set_progress(valor);
            }
        }
}


public class ToolbarcontrolValores : Gtk.Toolbar{

    public signal void user_set_value(double valor);

    private SlicerBalance escala = new SlicerBalance();
    private Gtk.Frame frame = new Gtk.Frame("");
    private Gtk.Label label = new Gtk.Label("");

    public ToolbarcontrolValores(string titulo){

        Gtk.ToolItem item2 = new Gtk.ToolItem();
        item2.set_expand(true);

        this.frame.set("label_widget", this.label);
        this.label.set_text(titulo);
        this.frame.set("label_xalign", 0.5);
        this.frame.set("label_yalign", 0.5);
        this.frame.set_border_width(4);

        Gtk.EventBox event = new Gtk.EventBox();
        event.set_border_width(4);
        event.add(this.escala);
        this.frame.add(event);
        this.frame.show_all();

        item2.add(this.frame);
        this.insert(item2, -1);
        this.show_all();

        this.escala.user_set_value.connect(this.__user_set_value);
    }

    public void __user_set_value(double valor){
        if (valor > 99.4){
            valor = 100.0;
            }
        int v = (int) valor;
        string str1 = this.label.get_text();
	    string str2 = v.to_string();
	    string str3 = "%";
	    string text = @"$str1: $str2$str3";
        this.frame.set_label(text);
        this.user_set_value(valor);
        }

    public void set_progress(double valor){
        this.escala.set_progress(valor);
    }
}


public class SlicerBalance : Gtk.EventBox{

    public signal void user_set_value(double valor);

    private Gtk.Scale escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    public Gtk.Adjustment ajuste = new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0);

    public SlicerBalance(){

        this.escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, this.ajuste);
        this.escala.set_digits(0);
        this.escala.set_draw_value(false);

        this.add(this.escala);
        this.show_all();

        this.escala.value_changed.connect (() => {
			this.user_set_value(this.ajuste.get_value());
		});
    }

    public void set_progress(double valor){
        this.ajuste.set_value(valor);
        this.escala.queue_draw();
        }
}
