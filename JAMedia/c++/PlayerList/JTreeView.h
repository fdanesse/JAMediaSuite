#ifndef JTreeView_H
#define JTreeView_H

#include <iostream>
#include <fstream>
#include <sigc++/sigc++.h>
#include <vector>
#include <gstreamermm.h>
#include <giomm/file.h>
#include <giomm/fileinfo.h>
#include <gdkmm/pixbuf.h>
#include <gtkmm/treeview.h>
#include <gtkmm/liststore.h>
#include <gtkmm/treeselection.h>
#include <gtkmm/dialog.h>
#include <gtkmm/label.h>
#include <gtkmm/filechooserdialog.h>
#include "JMenu.h"


class JTreeView : public Gtk::TreeView{

    public:
        ~JTreeView(){};
        JTreeView();

        void clear_list();
        void open_files(std::vector<std::basic_string<char> > lista);
        void select_begin();
        void previous_track();
        void next_track();
        void accion_menu(Glib::ustring text, Gtk::TreePath path);

    private:
        Glib::RefPtr<Gtk::ListStore> listore;
        Glib::RefPtr<Gtk::TreeSelection> sel;

        void select_end();
        //bool select_function(const Glib::RefPtr<Gtk::TreeModel>& model,
        //  const Gtk::TreeModel::Path& path, bool);
        void row_activated(const Gtk::TreePath &path, Gtk::TreeViewColumn*);
        bool on_button_press_event(GdkEventButton* event);

        void save_file(Glib::ustring process, Glib::ustring accion);
        void delete_file(Glib::ustring process);

        void append_file_track(std::basic_string<char> path);
        void pls_read(std::basic_string<char> path);

        class ModelColumns : public Gtk::TreeModel::ColumnRecord{
            public:
                ModelColumns(){add(pix); add(name); add(path);}
                Gtk::TreeModelColumn< Glib::RefPtr<Gdk::Pixbuf> > pix;
                Gtk::TreeModelColumn<Glib::ustring> name;
                Gtk::TreeModelColumn<Glib::ustring> path;};

        ModelColumns cols;
};

#endif // JTreeView_H
