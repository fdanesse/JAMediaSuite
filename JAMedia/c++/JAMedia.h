#ifndef JAMedia_H
#define JAMedia_H

#include <iostream>
#include <sigc++/sigc++.h>
#include <vector>
#include <glibmm/ustring.h>
#include <gtkmm/window.h>
#include <gtkmm/box.h>
#include <glibmm/fileutils.h>
#include <gtkmm/filechooserdialog.h>
#include <gtkmm/hvscale.h>
#include <gtkmm/adjustment.h>
#include "JToolbar/JToolbar.h"
#include "JPaned/JPaned.h"
#include "Controls/Controls.h"
#include "JAMediaPlayer/JAMediaPlayer.h"


class JAMedia : public Gtk::Window{

    public:
        ~JAMedia(){};
        JAMedia();

        void init();
        void toolbar_accion(Glib::ustring text, bool active);
        void vol_changed(double value);
        void motion(bool val);
        void open_files();
        void add_files();
        void load_file(Glib::ustring track);
        void previous_track();
        void next_track();
        void set_balance(Glib::ustring text, double val);

    private:
        Gtk::VBox *vbox;
        JToolbar *toolbar;
        JPaned *panel;
        Gtk::HScale *progress;
        Controls *controls;
        JAMediaPlayer *player = NULL;

        double vol;

        void video();
        void set_progress(double val);
        void estado_update(Glib::ustring valor);
        void progress_update(gint64 valor);
        std::vector<std::basic_string<char> > run_open_files();
};

#endif // JAMedia_H
