#include "JTreeView.h"
#include "../JAMedia.h"

//using namespace std;


JTreeView::JTreeView(){

    listore = Gtk::ListStore::create(cols);

    append_column("", cols.pix);
    append_column("Pista", cols.name);
    append_column("Path", cols.path);

    //set_activate_on_single_click(true);
    set_headers_clickable(true);set_enable_search(true);
    set_rules_hint(true);set_search_column(1);
    get_column(1)->set_sort_column(cols.name);
    get_column(2)->set_visible(false);
    //get_column(0)->set_reorderable(); Reordenar columnas

    set_model(listore);show_all();

    sel = get_selection(); sel->set_mode(Gtk::SELECTION_SINGLE);
    //sel->set_select_function(
    //  sigc::mem_fun(*this, &JTreeView::select_function) );
    signal_row_activated().connect(
        sigc::mem_fun(*this, &JTreeView::row_activated));}

void JTreeView::accion_menu(Glib::ustring text, Gtk::TreePath path){
    Gtk::TreeModel::iterator iter = listore->get_iter(path);
    Gtk::TreeModel::Row row = *iter;
    Gtk::TreeModel::iterator iter2 = sel->get_selected();
    Gtk::TreeModel::Row row2 = *iter2;
    Glib::ustring selected = row2[cols.path];
    Glib::ustring process = row[cols.path];
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());

    if (text == "Quitar"){
        if (selected == process){next_track();}
        listore->erase(iter);
        Gtk::TreeModel::iterator iter = sel->get_selected();
        if (not iter){top->init();}}

    else if (text == "Borrar"){
        Gtk::Dialog dialog("Borrar Archivo", *top, true);
        dialog.add_button("Borrar", Gtk::RESPONSE_OK);
        dialog.add_button("Cancelar", Gtk::RESPONSE_CANCEL);
        dialog.set_border_width(15);
        Gtk::Label *label = new Gtk::Label(
            "¿Eliminar Este Archivo Definitivamente?");
        dialog.get_vbox()->pack_start(*label, false, false, 0);
        dialog.get_vbox()->show_all();int result = dialog.run();

        switch (result){
            case Gtk::RESPONSE_OK:{
                if (selected == process){next_track();}
                delete_file(process);
                listore->erase(iter);
                Gtk::TreeModel::iterator iter3 = sel->get_selected();
                if (not iter3){top->init();}
                break;}
        delete label; dialog.hide();}}

    else if (text == "Guardar"){Glib::ustring destino = save_file(process);}
    else if (text == "Mover"){Glib::ustring destino = save_file(process);
        if (destino != ""){delete_file(process);row[cols.path] = destino;}} //FIXME: antes lo quitabamos de la lista
    else if (text == "Grabar"){}
        //FIXME: Grabar/Convertir/Extraer en el directorio seleccionado
}

void JTreeView::delete_file(Glib::ustring process){
    if (std::ifstream(process.c_str())){
        if (std::remove(process.c_str()) != 0){
            std::cout << "ERROR al intentar borrar: " << process << std::endl;}
        else {std::cout << "ARCHIVO ELIMINADO: " << process << std::endl; }}}
    //FIXME: Si falla borrar, es un track en un archivo de lista de reproduccion (pls, meu, etc)

Glib::ustring JTreeView::save_file(Glib::ustring process){
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    Gtk::FileChooserDialog dialog(*top, "Guardar Archivo",
    Gtk::FILE_CHOOSER_ACTION_SAVE);
    dialog.add_button("Guardar", Gtk::RESPONSE_OK);
    dialog.add_button("Cancelar", Gtk::RESPONSE_CANCEL);
    dialog.set_do_overwrite_confirmation(true);
    dialog.set_border_width(15); dialog.set_filename(process);
    Glib::RefPtr<Gio::File> gioFile; Glib::RefPtr<Gio::FileInfo> info;
    gioFile = Gio::File::create_for_path(process);
    info = gioFile->query_info();
    Glib::ustring tipo = info->get_content_type();
    std::cout << tipo << std::endl;
    Glib::RefPtr<Gtk::FileFilter> filter = Gtk::FileFilter::create();
    size_t found = tipo.find("audio");
    if (found!=std::string::npos){filter = Gtk::FileFilter::create();
        filter->set_name("Audio"); filter->add_mime_type("audio/*");
        dialog.add_filter(filter);}
    found = tipo.find("video");
    if (found!=std::string::npos){filter = Gtk::FileFilter::create();
        filter->set_name("Videos"); filter->add_mime_type("video/*");
        dialog.add_filter(filter);}
    found = tipo.find("vnd.rn-realmedia");
    if (found!=std::string::npos){filter = Gtk::FileFilter::create();
        filter->set_name("Videos");
        filter->add_mime_type("application/vnd.rn-realmedia/*");
        dialog.add_filter(filter);}
    Glib::ustring destino = ""; int result = dialog.run();
    switch (result){case Gtk::RESPONSE_OK:
    destino = dialog.get_filename().c_str(); break;} dialog.hide();
    if (destino != ""){std::FILE *f1 = std::fopen(process.c_str(), "rb");
        std::FILE *f2 = std::fopen(destino.c_str(), "wb");
        if (f1 != NULL and f2 != NULL){unsigned int c;
            while(!std::feof(f1)){c = std::getc(f1); std::fputc(c, f2);}}
        std::fclose(f1); std::fclose(f2); return destino;}}

