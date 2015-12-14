#include "JAMedia.h"

//using namespace std;


JAMedia::JAMedia(){
    set_title("JAMedia");
    try{set_icon_from_file("./Iconos/JAMedia.svg");}
    catch(const Glib::FileError& e){std::cout << e.what() << std::endl;}
    set_border_width(2); set_resizable(true);

    vol = 0.2;

    vbox = new Gtk::VBox();
    toolbar = new JToolbar();
    panel = new JPaned();
    progress = new Gtk::HScale(
        Gtk::Adjustment::create(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    progress->property_digits() = 0;
    controls = new Controls();

    vbox->pack_start(*toolbar, false, false, 0);
    vbox->pack_start(*panel, true, true, 0);

    Gtk::EventBox *event = new Gtk::EventBox();
    event->set_border_width(4);
    event->add(*progress);

    vbox->pack_start(*event, false, false, 0);
    vbox->pack_end(*controls, false, false, 0);

    add(*vbox);
    signal_realize().connect(sigc::mem_fun(*this, &JAMedia::init));
    progress->signal_adjust_bounds().connect(
        sigc::mem_fun(*this, &JAMedia::set_progress));
    show_all(); resize(640, 480);}

void JAMedia::init(){
    if (player != NULL){player->stop();delete player;player = NULL;}
    //FIXME: Mejorar esto?
    progress->set_sensitive(false);progress->set_value(0.0);
    controls->init();toolbar->video(false);panel->init();}

void JAMedia::toolbar_accion(Glib::ustring text, bool active){
    //Acciones en toolbar principal
    if (text == "Creditos"){}
    else if (text == "Ayuda"){}
    else if (text == "Izquierda" or text == "Derecha"){player->rotar(text);}
    //else if (text == "Controles"){}
    else if (text == "Balance"){panel->view_conf_or_list(text, active);}
    else if (text == "Fullscreen"){
        if (active){fullscreen(); set_border_width(0);}
        else {unfullscreen(); set_border_width(2);}}
    // Acciones sobre controles de reproducción
    else if (text == "Anterior"){previous_track();}
    else if (text == "Siguiente"){next_track();}
    else if (text == "Stop"){player->stop();controls->set_estado("paused");}
    else if (text == "Play"){player->pause_play();}
    else{std::cout << "Señal sin implementar para: ";
        std::cout << text << " " << active << std::endl;}}

void JAMedia::previous_track(){
    panel->previous_track();progress->set_value(0.0);}
void JAMedia::next_track(){panel->next_track();progress->set_value(0.0);}
void JAMedia::vol_changed(double value){vol = value; player->set_vol(vol);}

void JAMedia::motion(bool val){
    //Desplazamiento del mouse sobre drawingarea
    bool view = toolbar->get_view_controls();
    if (not view and not val){toolbar->hide(); progress->get_parent()->hide();
    controls->hide(); panel->list_view(false);}
    else if (not view and val){toolbar->show(); progress->get_parent()->show();
    controls->show();panel->list_view(true);}}

void JAMedia::open_files(){
    std::vector<std::basic_string<char> > lista = run_open_files();
    if (lista.size()){init(); panel->open_files(lista);
        panel->activar("clear, mas"); panel->select_begin();}}

void JAMedia::add_files(){
    std::vector<std::basic_string<char> > lista = run_open_files();
    if (lista.size()){panel->open_files(lista);}}

std::vector<std::basic_string<char> > JAMedia::run_open_files(){
    std::vector<std::basic_string<char> > lista;
    Gtk::FileChooserDialog dialog(*this, "Abrir Archivos",
        Gtk::FILE_CHOOSER_ACTION_OPEN);
    dialog.add_button("Abrir", Gtk::RESPONSE_OK);
    dialog.add_button("Cancelar", Gtk::RESPONSE_CANCEL);
    dialog.set_select_multiple(true); dialog.set_border_width(15);
    //FIXME: Agregar uri inicial
    //dialog.set_current_folder_uri("file://%s" % os.path.dirname(uri))

    Glib::RefPtr<Gtk::FileFilter> filter = Gtk::FileFilter::create();
    filter->set_name("Audio"); filter->add_mime_type("audio/*");
    dialog.add_filter(filter);

    filter = Gtk::FileFilter::create();
    filter->set_name("Videos"); filter->add_mime_type("video/*");
    filter->add_mime_type("application/vnd.rn-realmedia/*");
    dialog.add_filter(filter);

    //FIXME: Agregar lectura de playlist
    //https://es.wikipedia.org/wiki/XML_Shareable_Playlist_Format
    //https://es.wikipedia.org/wiki/M3U
    //https://wiki.videolan.org/PLS
    //filter = Gtk::FileFilter::create();
    //filter->set_name("Listas");
    //filter->add_mime_type("text/*");
    //dialog.add_filter(filter);

    int result = dialog.run();
    switch (result){
        case Gtk::RESPONSE_OK:lista = dialog.get_filenames(); break;}
    dialog.hide(); return lista;}

void JAMedia::set_progress(double val){player->seek_pos(gint64(val));}
void JAMedia::estado_update(Glib::ustring valor){controls->set_estado(valor);}
void JAMedia::progress_update(gint64 valor){progress->set_value(valor);}
void JAMedia::load_file(Glib::ustring track){
    if (player != NULL){player->stop();delete player;player = NULL;}
    toolbar->video(false); panel->new_file();progress->set_value(0.0);
    progress->set_sensitive(false);
    player = new JAMediaPlayer();player->set_vol(vol);controls->set_vol(vol);
    player->signal_end.connect(sigc::mem_fun(*this, &JAMedia::next_track));
    player->signal_progress_update.connect(
        sigc::mem_fun(*this, &JAMedia::progress_update));
    player->signal_estado_update.connect(
        sigc::mem_fun(*this, &JAMedia::estado_update));
    player->signal_video.connect(sigc::mem_fun(*this, &JAMedia::video));
    progress->set_sensitive(true); controls->set_sensitive(true); //FIXME: La sensibilidad de progress depende de la pista
    player->load(track, panel->get_xid()); player->play();}

void JAMedia::video(){toolbar->video(true); panel->video(true);}
void JAMedia::set_balance(Glib::ustring text, double val){
    if (player != NULL){player->set_balance(text, val);}}
