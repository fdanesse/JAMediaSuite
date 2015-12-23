#include "JTreeView.h"
#include "../JAMedia.h"

//using namespace std;


JTreeView::JTreeView(){

    listore = Gtk::ListStore::create(cols);

    append_column("", cols.pix);
    append_column("Pista", cols.name);
    append_column("Path", cols.path);

    //set_activate_on_single_click(true);
    set_headers_clickable(true);
    set_enable_search(true);
    set_rules_hint(true);
    set_search_column(1);
    get_column(1)->set_sort_column(cols.name);
    get_column(2)->set_visible(false);
    //get_column(0)->set_reorderable(); Reordenar columnas

    set_model(listore);
    show_all();

    sel = get_selection();
    sel->set_mode(Gtk::SELECTION_SINGLE);
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
        if (selected == process){
            next_track();}
        listore->erase(iter);
        Gtk::TreeModel::iterator iter = sel->get_selected();
        if (not iter){
            top->init();}}

    else if (text == "Borrar"){
        Gtk::Dialog dialog("Borrar Archivo", *top, true);
        dialog.add_button("Borrar", Gtk::RESPONSE_OK);
        dialog.add_button("Cancelar", Gtk::RESPONSE_CANCEL);
        dialog.set_border_width(15);
        Gtk::Label *label = new Gtk::Label(
            "¿Eliminar Este Archivo Definitivamente?");
        dialog.get_vbox()->pack_start(*label, false, false, 0);
        dialog.get_vbox()->show_all();
        int result = dialog.run();
        switch (result){
            case Gtk::RESPONSE_OK:{
                if (selected == process){
                    next_track();}
                delete_file(process);
                listore->erase(iter);
                Gtk::TreeModel::iterator iter3 = sel->get_selected();
                if (not iter3){
                    top->init();}
                break;}
        delete label;
        dialog.hide();}}

    else if (text == "Copiar"){
        save_file(process, text);}

    else if (text == "Mover"){
        if (selected == process){
            next_track();}
        save_file(process, text);listore->erase(iter);
        Gtk::TreeModel::iterator iter3 = sel->get_selected();
        if (not iter3){
            top->init();}}

    else if (text == "Subtitulos"){
        top->load_sub();}

    else if (text == "Grabar"){
        std::cout << "Grabar/Convertir/Extraer: " << process << std::endl;}
        //FIXME: Grabar/Convertir/Extraer en el directorio seleccionado
}

void JTreeView::delete_file(Glib::ustring process){
    Glib::RefPtr<Gio::File> giofile =
        Gio::File::create_for_parse_name(process);
    if (giofile->trash()){
        std::cout << "ARCHIVO ELIMINADO: " << process << std::endl;}
    else{
        std::cout << "ERROR al intentar borrar: " << process << std::endl;}}
    //if (std::ifstream(process.c_str())){
    //    if (std::remove(process.c_str()) != 0){
    //        std::cout << "ERROR al intentar borrar: " << process << std::endl;}
    //    else {std::cout << "ARCHIVO ELIMINADO: " << process << std::endl; }}}
    //FIXME: Si falla borrar, es un track en un archivo de lista de reproduccion (pls, meu, etc)

