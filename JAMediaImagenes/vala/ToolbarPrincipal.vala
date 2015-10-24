

internal class ToolbarPrincipal : Gtk.Toolbar{

    public signal void accion(string accion);

    Gtk.ToolButton guardar = new Gtk.ToolButton.from_stock(Gtk.Stock.SAVE);
    Gtk.ToolButton guardar_como = new Gtk.ToolButton.from_stock(Gtk.Stock.SAVE_AS);
    Gtk.ToolButton zoom_in = new Gtk.ToolButton.from_stock(Gtk.Stock.ZOOM_IN);
    Gtk.ToolButton zoom_out = new Gtk.ToolButton.from_stock(Gtk.Stock.ZOOM_OUT);
    Gtk.ToolButton zoom_100 = new Gtk.ToolButton.from_stock(Gtk.Stock.ZOOM_100);
    Gtk.ToolButton zoom_fit = new Gtk.ToolButton.from_stock(Gtk.Stock.ZOOM_FIT);
    Gtk.ToolButton izquierda = new Gtk.ToolButton.from_stock(Gtk.Stock.UNDO);
    Gtk.ToolButton derecha = new Gtk.ToolButton.from_stock(Gtk.Stock.REDO);
    Gtk.ToolButton anterior = new Gtk.ToolButton.from_stock(Gtk.Stock.GO_BACK);
    Gtk.ToolButton siguiente = new Gtk.ToolButton.from_stock(Gtk.Stock.GO_FORWARD);

    internal ToolbarPrincipal(){

        Gtk.ToolButton abrir = new Gtk.ToolButton.from_stock(Gtk.Stock.OPEN);
        abrir.set_tooltip_text("Abrir");
        abrir.clicked.connect (() => {
            this.emit_accion("Abrir");
        });
        this.insert(abrir, -1);

        this.guardar.set_tooltip_text("Guardar");
        this.guardar.clicked.connect (() => {
            this.emit_accion("Guardar");
        });
        this.insert(this.guardar, -1);

        this.guardar_como.set_tooltip_text("Guardar Como");
        this.guardar_como.clicked.connect (() => {
            this.emit_accion("Guardar Como");
        });
        this.insert(this.guardar_como, -1);

        Gtk.SeparatorToolItem sep1 = new Gtk.SeparatorToolItem();
        this.insert(sep1, -1);

        this.zoom_in.set_tooltip_text("Acercar");
        this.zoom_in.clicked.connect (() => {
            this.emit_accion("Acercar");
        });
        this.insert(this.zoom_in, -1);

        this.zoom_out.set_tooltip_text("Alejar");
        this.zoom_out.clicked.connect (() => {
            this.emit_accion("Alejar");
        });
        this.insert(this.zoom_out, -1);

        this.zoom_100.set_tooltip_text("Ver tamaño original");
        this.zoom_100.clicked.connect (() => {
            this.emit_accion("Ver tamaño original");
        });
        this.insert(this.zoom_100, -1);

        this.zoom_fit.set_tooltip_text("Ocupar todo el espacio");
        this.zoom_fit.clicked.connect (() => {
            this.emit_accion("Ocupar todo el espacio");
        });
        this.insert(this.zoom_fit, -1);

        Gtk.SeparatorToolItem sep2 = new Gtk.SeparatorToolItem();
        this.insert(sep2, -1);

        this.izquierda.set_tooltip_text("Rotar a la izquierda");
        this.izquierda.clicked.connect (() => {
            this.emit_accion("Rotar a la izquierda");
        });
        this.insert(this.izquierda, -1);

        this.derecha.set_tooltip_text("Rotar a la derecha");
        this.derecha.clicked.connect (() => {
            this.emit_accion("Rotar a la derecha");
        });
        this.insert(this.derecha, -1);

        Gtk.SeparatorToolItem sep3 = new Gtk.SeparatorToolItem();
        this.insert(sep3, -1);

        this.anterior.set_tooltip_text("Ver imagen anterior");
        this.anterior.clicked.connect (() => {
            this.emit_accion("Ver imagen anterior");
        });
        this.insert(this.anterior, -1);

        this.siguiente.set_tooltip_text("Ver imagen siguiente");
        this.siguiente.clicked.connect (() => {
            this.emit_accion("Ver imagen siguiente");
        });
        this.insert(this.siguiente, -1);

        this.show_all();
        }

    private void emit_accion(string accion){
        this.accion(accion);
        }

    public void has_change(bool changed){
        this.guardar.set_sensitive(changed);
        }

    public void has_file(bool hasfile){
        this.guardar_como.set_sensitive(hasfile);
        this.zoom_in.set_sensitive(hasfile);
        this.zoom_out.set_sensitive(hasfile);
        this.zoom_100.set_sensitive(hasfile);
        this.zoom_fit.set_sensitive(hasfile);
        this.izquierda.set_sensitive(hasfile);
        this.derecha.set_sensitive(hasfile);
        }

    }
