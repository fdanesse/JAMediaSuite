#ifndef JMenu_H
#define JMenu_H

#include <iostream>
#include <sigc++/sigc++.h>
#include <glibmm/ustring.h>
#include <gtkmm/menu.h>
#include <gtkmm/menuitem.h>
#include <gtkmm/treepath.h>


class JMenu : public Gtk::Menu{

    public:
        ~JMenu(){};
        JMenu(Gtk::TreePath path, bool is_file, bool is_video);

    private:

        Gtk::TreePath path;
        bool __on_button_press_event(
            GdkEventButton *button_event, Glib::ustring text);
};

#endif // JMenu_H
