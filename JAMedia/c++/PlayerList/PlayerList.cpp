#include "../JAMedia.h"
#include "PlayerList.h"

//using namespace std;


PlayerList::PlayerList(){
    set_size_request(170, -1);
    vbox = new Gtk::VBox();
    toolbar = new ToolbarList();
    balance = new Balance();
    treeview = new JTreeView();
    vbox->pack_start(*toolbar, false, false, 0);
    {
        Gtk::ScrolledWindow *scroll = new Gtk::ScrolledWindow();
        scroll->set_policy(Gtk::POLICY_AUTOMATIC, Gtk::POLICY_AUTOMATIC);
        Gtk::VBox *vbox1 = new Gtk::VBox(); scroll->add(*vbox1);
        vbox1->pack_start(*balance, false, false, 0);
        vbox1->pack_start(*treeview, false, false, 0);
        vbox->pack_start(*scroll, true, true, 0);
    }
    add(*vbox);
    show_all();}

//void PlayerList::set_info(Glib::ustring info){
//    balance->set_info(info);}

void PlayerList::view_conf_or_list(Glib::ustring text, bool active){
    if (active){
        balance->show();
        treeview->hide();}
    else {
        balance->hide();
        treeview->show();}}

void PlayerList::init(){//Cuando la lista se llena o se vacía
    toolbar->init();
    balance->hide();
    treeview->show();
    treeview->clear_list();}

void PlayerList::activar(Glib::ustring valor){
    toolbar->activar(valor);}

void PlayerList::open_files(std::vector<std::basic_string<char> > lista){
    treeview->open_files(lista);}

void PlayerList::select_begin(){
    treeview->select_begin();}

void PlayerList::previous_track(){
    treeview->previous_track();}

void PlayerList::next_track(){
    treeview->next_track();}

void PlayerList::video(bool val){
    if (val){
        toolbar->activar("con");}
    else{
        toolbar->video(val);
        balance->hide();
        treeview->show();}}

void PlayerList::new_file(){
    video(false);
    balance->init();}
