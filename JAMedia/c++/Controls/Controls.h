#ifndef Controls_H
#define Controls_H

#include <iostream>
#include <vector>
#include <sigc++/sigc++.h>
#include <glibmm/ustring.h>
#include <glibmm/fileutils.h>
#include <gdkmm/pixbuf.h>
#include <gtkmm/toolbar.h>
#include <gtkmm/toggletoolbutton.h>
#include <gtkmm/volumebutton.h>
#include <gtkmm/image.h>
#include <gtkmm/toolitem.h>


class Controls : public Gtk::Toolbar{

    public:
        ~Controls(){};
        Controls();

        void set_vol(double valor);
        void set_estado(Glib::ustring valor);
        void init();

    private:
        Gtk::ToolButton *ant;
        Gtk::ToolButton *pla;
        Gtk::ToolButton *sig;
        Gtk::ToolButton *sto;
        Gtk::VolumeButton *vol;

        Glib::RefPtr<Gdk::Pixbuf> pixbufplay;
        Glib::RefPtr<Gdk::Pixbuf> pixbufpause;

        Glib::ustring estado;
        Gtk::Image * get_imagen(Glib::ustring file, bool flip);

        //virtual void toggled(Glib::ustring text,
        //  Gtk::ToggleToolButton *button);
        virtual void clicked(Glib::ustring text);
        virtual void vol_changed(double value);
        bool run_set_estado(Glib::ustring valor);
    };

#endif // Controls_H
