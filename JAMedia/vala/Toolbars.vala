
public class Toolbar : Gtk.EventBox{

    public signal void accion(string acc);
    public signal void credits();
    public signal void help();

    public Toolbar(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 3, false);
        toolbar.insert(separador1, -1);

        Gtk.ToolButton button1 = get_button("Iconos/JAMedia.svg", false, 35, "Creditos");
		button1.clicked.connect (() => {
			this.__emit_credits();
		});
		toolbar.insert(button1, -1);

        Gtk.ToolButton button2 = get_button("Iconos/JAMedia-help.svg", false, 24, "Ayuda");
		button2.clicked.connect (() => {
			this.__emit_help();
		});
		toolbar.insert(button2, -1);

        Gtk.ToolButton button3 = get_button("Iconos/configurar.svg", false, 24, "Configuraciones");
		button3.clicked.connect (() => {
			this.__emit_accion("show-config");
		});
		toolbar.insert(button3, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 0, true);
        toolbar.insert(separador2, -1);

        Gtk.ToolButton button4 = get_button("Iconos/button-cancel.svg", false, 24, "Salir");
		button4.clicked.connect (() => {
			this.__emit_accion("salir");
		});
		toolbar.insert(button4, -1);

        Gtk.SeparatorToolItem separador3 = get_separador(false, 3, false);
        toolbar.insert(separador3, -1);

        this.add(toolbar);
        this.show_all();
    }

    private void __emit_credits(){
        this.credits();
    }

    private void __emit_help(){
        this.help();
    }

    private void __emit_accion(string accion){
        this.accion(accion);
    }
}


public class ToolbarSalir : Gtk.EventBox{

    public signal void salir();
    private Gtk.Label label = new Gtk.Label("");

    public ToolbarSalir(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 0, true);
        toolbar.insert(separador1, -1);

        Gtk.ToolButton button1 = get_button("Iconos/button-cancel.svg", false, 24, "Cancelar");
		button1.clicked.connect (() => {
			this.cancelar();
		});
		toolbar.insert(button1, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 3, false);
        toolbar.insert(separador2, -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        label.show();
        item.add(this.label);
        toolbar.insert(item, -1);

        Gtk.SeparatorToolItem separador3 = get_separador(false, 3, false);
        toolbar.insert(separador3, -1);

        Gtk.ToolButton button2 = get_button("Iconos/dialog-ok.svg", false, 24, "Aceptar");
		button2.clicked.connect (() => {
			this.__emit_salir();
		});
		toolbar.insert(button2, -1);

        Gtk.SeparatorToolItem separador4 = get_separador(false, 0, true);
        toolbar.insert(separador4, -1);

        this.add(toolbar);
        this.show_all();
    }

    public void __emit_salir(){
        this.cancelar();
        this.salir();
        }

    public void run(string nombre_aplicacion){
        string text = string.join(" ", "¿Salir de", nombre_aplicacion, "?");
        this.label.set_text(text);
        this.show();
        }

    public void cancelar(){
        this.label.set_text("");
        this.hide();
        }
}
