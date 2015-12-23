#include "JMenu.h"
#include "JTreeView.h"

//using namespace std;


JMenu::JMenu(Gtk::TreePath p, bool is_file, bool is_video){

    path = p;

    if (is_video){
        Gtk::MenuItem *item = new Gtk::MenuItem();
        item->add_label("Abrir Subtítulos");
        item->signal_button_press_event().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JMenu::__on_button_press_event), "Subtitulos"));
        append(*item);}

    Gtk::MenuItem *item1 = new Gtk::MenuItem();
    item1->add_label("Quitar de la Lista");
    item1->signal_button_press_event().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JMenu::__on_button_press_event), "Quitar"));
    append(*item1);

    if (is_file){
        Gtk::MenuItem *item4 = new Gtk::MenuItem();
        item4->add_label("Copiar...");
        item4->signal_button_press_event().connect(sigc::bind<Glib::ustring> (
            sigc::mem_fun(*this, &JMenu::__on_button_press_event), "Copiar"));
        append(*item4);}

    if (is_file){
        Gtk::MenuItem *item5 = new Gtk::MenuItem();
        item5->add_label("Mover a...");
        item5->signal_button_press_event().connect(sigc::bind<Glib::ustring> (
            sigc::mem_fun(*this, &JMenu::__on_button_press_event), "Mover"));
        append(*item5);}

    Gtk::MenuItem *item3 = new Gtk::MenuItem();
    item3->add_label("Grabar/Convertir/Extraer...");
    item3->signal_button_press_event().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &JMenu::__on_button_press_event), "Grabar"));
    append(*item3);

    if (is_file){
        Gtk::MenuItem *item2 = new Gtk::MenuItem();
        item2->add_label("Borrar Definitivamente");
        item2->signal_button_press_event().connect(sigc::bind<Glib::ustring> (
            sigc::mem_fun(*this, &JMenu::__on_button_press_event), "Borrar"));
        append(*item2);}

    show_all();}

bool JMenu::__on_button_press_event(GdkEventButton *button_event, Glib::ustring text){
    JTreeView *treeview = dynamic_cast<JTreeView*> (get_attach_widget());
    treeview->accion_menu(text, path);
    return true;}
