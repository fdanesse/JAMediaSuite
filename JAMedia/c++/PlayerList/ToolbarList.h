#ifndef ToolbarList_H
#define ToolbarList_H

#include <iostream>
#include <sigc++/sigc++.h>
#include <glibmm/ustring.h>
#include <glibmm/fileutils.h>
#include <gdkmm/pixbuf.h>
#include <gtkmm/toolbar.h>
#include <gtkmm/toggletoolbutton.h>
#include <gtkmm/toolbutton.h>
#include <gtkmm/image.h>


class ToolbarList : public Gtk::Toolbar{

    public:
        ~ToolbarList(){};
        ToolbarList();

        void init();
        void activar(Glib::ustring valor);
        void video(bool val);

    private:
        Gtk::ToggleToolButton *con;
        Gtk::ToolButton *mas;
        Gtk::ToolButton *ope;
        Gtk::ToolButton *cle;

        Gtk::Image * get_imagen(Glib::ustring file, bool flip);

        virtual void toggled(Glib::ustring text,
            Gtk::ToggleToolButton *button);
        virtual void clicked(Glib::ustring text);
};

#endif // ToolbarList_H
