#ifndef Balance_H
#define Balance_H

#include <iostream>
#include <sstream>
#include <sigc++/sigc++.h>
#include <gtkmm/box.h>
#include <gtkmm/frame.h>
#include <gtkmm/eventbox.h>
#include <gtkmm/hvscale.h>
#include <gtkmm/adjustment.h>
#include <gtkmm/textview.h>


class Balance : public Gtk::VBox{

    public:
        ~Balance(){};
        Balance();
        void init();
        //void set_info(Glib::ustring info);

    private:
        Gtk::Frame *fbri;
        Gtk::HScale *pbri;
        Gtk::Frame *fcon;
        Gtk::HScale *pcon;
        Gtk::Frame *fsat;
        Gtk::HScale *psat;
        Gtk::Frame *fmat;
        Gtk::HScale *pmat;
        Gtk::Frame *fgam;
        Gtk::HScale *pgam;
        //Gtk::TextView *textview;

        void on_adjustment_value_changed(Glib::ustring text);
        bool run_adjustment_value(Glib::ustring text);
};

#endif // Balance_H
