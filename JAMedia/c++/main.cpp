#include <gtkmm/application.h>
#include "JAMedia.h"


int main(int argc, char** argv, char** env) {
    Glib::RefPtr<Gtk::Application> app =
        Gtk::Application::create(argc, argv, "uy.gtkmm.jamedia");
    JAMedia jamedia;
    return app->run(jamedia);
    //return EXIT_SUCCESS;
}
