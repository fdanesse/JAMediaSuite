#include "JToolbar.h"
#include "../JAMedia.h"

//using namespace std;


JToolbar::JToolbar(){

    cre = new Gtk::ToolButton(
        *JToolbar::get_imagen("./Iconos/JAMedia.svg", false), "");
    cre->set_tooltip_text("Créditos");
    cre->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JToolbar::clicked), "Creditos"));
    insert(*cre, -1);

    ayu = new Gtk::ToolButton(
        *JToolbar::get_imagen("./Iconos/help.svg", false), "");
    ayu->set_tooltip_text("Ayuda");
    ayu->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JToolbar::clicked), "Ayuda"));
    insert(*ayu, -1);

    {
        Gtk::SeparatorToolItem *sep = new Gtk::SeparatorToolItem();
        insert(*sep, -1);
    }

    izq = new Gtk::ToolButton(
        *JToolbar::get_imagen("./Iconos/rotar.svg", false), "");
    izq->set_tooltip_text("Rotar a la Izquierda");
    izq->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JToolbar::clicked), "Izquierda"));
    insert(*izq, -1);

    der = new Gtk::ToolButton(
        *JToolbar::get_imagen("./Iconos/rotar.svg", true), "");
    der->set_tooltip_text("Rotar a la Derecha");
    der->signal_clicked().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JToolbar::clicked), "Derecha"));
    insert(*der, -1);

    {
        Gtk::SeparatorToolItem *sep = new Gtk::SeparatorToolItem();
        insert(*sep, -1);
    }

    lis = new Gtk::ToggleToolButton(
        *JToolbar::get_imagen("./Iconos/lista.svg", false), "");
    lis->set_tooltip_text("Lista Visibles");
    lis->set_active(true);
    lis->signal_toggled().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JToolbar::toggled), "Lista", lis));
    insert(*lis, -1);

    con = new Gtk::ToggleToolButton(
        *JToolbar::get_imagen("./Iconos/controls.svg", false), "");
    con->set_tooltip_text("Controles Visibles");
    con->set_active(true);
    //con->signal_toggled().connect(sigc::bind<Glib::ustring> (
    //    sigc::mem_fun(*this, &JToolbar::toggled), "Controles", con));
    insert(*con, -1);

    ful = new Gtk::ToggleToolButton(
        *JToolbar::get_imagen("./Iconos/fullscreen.png", false), "");
    ful->set_tooltip_text("Pantalla Completa");
    ful->set_active(false);
    ful->signal_toggled().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JToolbar::toggled), "Fullscreen", ful));
    insert(*ful, -1);

    {
        Gtk::SeparatorToolItem *sep = new Gtk::SeparatorToolItem();
        sep->set_draw(false);
        sep->set_expand(true);
        insert(*sep, -1);}
        show_all();
    }

Gtk::Image * JToolbar::get_imagen(Glib::ustring file, bool flip){
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

void JToolbar::toggled(Glib::ustring text, Gtk::ToggleToolButton *button){
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    top->toolbar_accion(text, button->get_active());}

void JToolbar::clicked(Glib::ustring text){
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    top->toolbar_accion(text, true);}

bool JToolbar::get_view_controls(){
    return con->get_active();}

bool JToolbar::get_view_list(){
    return lis->get_active();}

void JToolbar::video(bool val){
    izq->set_sensitive(val);
    der->set_sensitive(val);}
