#include <iostream>
#include <gtkmm/application.h>
#include "JAMedia.h"


int main(int argc, char** argv, char** env) {
    std::cout << std::endl << "JAMedia 16 (c++)" << std::endl;
    std::cout << "Requiere gtkmm para Gtk3 y ";
    std::cout << "gstreamermm para gstreamer-0.10" << std::endl;
    std::cout << "libgstreamermm-0.10" << std::endl;
    std::cout << "Por más información visita: ";
    std::cout << "https://sites.google.com/site/sugaractivities/";
    std::cout << "jamediaobjects/jam" << std::endl;
    std::cout << "Flavio Danesse <fdanesse@gmail.com> - ";
    std::cout << "San José - Uruguay" << std::endl << std::endl;
    Glib::RefPtr<Gtk::Application> app =
        Gtk::Application::create(argc, argv, "uy.gtkmm.jamedia");
    JAMedia jamedia;
    return app->run(jamedia);
    //return EXIT_SUCCESS;
}
