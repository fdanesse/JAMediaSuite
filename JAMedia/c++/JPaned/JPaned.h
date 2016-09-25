#ifndef JPaned_H
#define JPaned_H

#include <iostream>
#include <sigc++/sigc++.h>
#include <vector>
#include <glibmm/ustring.h>
#include <gtkmm/hvpaned.h>
#include <gtkmm/drawingarea.h>
#include <gdkmm.h>
#include <gdk/gdkx.h>

#include "../PlayerList/PlayerList.h"


class JPaned : public Gtk::HPaned{

    public:
        ~JPaned(){};
        JPaned();

        void init();
        void activar(Glib::ustring valor);
        void list_view(bool val);
        void open_files(std::vector<std::basic_string<char> > lista);
        void select_begin();
        void previous_track();
        void next_track();
        void view_conf_or_list(Glib::ustring text, bool active);
        gulong get_xid();
        void video(bool val);
        void new_file();
        //void set_info(Glib::ustring info);

    private:
        Gtk::DrawingArea *drawing;
        PlayerList *playerlist;

        virtual bool motion(const GdkEventMotion *event);
};

#endif // JPaned_H
