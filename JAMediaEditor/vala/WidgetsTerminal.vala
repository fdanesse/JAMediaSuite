
public class ToolbarTerminal : Gtk.Toolbar{

    public ToolbarTerminal(){

        /*
        ### Interpretes disponibles.
        bash_path = None
        python_path = None

        paths = os.environ["PATH"].split(':')
        for path in paths:
            if 'bash' in os.listdir(path):
                bash_path = os.path.join(path, 'bash')

            if 'python' in os.listdir(path):
                python_path = os.path.join(path, 'python')

            if bash_path and python_path:
                break

        for path in paths:
            if 'ipython' in os.listdir(path):
                python_path = os.path.join(path, 'ipython')
        */

        Gtk.ToolButton button1 = get_button("Iconos/edit-copy.svg", false, Gdk.PixbufRotation.NONE, 18, "Copiar");
		//button1.clicked.connect (() => {
		//	this.accion("Copiar");
		//    });
		this.insert(button1, -1);

        Gtk.ToolButton button2 = get_button("Iconos/editpaste.svg", false, Gdk.PixbufRotation.NONE, 18, "Pegar");
		//button2.clicked.connect (() => {
		//	this.accion("Pegar");
		//    });
		this.insert(button2, -1);

        this.insert(get_separador(false, 0, true), - 1);

        Gtk.ToolButton button3 = get_button("Iconos/font.svg", false, Gdk.PixbufRotation.NONE, 18, "Fuente");
		//button3.clicked.connect (() => {
		//	this.accion("Fuente");
		//    });
		this.insert(button3, -1);

        Gtk.ToolButton button4 = get_button("Iconos/tab-new.svg", false, Gdk.PixbufRotation.NONE, 18, "Nueva Terminal");
		//button4.clicked.connect (() => {
		//	this.accion("Nueva Terminal");
		//    });
		this.insert(button4, -1);

        this.insert(get_separador(false, 10, false), - 1);

        Gtk.ToolButton button5 = get_button("Iconos/bash.svg", false, Gdk.PixbufRotation.NONE, 18, "Terminal bash");
		//button5.clicked.connect (() => {
		//	this.accion("Terminal bash");
		//    });
		this.insert(button5, -1);

        Gtk.ToolButton button6 = get_button("Iconos/python.svg", false, Gdk.PixbufRotation.NONE, 18, "Terminal python");
		//button6.clicked.connect (() => {
		//	this.accion("Terminal python");
		//    });
		this.insert(button6, -1);

        this.show_all();
    }
}
