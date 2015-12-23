#include "ToolbarList.h"
#include "../JAMedia.h"

//using namespace std;


ToolbarList::ToolbarList(){

    con = new Gtk::ToggleToolButton(*ToolbarList::get_imagen(
        "./Iconos/control_panel.png", false), "");
    con->set_tooltip_text("Configuraciones");
    con->signal_toggled().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &ToolbarList::toggled), "Balance", con));
    insert(*con, -1);

    mas = new Gtk::ToolButton(*ToolbarList::get_imagen(
        "./Iconos/document-new.svg", false), "");
    mas->set_tooltip_text("Agregar Archivos");
    mas->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &ToolbarList::clicked), "Mas"));
    insert(*mas, -1);

    ope = new Gtk::ToolButton(*ToolbarList::get_imagen(
        "./Iconos/document-open.svg", false), "");
    ope->set_tooltip_text("Cargar Archivos");
    ope->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &ToolbarList::clicked), "Open"));
    insert(*ope, -1);

    cle = new Gtk::ToolButton(
        *ToolbarList::get_imagen("./Iconos/clear.svg", false), "");
    cle->set_tooltip_text("Limpiar Lista");
    cle->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &ToolbarList::clicked), "Clear"));
    insert(*cle, -1); show_all();}

Gtk::Image * ToolbarList::get_imagen(Glib::ustring file, bool flip){
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

void ToolbarList::init(){
    con->set_active(false);
    con->set_sensitive(false);
    mas->set_sensitive(false);
    cle->set_sensitive(false);}

void ToolbarList::activar(Glib::ustring valor){
    size_t found;
    found = valor.find("clear");
    if (found!=std::string::npos){
        cle->set_sensitive(true);}
    found = valor.find("mas");
    if (found!=std::string::npos){
        mas->set_sensitive(true);}
    found = valor.find("con");
    if (found!=std::string::npos){
        con->set_sensitive(true);}}

void ToolbarList::toggled(Glib::ustring text, Gtk::ToggleToolButton *button){
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    top->toolbar_accion(text, button->get_active());}

void ToolbarList::clicked(Glib::ustring text){
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    if (text == "Clear"){
        top->init();}
    else if (text == "Open"){
        top->open_files();}
    else if (text == "Mas"){
        top->add_files();}}

void ToolbarList::video(bool val){
    con->set_active(false);
    con->set_sensitive(val);}
