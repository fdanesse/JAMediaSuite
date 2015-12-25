#ifndef PlayerList_H
#define PlayerList_H

#include <iostream>
#include <sigc++/sigc++.h>
#include <vector>
#include <gtkmm/frame.h>
#include <gtkmm/box.h>
#include <gtkmm/scrolledwindow.h>
#include "ToolbarList.h"
#include "JTreeView.h"
#include "Balance.h"


class PlayerList : public Gtk::Frame{

    public:
        ~PlayerList(){};
        PlayerList();

        void init();
        void activar(Glib::ustring valor);
        void open_files(std::vector<std::basic_string<char> > lista);
        void select_begin();
        void previous_track();
        void next_track();
        void view_conf_or_list(Glib::ustring text, bool active);
        void video(bool val);
        void new_file();
        //void set_info(Glib::ustring info);

    private:
        Gtk::VBox *vbox;
        ToolbarList *toolbar;
        Balance *balance;
        JTreeView *treeview;
};

#endif // PlayerList_H