void JTreeView::save_file(Glib::ustring process, Glib::ustring accion){
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    Gtk::FileChooserDialog dialog(*top, accion + " Archivo",
    Gtk::FILE_CHOOSER_ACTION_SAVE);
    dialog.add_button(accion, Gtk::RESPONSE_OK);
    dialog.add_button("Cancelar", Gtk::RESPONSE_CANCEL);
    dialog.set_do_overwrite_confirmation(true);
    dialog.set_border_width(15);
    dialog.set_filename(process);
    Glib::RefPtr<Gio::File> giofile =
        Gio::File::create_for_parse_name(process);
    Glib::RefPtr<Gio::FileInfo> info;
    info = giofile->query_info();
    Glib::ustring tipo = info->get_content_type();
    Glib::RefPtr<Gtk::FileFilter> filter = Gtk::FileFilter::create();
    size_t found = tipo.find("audio");
    if (found!=std::string::npos){
        filter = Gtk::FileFilter::create();
        filter->set_name("Audio");
        filter->add_mime_type("audio/*");
        dialog.add_filter(filter);}
    found = tipo.find("video");
    if (found!=std::string::npos){
        filter = Gtk::FileFilter::create();
        filter->set_name("Videos");
        filter->add_mime_type("video/*");
        dialog.add_filter(filter);}
    Glib::ustring destino = "";
    int result = dialog.run();
    switch (result){case Gtk::RESPONSE_OK:
    destino = dialog.get_filename().c_str(); break;} dialog.hide();
    if (destino != ""){
        Glib::RefPtr<Gio::File> giodest =
            Gio::File::create_for_parse_name(destino);
        if (accion == "Copiar"){
            if (not giofile->copy(giodest)){
                std::cout << "ERROR al Copiar: " << process;
                std::cout << " en: " << destino << std::endl;}}
        else if (accion == "Mover"){
            if (not giofile->move(giodest)){
                std::cout << "ERROR al Mover: " << process;
                std::cout << " en: " << destino << std::endl;}}
        else{
            std::cout << accion << std::endl;}
        }}
    //if (destino != ""){std::FILE *f1 = std::fopen(process.c_str(), "rb");
    //    std::FILE *f2 = std::fopen(destino.c_str(), "wb");
    //    if (f1 != NULL and f2 != NULL){unsigned int c;
    //        while(!std::feof(f1)){c = std::getc(f1); std::fputc(c, f2);}}
    //    std::fclose(f1); std::fclose(f2);return destino;}}

bool JTreeView::on_button_press_event(GdkEventButton *event){
    //click izq selecciona, der menu contextual.
    Gtk::TreeModel::Path path;
    Gtk::TreeViewColumn *column;
    int cell_x;
    int cell_y;
    get_path_at_pos(event->x, event->y, path, column, cell_x, cell_y);
    Gtk::TreeModel::iterator iter = listore->get_iter(path);
    if ((event->type == GDK_BUTTON_PRESS) && (event->button == 1)){
        sel->select(iter);
        row_activated(listore->get_path(iter), get_column(0));
        scroll_to_row(listore->get_path(iter));
        return true;}
    else if ((event->type == GDK_BUTTON_PRESS) && (event->button == 3)){
        Gtk::TreeModel::Row row = *listore->get_iter(path);
        Glib::RefPtr<Gio::File> giofile =
            Gio::File::create_for_parse_name(row[cols.path]);
        bool video = false;
        if(giofile->query_exists()){
            Glib::ustring tipo = giofile->query_info()->get_content_type();
            size_t found = tipo.find("video");
            if (found != std::string::npos){
                video = true;}}
        JMenu *menu = new JMenu(path, giofile->query_exists(), video);
        menu->attach_to_widget(*this);
        menu->popup(event->button, event->time);
        return true;}
    else {
        return false;}}

void JTreeView::select_begin(){
    //Gtk::TreeModel::Row row = listore->children()[0];
    //if(row) sel->select(row);
    Gtk::TreeModel::iterator iter = listore->children().begin();
    if (iter){
        sel->select(iter);
        row_activated(listore->get_path(iter), get_column(0));
        scroll_to_row(listore->get_path(iter));}}

void JTreeView::select_end(){
    Gtk::TreeModel::iterator iter = listore->children().end();
    Gtk::TreeModel::Row row = *(--iter);
    if (row){
        sel->select(iter);
        row_activated(listore->get_path(iter), get_column(0));
        scroll_to_row(listore->get_path(iter));}}

void JTreeView::previous_track(){
    Gtk::TreeModel::iterator iter = sel->get_selected();
    if (iter){
        Gtk::TreeModel::Row row = *(--iter);
        if (row){
            sel->select(iter);
            row_activated(listore->get_path(iter), get_column(0));
            scroll_to_row(listore->get_path(iter));}
        else{
            select_end();}}}

