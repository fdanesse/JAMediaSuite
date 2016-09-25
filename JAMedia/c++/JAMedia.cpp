#include "JAMedia.h"

//using namespace std;


JAMedia::JAMedia(){

    set_title("JAMedia");
    try{
        set_icon_from_file("./Iconos/JAMedia.svg");}
    catch(const Glib::FileError& e){
        std::cout << e.what() << std::endl;}
    set_border_width(2); set_resizable(true);

    vol = 0.2;
    default_dirpath = std::getenv("HOME");

    Glib::RefPtr<Gdk::Pixbuf> pixbuf =
        Gdk::Pixbuf::create_from_file("./Iconos/jamedia_cursor.svg");
    pixbuf = pixbuf->scale_simple(24, 24, Gdk::INTERP_BILINEAR);
    Glib::RefPtr< Gdk::Display > display = Gdk::Display::get_default();
    jamedia_cursor = Gdk::Cursor::create(display, pixbuf, 0, 0);
    cursor_blank = Gdk::Cursor::create(display, Gdk::BLANK_CURSOR);

    vbox = new Gtk::VBox();
    toolbar = new JToolbar();
    panel = new JPaned();
    progress = new Gtk::HScale(
        Gtk::Adjustment::create(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    progress->set_draw_value(false);
    controls = new Controls();

    vbox->pack_start(*toolbar, false, false, 0);
    vbox->pack_start(*panel, true, true, 0);

    Gtk::EventBox *event = new Gtk::EventBox();
    event->set_border_width(4);
    event->add(*progress);

    vbox->pack_start(*event, false, false, 0);
    vbox->pack_end(*controls, false, false, 0);

    add(*vbox);
    signal_realize().connect(sigc::mem_fun(*this, &JAMedia::do_realize));
    progress->signal_adjust_bounds().connect(
        sigc::mem_fun(*this, &JAMedia::set_progress));
    show_all();
    resize(640, 480);

    time_t t = time(0);
    struct tm *now = localtime(&t);
    mov = (now->tm_hour * 60 * 60) + (now->tm_min * 60) + now->tm_sec;

    signal_motion_notify_event().connect(
        sigc::mem_fun(*this, &JAMedia::do_motion));
    Glib::signal_timeout().connect(
        sigc::mem_fun(*this, &JAMedia::set_mouse), 1000);

    std::cout << "JAMedia Process: " << getpid() << std::endl;
    }

bool JAMedia::set_mouse(){
    time_t t = time(0);
    struct tm *now = localtime(&t);
    int tiempo = (now->tm_hour * 60 * 60) + (now->tm_min * 60) + now->tm_sec;
    if (tiempo - mov > 2){
        get_window()->set_cursor(cursor_blank);}
    return true;}

bool JAMedia::do_motion(const GdkEventMotion *event){
    time_t t = time(0);
    struct tm *now = localtime(&t);
    mov = (now->tm_hour * 60 * 60) + (now->tm_min * 60) + now->tm_sec;
    get_window()->set_cursor(jamedia_cursor);
    return true;}

void JAMedia::do_realize(){
    get_window()->set_cursor(jamedia_cursor);
    init();}

void JAMedia::init(){
    if (player != NULL){
        player->stop();delete player;player = NULL;}
    progress->set_sensitive(false);
    progress->set_value(0.0);
    controls->init();
    toolbar->video(false);
    panel->init();}

void JAMedia::toolbar_accion(Glib::ustring text, bool active){
    //Acciones en toolbar principal
    if (text == "Creditos"){
        }

    else if (text == "Ayuda"){
        }

    else if (text == "Izquierda" or text == "Derecha"){
        player->rotar(text);}

    else if (text == "Lista"){
        panel->list_view(active);}

    //else if (text == "Controles"){}

    else if (text == "Balance"){
        panel->view_conf_or_list(text, active);}

    else if (text == "Fullscreen"){
        if (active){
            fullscreen();
            set_border_width(0);}
        else {
            unfullscreen();
            set_border_width(2);}}

    // Acciones sobre controles de reproducción
    else if (text == "Anterior"){
        previous_track();}

    else if (text == "Siguiente"){
        next_track();}

    else if (text == "Stop"){
        player->stop();
        controls->set_estado("paused");}

    else if (text == "Play"){
        player->pause_play();}

    else{
        std::cout << "Señal sin implementar para: ";
        std::cout << text << " " << active << std::endl;}}

void JAMedia::previous_track(){
    panel->previous_track();
    progress->set_value(0.0);}

void JAMedia::next_track(){
    panel->next_track();
    progress->set_value(0.0);}

void JAMedia::vol_changed(double value){
    vol = value; player->set_vol(vol);}

void JAMedia::motion(bool val){
    //Desplazamiento del mouse sobre drawingarea
    time_t t = time(0);
    struct tm *now = localtime(&t);
    mov = (now->tm_hour * 60 * 60) + (now->tm_min * 60) + now->tm_sec;
    get_window()->set_cursor(jamedia_cursor);
    bool view = toolbar->get_view_controls();
    bool vlis = toolbar->get_view_list();
    if (not view and not val){
        toolbar->hide();
        progress->get_parent()->hide();
        controls->hide();
        panel->list_view(false);}
    else if (not view and val){
        toolbar->show();
        progress->get_parent()->show();
        controls->show();
        panel->list_view(vlis);}}

void JAMedia::open_files(){
    std::vector<std::basic_string<char> > lista = run_open_files();
    if (lista.size()){
        init();
        panel->open_files(lista);
        panel->activar("clear, mas");
        panel->select_begin();}}

void JAMedia::add_files(){
    std::vector<std::basic_string<char> > lista = run_open_files();
    if (lista.size()){
        panel->open_files(lista);}}

std::vector<std::basic_string<char> > JAMedia::run_open_files(){
    std::vector<std::basic_string<char> > lista;
    Gtk::FileChooserDialog dialog(*this, "Abrir Archivos",
        Gtk::FILE_CHOOSER_ACTION_OPEN);
    dialog.add_button("Abrir", Gtk::RESPONSE_OK);
    dialog.add_button("Cancelar", Gtk::RESPONSE_CANCEL);
    dialog.set_select_multiple(true);
    dialog.set_border_width(15);
    dialog.set_current_folder_uri("file://" + default_dirpath);
    Glib::RefPtr<Gtk::FileFilter> filter = Gtk::FileFilter::create();
    filter->set_name("Video");
    filter->add_mime_type("video/*");
    filter->add_pattern("*.mpg");
    filter->add_pattern("*.mp4");
    filter->add_pattern("*.mkv");
    filter->add_pattern("*.avi");
    filter->add_pattern("*.mpeg");
    filter->add_pattern("*.rmvb");
    filter->add_pattern("*.ogg");
    filter->add_pattern("*.ogv");
    dialog.add_filter(filter);
    filter = Gtk::FileFilter::create();
    filter->set_name("Audio");
    filter->add_mime_type("audio/*");
    //FIXME: Probar con diferentes formatos. filter->add_mime_type("application/vnd.rn-realmedia/*");
    dialog.add_filter(filter);
    int result = dialog.run();
    switch (result){
        case Gtk::RESPONSE_OK:
            lista = dialog.get_filenames();
            break;}
    dialog.hide();
    if (lista.size()){
        Glib::ustring path = lista[0].c_str();
        default_dirpath = path.substr(0, path.find_last_of('/'));}
    return lista;}

void JAMedia::set_progress(double val){
    player->seek_pos(gint64(val));}

void JAMedia::estado_update(Glib::ustring valor){
    controls->set_estado(valor);}

void JAMedia::progress_update(gint64 valor){
    progress->set_value(valor);}

void JAMedia::load_file(Glib::ustring track){
    if (player != NULL){
        player->stop();
        delete player;
        player = NULL;}
    toolbar->video(false);
    panel->new_file();
    progress->set_value(0.0);
    Glib::RefPtr<Gio::File> giofile = Gio::File::create_for_parse_name(track);
    progress->set_sensitive(giofile->query_exists());
    player = new JAMediaPlayer();
    player->set_vol(vol);
    controls->set_vol(vol);
    player->signal_end.connect(sigc::mem_fun(*this, &JAMedia::next_track));
    player->signal_progress_update.connect(
        sigc::mem_fun(*this, &JAMedia::progress_update));
    player->signal_estado_update.connect(
        sigc::mem_fun(*this, &JAMedia::estado_update));
    player->signal_video.connect(sigc::mem_fun(*this, &JAMedia::video));
    //player->signal_info_update.connect(sigc::mem_fun(*this, &JAMedia::info));
    controls->set_sensitive(true);
    player->load(track, panel->get_xid());
    player->play();}

void JAMedia::video(){
    toolbar->video(true);
    panel->video(true);}

//void JAMedia::info(Glib::ustring info){
//    panel->set_info(info);}

void JAMedia::set_balance(Glib::ustring text, double val){
    if (player != NULL){
        player->set_balance(text, val);}}

void JAMedia::load_sub(){
    Glib::ustring file;
    Gtk::FileChooserDialog dialog(*this, "Cargar Subtítulos",
        Gtk::FILE_CHOOSER_ACTION_OPEN);
    dialog.add_button("Abrir", Gtk::RESPONSE_OK);
    dialog.add_button("Cancelar", Gtk::RESPONSE_CANCEL);
    dialog.set_select_multiple(false);
    dialog.set_border_width(15);
    dialog.set_current_folder_uri("file://" + default_dirpath);
    Glib::RefPtr<Gtk::FileFilter> filter = Gtk::FileFilter::create();
    filter->set_name("Texto");
    filter->add_mime_type("text/*");
    dialog.add_filter(filter);
    int result = dialog.run();
    switch (result){
        case Gtk::RESPONSE_OK:
            file = dialog.get_filename();
            break;}
    dialog.hide();
    if (file.size()){
        default_dirpath = file.substr(0, file.find_last_of('/'));}
    player->load_sub(file);}
