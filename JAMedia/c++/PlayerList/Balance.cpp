#include "../JAMedia.h"
#include "Balance.h"
#include "../JAMedia.h"

//using namespace std;


Balance::Balance(){
    Gtk::EventBox *event;

    fbri = new Gtk::Frame(" Brillo: ");
    fbri->set_border_width(4);
    pbri = new Gtk::HScale(
        Gtk::Adjustment::create(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    pbri->signal_value_changed().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Balance::on_adjustment_value_changed), "Brillo"));
    pbri->set_value(50.0);
    pbri->set_draw_value(false);
    event = new Gtk::EventBox();
    event->set_border_width(4);
    fbri->add(*event);
    event->add(*pbri);
    pack_start(*fbri, false, false, 0);

    fcon = new Gtk::Frame(" Contraste: ");
    fcon->set_border_width(4);
    pcon = new Gtk::HScale(
        Gtk::Adjustment::create(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    pcon->signal_value_changed().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Balance::on_adjustment_value_changed), "Contraste"));
    pcon->set_value(50.0);
    pcon->set_draw_value(false);
    event = new Gtk::EventBox();
    event->set_border_width(4);
    fcon->add(*event);
    event->add(*pcon);
    pack_start(*fcon, false, false, 0);

    fsat = new Gtk::Frame(" Saturación: ");
    fsat->set_border_width(4);
    psat = new Gtk::HScale(
        Gtk::Adjustment::create(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    psat->signal_value_changed().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Balance::on_adjustment_value_changed), "Saturacion"));
    psat->set_value(50.0);
    psat->set_draw_value(false);
    event = new Gtk::EventBox();
    event->set_border_width(4);
    fsat->add(*event);
    event->add(*psat);
    pack_start(*fsat, false, false, 0);

    fmat = new Gtk::Frame(" Matiz: ");
    fmat->set_border_width(4);
    pmat = new Gtk::HScale(
        Gtk::Adjustment::create(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    pmat->signal_value_changed().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Balance::on_adjustment_value_changed), "Matiz"));
    pmat->set_value(50.0);
    pmat->set_draw_value(false);
    event = new Gtk::EventBox();
    event->set_border_width(4);
    fmat->add(*event);
    event->add(*pmat);
    pack_start(*fmat, false, false, 0);

    fgam = new Gtk::Frame(" Gamma: ");
    fgam->set_border_width(4);
    pgam = new Gtk::HScale(
        Gtk::Adjustment::create(0.0, 0.0, 101.0, 0.1, 1.0, 1.0));
    pgam->signal_value_changed().connect(sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Balance::on_adjustment_value_changed), "Gamma"));
    pgam->set_value(10.0);
    pgam->set_draw_value(false);
    event = new Gtk::EventBox();
    event->set_border_width(4);
    fgam->add(*event);
    event->add(*pgam);
    pack_start(*fgam, false, false, 0);

    //textview = new Gtk::TextView();
    //pack_start(*textview, true, true, 0);
    //textview->set_editable(false);

    show_all();}

void Balance::init(){
    pbri->set_value(50.0);
    pcon->set_value(50.0);
    psat->set_value(50.0);
    pmat->set_value(50.0);
    pgam->set_value(10.0);
    //textview->get_buffer()->set_text("");
    }

//void Balance::set_info(Glib::ustring info){
//    Glib::ustring text = textview->get_buffer()->get_text();
//    textview->get_buffer()->set_text(text + info + "\n");}

void Balance::on_adjustment_value_changed(Glib::ustring text){
    Glib::signal_idle().connect( sigc::bind<Glib::ustring> (
        sigc::mem_fun(*this, &Balance::run_adjustment_value), text));}

bool Balance::run_adjustment_value(Glib::ustring text){
    double val = 0.0;
    if (text == "Brillo"){
        val = pbri->get_value();
        std::ostringstream os;
        os << (int)val;
        Glib::ustring str = os.str();
        fbri->set_label(" Brillo: " + str + "%");}
    else if (text == "Contraste"){
        val = pcon->get_value();
        std::ostringstream os;
        os << (int)val;
        Glib::ustring str = os.str();
        fcon->set_label(" Contraste: " + str + "%");}
    else if (text == "Saturacion"){
        val = psat->get_value();
        std::ostringstream os;
        os << (int)val;
        Glib::ustring str = os.str();
        fsat->set_label(" Saturacion: " + str + "%");}
    else if (text == "Matiz"){
        val = pmat->get_value();
        std::ostringstream os;
        os << (int)val;
        Glib::ustring str = os.str();
        fmat->set_label(" Matiz: " + str + "%");}
    else if (text == "Gamma"){
        val = pgam->get_value();
        std::ostringstream os;
        os << (int)val;Glib::ustring str = os.str();
        fgam->set_label(" Gamma: " + str + "%");}
    JAMedia *top = dynamic_cast<JAMedia*> (this->get_toplevel());
    top->set_balance(text, val);
    return false;}
