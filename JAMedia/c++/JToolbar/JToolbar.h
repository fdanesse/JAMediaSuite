#ifndef JToolbar_H
#define JToolbar_H

#include <iostream>
#include <sigc++/sigc++.h>
#include <glibmm/ustring.h>
#include <glibmm/fileutils.h>
#include <gdkmm/pixbuf.h>
#include <gtkmm/toolbar.h>
#include <gtkmm/toggletoolbutton.h>
#include <gtkmm/image.h>
#include <gtkmm/separatortoolitem.h>


class JToolbar : public Gtk::Toolbar{

    public:
        ~JToolbar(){};
        JToolbar();

        bool get_view_controls();
        bool get_view_list();
        void video(bool val);

    private:
        Gtk::ToolButton *cre;
        Gtk::ToolButton *ayu;
        Gtk::ToolButton *izq;
        Gtk::ToolButton *der;

        Gtk::ToggleToolButton *lis;
        Gtk::ToggleToolButton *con;
        Gtk::ToggleToolButton *ful;

        Gtk::Image * get_imagen(Glib::ustring file, bool flip);

        virtual void toggled(Glib::ustring text,
            Gtk::ToggleToolButton *button);
        virtual void clicked(Glib::ustring text);
};

#endif // JToolbar_H