void JTreeView::next_track(){
    Gtk::TreeModel::iterator iter = sel->get_selected();
    if (iter){
        Gtk::TreeModel::Row row = *(++iter);
        if (row){
            sel->select(iter);
            row_activated(listore->get_path(iter), get_column(0));
            scroll_to_row(listore->get_path(iter));}
        else{
            select_begin();}}}

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
    if (iter){
        Gtk::TreeModel::Row row = *iter;
        JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
        top->load_file(row[cols.path]);}}

void JTreeView::clear_list(){
    listore->clear();}

void JTreeView::open_files(std::vector<std::basic_string<char> > lista){
    //Recibe una lista de archivos que pueden ser archivos de audio y/o video
    //o un archivo de lista de reproducción en formato pls, m3u, etc...
    for(int i = 0; i < lista.size(); i++){
        std::basic_string<char> path = lista[i];
        Glib::ustring name = basename(path.c_str());
        size_t ext = name.find(".pls"); //FIXME: m3u, json, JAMedia
        if (ext != std::string::npos){
            pls_read(path);}
        else{
            append_file_track(path);}}}

void JTreeView::pls_read(std::basic_string<char> path){
    std::basic_string<char> line;
    std::ifstream archivo;
    archivo.open(path.c_str());
    if (archivo.is_open()){
        Glib::ustring title;
        Glib::ustring track;
        while(std::getline(archivo, line)){
            size_t pos_tag = line.find("File");
            if (pos_tag != std::string::npos){
                track = line.substr(line.find("=")+1);}
            else{
                pos_tag = line.find("Title");
                if (pos_tag != std::string::npos){
                    title = line.substr(line.find("=")+1);}}
            if (not title.empty() and not track.empty()){
                //FIXME: quitar espacios y tabulaciones, comillas, etc.
                Glib::RefPtr<Gio::File> giofile =
                    Gio::File::create_for_parse_name(path);
                if (giofile->query_exists() or gst_uri_is_valid(path.c_str())){
                    Gtk::TreeModel::Row row = *(listore->append());
                    Glib::ustring icon = "./Iconos/sonido.svg";
                    Glib::RefPtr<Gdk::Pixbuf> pixbuf =
                        Gdk::Pixbuf::create_from_file(icon);
                    pixbuf = pixbuf->scale_simple(24, 24, Gdk::INTERP_BILINEAR);
                    row[cols.pix] = pixbuf;row[cols.name] = title;
                    row[cols.path] = track;}
                track.clear();
                title.clear();}}
        archivo.close();}}

void JTreeView::append_file_track(std::basic_string<char> path){
    //recibe el path a un archivo.
    Gtk::TreeModel::Row row = *(listore->append());
    Glib::ustring icon = "./Iconos/sonido.svg";
    Glib::RefPtr<Gdk::Pixbuf> pixbuf = Gdk::Pixbuf::create_from_file(icon);
    pixbuf = pixbuf->scale_simple(24, 24, Gdk::INTERP_BILINEAR);
    Glib::RefPtr<Gio::File> giofile = Gio::File::create_for_parse_name(path);
    //Glib::RefPtr<Gio::FileInfo> info;
    Glib::ustring tipo = giofile->query_info()->get_content_type();
    Glib::ustring name = basename(path.c_str());
    try{//FIXME: Agregar "application/vnd.rn-realmedia/*"
        size_t found = tipo.find("video");
        if (found != std::string::npos){
            icon = "./Iconos/video.svg";
            pixbuf = Gdk::Pixbuf::create_from_file(icon);
            pixbuf = pixbuf->scale_simple(24, 24, Gdk::INTERP_BILINEAR);
            row[cols.pix] = pixbuf;}}
    catch(const Glib::FileError& e){
        std::cout << e.what() << std::endl;
        row[cols.pix] = pixbuf;}
    row[cols.name] = name;
    row[cols.path] = path.c_str();}
