

internal class MenuPrincipal : Gtk.MenuBar{

    public signal void accion(string accion);

    private MenuArchivo marchivo = new MenuArchivo();
    private MenuUtiles mutiles = new MenuUtiles();
    private MenuAyuda mayuda = new MenuAyuda();

    internal MenuPrincipal(){

        Gtk.MenuItem archivo = new Gtk.MenuItem();
        archivo.set_label("Archivo");
        archivo.set_submenu(this.marchivo);
        this.append(archivo);

        Gtk.MenuItem utiles = new Gtk.MenuItem();
        utiles.set_label("Utiles");
        utiles.set_submenu(this.mutiles);
        this.append(utiles);

        Gtk.MenuItem ayuda = new Gtk.MenuItem();
        ayuda.set_label("Ayuda");
        ayuda.set_submenu(this.mayuda);
        this.append(ayuda);

        this.show_all();

        this.marchivo.accion.connect ((accion) => {
            this.re_emit_accion(accion);
         });
        this.mutiles.accion.connect ((accion) => {
            this.re_emit_accion(accion);
         });
        this.mayuda.accion.connect ((accion) => {
            this.re_emit_accion(accion);
         });

        }

    private void re_emit_accion(string accion){
        this.accion(accion);
        }

    public void has_file(bool hasfile){
        this.marchivo.has_file(hasfile);
        this.mutiles.has_file(hasfile);
        }

    public void has_change(bool changed){
        this.marchivo.has_change(changed);
        }
    }


internal class MenuArchivo : Gtk.Menu{

    public signal void accion(string label);

    private Gtk.MenuItem abrir = new Gtk.MenuItem();
    private Gtk.MenuItem guardar = new Gtk.MenuItem();
    private Gtk.MenuItem guardar_como = new Gtk.MenuItem();
    private Gtk.MenuItem imprimir = new Gtk.MenuItem();
    private Gtk.MenuItem propiedades = new Gtk.MenuItem();
    private Gtk.MenuItem cerrar = new Gtk.MenuItem();

    internal MenuArchivo(){

        this.abrir.set_label("Abrir...");
        this.abrir.activate.connect ((source) => {
            this.emit_accion(this.abrir.get_label());
         });
        this.append(this.abrir);

        Gtk.SeparatorMenuItem separador1 = new Gtk.SeparatorMenuItem();
        this.append(separador1);

        this.guardar.set_label("Guardar");
        this.guardar.activate.connect ((source) => {
            this.emit_accion(this.guardar.get_label());
         });
        this.append(this.guardar);

        this.guardar_como.set_label("Guardar Como...");
        this.guardar_como.activate.connect ((source) => {
            this.emit_accion(this.guardar_como.get_label());
         });
        this.append(this.guardar_como);

        Gtk.SeparatorMenuItem separador2 = new Gtk.SeparatorMenuItem();
        this.append(separador2);

        this.imprimir.set_label("Imprimir...");
        this.imprimir.activate.connect ((source) => {
            this.emit_accion(this.imprimir.get_label());
         });
        this.append(this.imprimir);

        Gtk.SeparatorMenuItem separador3 = new Gtk.SeparatorMenuItem();
        this.append(separador3);

        this.propiedades.set_label("Propiedades...");
        this.propiedades.activate.connect ((source) => {
            this.emit_accion(this.propiedades.get_label());
         });
        this.append(this.propiedades);

        Gtk.SeparatorMenuItem separador4 = new Gtk.SeparatorMenuItem();
        this.append(separador4);

        this.cerrar.set_label("Cerrar");
        this.cerrar.activate.connect ((source) => {
            this.emit_accion(this.cerrar.get_label());
         });
        this.append(this.cerrar);

        this.show_all();
        }

    public void has_change(bool changed){
        this.guardar.set_sensitive(changed);
        }

    private void emit_accion(string label){
        this.accion(label);
        }

    public void has_file(bool hasfile){
        this.guardar_como.set_sensitive(hasfile);
        this.imprimir.set_sensitive(hasfile);
        this.propiedades.set_sensitive(hasfile);
        this.cerrar.set_sensitive(hasfile);
        }
    }


internal class MenuUtiles : Gtk.Menu{

    public signal void accion(string label);

    private Gtk.MenuItem canales = new Gtk.MenuItem();
    private Gtk.MenuItem grises = new Gtk.MenuItem();

    internal MenuUtiles(){

        this.canales.set_label("Canales...");
        this.canales.activate.connect ((source) => {
            this.emit_accion(this.canales.get_label());
         });
        this.append(this.canales);

        this.grises.set_label("Grises...");
        this.grises.activate.connect ((source) => {
            this.emit_accion(this.grises.get_label());
         });
        this.append(this.grises);

        this.show_all();
        }

    private void emit_accion(string label){
        this.accion(label);
        }

    public void has_file(bool hasfile){
        foreach(Gtk.Widget item in this.get_children()){
            item.set_sensitive(hasfile);
            }
        }

    }


internal class MenuAyuda : Gtk.Menu{

    public signal void accion(string label);

    internal MenuAyuda(){

        this.show_all();
        }

    }
