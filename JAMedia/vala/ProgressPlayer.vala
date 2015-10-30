
public class ProgressPlayer : Gtk.EventBox{

    public signal void volumen(double valor);
    public signal void seek(double valor);

    private BarraProgreso barraprogreso = new BarraProgreso();
    public ControlVolumen _volumen = new ControlVolumen();

    public ProgressPlayer(){

        Gtk.Box hbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
        hbox.pack_start(this.barraprogreso, true, true, 0);
        hbox.pack_start(this._volumen, false, false, 0);

        this.add(hbox);

        this.barraprogreso.user_set_value.connect(this.__user_set_value);
        this._volumen.volumen.connect(this.__set_volumen);

        this.show_all();
    }

    private void __user_set_value(double valor){
        this.seek(valor);
        }

    private void __set_volumen(double valor){
        this.volumen(valor);
        }

    public void set_progress(int64 valor){
        this.barraprogreso.set_progress(valor);
        }
}


public class BarraProgreso : Gtk.EventBox{

    public signal void user_set_value(double valor);

    private ProgressBar2 escala = new ProgressBar2();
    private double valor = 0.0;

    public BarraProgreso(){

        this.add(escala);
        this.show_all();

        this.escala.user_set_value.connect(this.__emit_valor);
        this.set_size_request(-1, 24);
    }

    private void __emit_valor(double valor){
        if (this.valor != valor){
            this.valor = valor;
            this.user_set_value(valor);
            }
        }

    public void set_progress(int64 valor){
        if (this.valor != valor){
            this.valor = valor;
            this.escala.ajuste.set_value((double) valor);
            this.escala.queue_draw();
            }
        }
}


public class ProgressBar2 : Gtk.EventBox{

    public signal void user_set_value(double valor);

    private Gtk.Scale escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    public Gtk.Adjustment ajuste = new Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0);

    public ProgressBar2(){

        this.set_border_width(4);
        this.escala = new Gtk.Scale(Gtk.Orientation.HORIZONTAL, this.ajuste);
        this.escala.set_digits(0);
        this.escala.set_draw_value(false);

        this.add(this.escala);
        this.show_all();

        this.escala.change_value.connect ((scroll, new_value) => {
			if (new_value < 0.0){
			    new_value = 0.0;
			    }
			if (new_value > 100.0){
			    new_value = 100.0;
			    }
			this.user_set_value(new_value);
			return false;
		});
    }
}


public class ControlVolumen : Gtk.VolumeButton{

    public signal void volumen(double valor);

    public ControlVolumen(){

        this.show_all();
        this.set_value(0.1);

        this.value_changed.connect ((valor) => {
            this.volumen(valor);
		    });
    }
}
