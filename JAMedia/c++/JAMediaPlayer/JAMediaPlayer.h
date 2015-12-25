#ifndef JAMediaPlayer_H
#define JAMediaPlayer_H

#include <iostream>
#include <sigc++/sigc++.h>
#include <glibmm.h>
#include <gstreamermm.h>


class JAMediaPlayer : public Glib::Object{

    public:
        ~JAMediaPlayer(){};
        JAMediaPlayer();

        sigc::signal<void> signal_end;
        sigc::signal<void> signal_video;
        sigc::signal<void, gint64> signal_progress_update;
        sigc::signal<void, Glib::ustring> signal_estado_update;
        sigc::signal<void, Glib::ustring> signal_info_update;

        void load(Glib::ustring track, const gulong ventana_id);
        void set_vol(double value);
        void play();
        void pause_play();
        void stop();
        void seek_pos(gint64 val);
        void rotar(Glib::ustring valor);
        void set_balance(Glib::ustring prop, double valor);
        void load_sub(Glib::ustring file);

    private:
        gulong xid;
        gint64 posicion;
        bool progressbar;
        sigc::connection actualizador;

        Glib::RefPtr<Gst::PlayBin2> playbin;
        Glib::RefPtr<Gst::Bin> video;
        Glib::RefPtr<Gst::Element> videoflip;
        Glib::RefPtr<Gst::Element> videobalance;
        Glib::RefPtr<Gst::Element> gamma;
        Glib::RefPtr<Gst::Bus> bus;
        Gst::State estado;

        //void on_bus_message_sync(const Glib::RefPtr<Gst::Message>& message);
        bool on_bus_message(const Glib::RefPtr<Gst::Bus>& bus,
            const Glib::RefPtr<Gst::Message>& message);
        void new_handler(bool reset);
        bool handler();
};

#endif // JAMediaPlayer_H
