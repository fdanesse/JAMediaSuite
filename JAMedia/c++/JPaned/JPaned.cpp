#include "JPaned.h"
#include "../JAMedia.h"

//using namespace std;
//using namespace Gdk;


JPaned::JPaned(){
    drawing = new Gtk::DrawingArea();
    playerlist = new PlayerList();
    drawing->override_background_color(
        Gdk::RGBA("BLACK"), Gtk::STATE_FLAG_NORMAL);
    pack1(*drawing, Gtk::EXPAND);
    pack2(*playerlist, Gtk::FILL);
    show_all();
    drawing->add_events(Gdk::POINTER_MOTION_MASK);
    drawing->signal_motion_notify_event().connect(
        sigc::mem_fun(*this, &JPaned::motion));}

//void JPaned::set_info(Glib::ustring info){
//    playerlist->set_info(info);}

void JPaned::view_conf_or_list(Glib::ustring text, bool active){
    playerlist->view_conf_or_list(text, active);}

void JPaned::init(){
    playerlist->init();}

void JPaned::activar(Glib::ustring valor){
    playerlist->activar(valor);}

bool JPaned::motion(const GdkEventMotion *event){
    //Desplazamiento del mouse sobre drawingarea.
    int x = int(event->x);
    int y = int(event->y);
    Gtk::Allocation rect = drawing->get_allocation();
    const int w = rect.get_width();
    const int h = rect.get_height();
    bool ret = false;
    if (y < 41 or y > h - 41 or x > w - 41 ){
        ret = true;}
    else{
        ret = false;}
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    top->motion(ret);
    return true;}

void JPaned::list_view(bool val){
    if (val){
        playerlist->show();}
    else{
        playerlist->hide();}}

void JPaned::open_files(std::vector<std::basic_string<char> > lista){
    playerlist->open_files(lista);}

void JPaned::select_begin(){
    playerlist->select_begin();}

void JPaned::previous_track(){
    playerlist->previous_track();}

void JPaned::next_track(){
    playerlist->next_track();}

gulong JPaned::get_xid(){
    gulong xid = GDK_WINDOW_XID(drawing->get_window()->gobj());
    return xid;}

void JPaned::video(bool val){
    playerlist->video(val);} //FIXME: drawing debe estar oculto si no hay video

void JPaned::new_file(){
    playerlist->new_file();}
