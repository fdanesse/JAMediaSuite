#include "../JAMedia.h"
#include "Controls.h"

//using namespace std;


Controls::Controls(){

    pixbufplay = Gdk::Pixbuf::create_from_file("./Iconos/pausa.svg");
    pixbufplay = pixbufplay->scale_simple(24, 24, Gdk::INTERP_BILINEAR);
    pixbufpause = Gdk::Pixbuf::create_from_file("./Iconos/play.svg");
    pixbufpause = pixbufpause->scale_simple(24, 24, Gdk::INTERP_BILINEAR);

    {
        Gtk::SeparatorToolItem *sep = new Gtk::SeparatorToolItem();
        sep->set_draw(false);
        sep->set_expand(true);
        insert(*sep, -1);
    }

    ant = new Gtk::ToolButton(
        *Controls::get_imagen("./Iconos/siguiente.svg", true), "");
    ant->set_tooltip_text("Pista Anterior");
    ant->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Controls::clicked), "Anterior"));
    insert(*ant, -1);

    pla = new Gtk::ToolButton(
        *Controls::get_imagen("./Iconos/play.svg", false), "");
    pla->set_tooltip_text("Reproducir");
    pla->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Controls::clicked), "Play"));
    insert(*pla, -1);

    sig = new Gtk::ToolButton(
        *Controls::get_imagen("./Iconos/siguiente.svg", false), "");
    sig->set_tooltip_text("Pista Siguiente");
    sig->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Controls::clicked), "Siguiente"));
    insert(*sig, -1);

    sto = new Gtk::ToolButton(
        *Controls::get_imagen("./Iconos/stop.svg", false), "");
    sto->set_tooltip_text("Detener Reproducción");
    sto->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Controls::clicked), "Stop"));
    insert(*sto, -1);

    vol = new Gtk::VolumeButton();
    vol->set_image(*Controls::get_imagen(
        "./Iconos/Media-Controls-Volume-Up-icon.png", false));
    vol->signal_value_changed().connect(
        sigc::mem_fun(*this, &Controls::vol_changed));

    {
        Gtk::ToolItem *item = new Gtk::ToolItem(); item->add(*vol);
        insert(*item, -1);
        Gtk::SeparatorToolItem *sep = new Gtk::SeparatorToolItem();
        sep->set_draw(false);
        sep->set_expand(true);
        insert(*sep, -1);}
        show_all();
    }

Gtk::Image * Controls::get_imagen(Glib::ustring file, bool flip){
    try{
        Glib::RefPtr<Gdk::Pixbuf> pixbuf = Gdk::Pixbuf::create_from_file(file);
        pixbuf = pixbuf->scale_simple(24, 24, Gdk::INTERP_BILINEAR);
        if (flip) {
            pixbuf = pixbuf->flip(true);}
        Gtk::Image *imagen = new Gtk::Image(pixbuf);
        return imagen;}
    catch(const Glib::FileError& e){
        std::cout << e.what() << std::endl;
        Gtk::Image *imagen = new Gtk::Image();
        return imagen;}}

void Controls::init(){
    set_sensitive(false);
    set_estado("paused");}

//void Controls::toggled(Glib::ustring text, Gtk::ToggleToolButton *button){
    //JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    //top->toolbar_accion(text, button->get_active());}

void Controls::set_estado(Glib::ustring valor){
    Glib::signal_idle().connect(sigc::bind<Glib::ustring>(
        sigc::mem_fun(*this, &Controls::run_set_estado), valor));}

bool Controls::run_set_estado(Glib::ustring valor){
    if (estado != valor){
        estado = valor;
        Gtk::Image *img = dynamic_cast<Gtk::Image*> (pla->get_icon_widget());
        if (estado == "playing"){
            img->set(pixbufplay);
            pla->set_tooltip_text("Pausar");}
        else{
            img->set(pixbufpause);
            pla->set_tooltip_text("Reproducir");}}
    return false;}

void Controls::clicked(Glib::ustring text){
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    top->toolbar_accion(text, true);}

void Controls::vol_changed(double value){
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    top->vol_changed(value);}

void Controls::set_vol(double valor){
    vol->set_value(valor);}