bool JTreeView::on_button_press_event(GdkEventButton *event){
    //click izq selecciona, der menu contextual.
    Gtk::TreeModel::Path path; Gtk::TreeViewColumn *column;
    int cell_x; int cell_y;
    get_path_at_pos(event->x, event->y, path, column, cell_x, cell_y);
    Gtk::TreeModel::iterator iter = listore->get_iter(path);
    if ((event->type == GDK_BUTTON_PRESS) && (event->button == 1)){
        sel->select(iter);
        row_activated(listore->get_path(iter), get_column(0));return true;}
    else if ((event->type == GDK_BUTTON_PRESS) && (event->button == 3)){
        JMenu *menu = new JMenu(path);menu->attach_to_widget(*this);
        menu->popup(event->button, event->time);return true;}
    else {return false;}}

void JTreeView::select_begin(){
    //Gtk::TreeModel::Row row = listore->children()[0];
    //if(row) sel->select(row);
    Gtk::TreeModel::iterator iter = listore->children().begin();
    if (iter){sel->select(iter);
        row_activated(listore->get_path(iter), get_column(0));}}

void JTreeView::select_end(){
    Gtk::TreeModel::iterator iter = listore->children().end();
    Gtk::TreeModel::Row row = *(--iter);
    if (row){sel->select(iter);
        row_activated(listore->get_path(iter), get_column(0));}}

void JTreeView::previous_track(){
    Gtk::TreeModel::iterator iter = sel->get_selected();
    if (iter){
        Gtk::TreeModel::Row row = *(--iter);
        if (row){
            sel->select(iter);
            row_activated(listore->get_path(iter), get_column(0));}
        else{select_end();}}}

void JTreeView::next_track(){
    Gtk::TreeModel::iterator iter = sel->get_selected();
    if (iter){
        Gtk::TreeModel::Row row = *(++iter);
        if (row){
            sel->select(iter);
            row_activated(listore->get_path(iter), get_column(0));}
        else{select_begin();}}}

//bool JTreeView::select_function(const Glib::RefPtr<Gtk::TreeModel>& model,
//      const Gtk::TreeModel::Path& path, bool dat){
// A partir de la segunda vez, se ejecuta 4 veces en cada selección.
//    const Gtk::TreeModel::iterator iter = model->get_iter(path);
//    if (iter){
//        Gtk::TreeModel::Row row = *iter;
//        std::cout << dat << " Name= " << row[cols.name] << " ";
//        std::cout << "Path= " << row[cols.path] << std::endl;}
//        scroll_to_cell(path);
//    return true;}

void JTreeView::row_activated(const Gtk::TreePath &path,
    Gtk::TreeViewColumn* col){
    //Doble click sobre un elemento
    Gtk::TreeModel::iterator iter = listore->get_iter(path);
    if (iter){Gtk::TreeModel::Row row = *iter;
        JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
        top->load_file(row[cols.path]);}} //FIXME: scroll_to_cell(&path, &col);

void JTreeView::clear_list(){listore->clear();}

void JTreeView::open_files(std::vector<std::basic_string<char> > lista){
    //Agrega pistas a la lista
    Gtk::TreeModel::Row row; Glib::RefPtr<Gdk::Pixbuf> pixbuf;
    Glib::ustring icon = "./Iconos/sonido.svg";
    Glib::RefPtr<Gio::File> gioFile; Glib::RefPtr<Gio::FileInfo> info;
    Glib::ustring tipo;
    for(int i = 0; i < lista.size(); i++){
        std::basic_string<char> path = lista[i];
        Glib::ustring name = basename(path.c_str());
        Glib::ustring rpath = path.c_str();
        gioFile = Gio::File::create_for_path(rpath);
        info = gioFile->query_info();
        tipo = info->get_content_type(); row = *(listore->append());
        try{size_t found = tipo.find("audio");
            if (found!=std::string::npos){icon = "./Iconos/sonido.svg";}
            else {found = tipo.find("video");
                //FIXME: Agregar "application/vnd.rn-realmedia/*"
                if (found!=std::string::npos){icon = "./Iconos/video.svg";}
                else{icon = "./Iconos/sonido.svg";
                    std::cout << "FIXME: Nuevo tipo de archivo ";
                    std::cout << (found!=std::string::npos);
                    std::cout << " " << tipo << std::endl;}}
            pixbuf = Gdk::Pixbuf::create_from_file(icon);
            pixbuf = pixbuf->scale_simple(24, 24, Gdk::INTERP_BILINEAR);
            row[cols.pix] = pixbuf;}
        catch(const Glib::FileError& e){std::cout << e.what() << std::endl;
            row[cols.pix] = pixbuf;}
        row[cols.name] = name; row[cols.path] = rpath;}}
