#include "JAMediaPlayer.h"

//using namespace std;


JAMediaPlayer::JAMediaPlayer(){

    Gst::init();
    playbin = Gst::PlayBin2::create();
    //playbin.set_property("buffer-size", 50000)

    //Video out
    video = Gst::Bin::create("jamedia_video_pipeline");

    Glib::RefPtr<Gst::Element> convert =
        Gst::ElementFactory::create_element("ffmpegcolorspace", "conv");
    Glib::RefPtr<Gst::Element> rate =
        Gst::ElementFactory::create_element("videorate", "rate");
    videobalance = Gst::ElementFactory::create_element(
        "videobalance", "videobalance");
    gamma = Gst::ElementFactory::create_element("gamma", "gamma");
    videoflip = Gst::ElementFactory::create_element("videoflip", "videoflip");
    Glib::RefPtr<Gst::XvImageSink> pantalla = Gst::XvImageSink::create();

    rate->set_property("max-rate", 30);
    pantalla->property_force_aspect_ratio() = true;
    pantalla->set_sync(true);

    video->add(convert);
    video->add(rate);
    video->add(videobalance);
    video->add(gamma);
    video->add(videoflip);
    video->add(pantalla);

    convert->link(rate);
    rate->link(videobalance);
    videobalance->link(gamma);
    gamma->link(videoflip);
    videoflip->link(pantalla);

    Glib::RefPtr<Gst::GhostPad> ghost_pad =
        Gst::GhostPad::create(convert->get_static_pad("sink"), "sink");
    video->add_pad(ghost_pad);

    playbin->property_video_sink() = video;

    Glib::RefPtr<Gst::Bus> bus = playbin->get_bus();
    bus->add_watch(sigc::mem_fun(*this, &JAMediaPlayer::on_bus_message));
    //bus->enable_sync_message_emission();
    //bus->signal_sync_message().connect(
    //  sigc::mem_fun(*this, &JAMediaPlayer::on_bus_message_sync));
}

//void JAMediaPlayer::on_bus_message_sync(const Glib::RefPtr<Gst::Message>& message){

bool JAMediaPlayer::on_bus_message(const Glib::RefPtr<Gst::Bus>& bus,
    const Glib::RefPtr<Gst::Message>& message){

    switch(message->get_message_type()){
        case Gst::MESSAGE_ELEMENT: {
            if (message->get_structure().has_name("prepare-xwindow-id")){
                Glib::RefPtr<Gst::Element> element =
                    Glib::RefPtr<Gst::Element>::cast_dynamic(message->get_source());
                Glib::RefPtr< Gst::ElementInterfaced<Gst::XOverlay> > xoverlay =
                    Gst::Interface::cast <Gst::XOverlay>(element);
                if (xoverlay){
                    xoverlay->set_xwindow_id(xid);}}
            break;}

        case Gst::MESSAGE_STATE_CHANGED:{
            Glib::RefPtr<Gst::MessageStateChanged> stateChangeMsg =
                Glib::RefPtr<Gst::MessageStateChanged>::cast_dynamic(message);
            if (stateChangeMsg){
                Gst::State oldState, newState, pendingState;
                stateChangeMsg->parse(oldState, newState, pendingState);
                if (estado != newState){
                    estado = newState;
                    if (estado == Gst::STATE_PLAYING){
                        signal_estado_update.emit("playing");
                        new_handler(true);}
                    else {signal_estado_update.emit("paused");
                        new_handler(false);}}}
            break;}

        case Gst::MESSAGE_EOS:{
            new_handler(false);
            signal_end.emit();
            return false;
            break;}

        case Gst::MESSAGE_ERROR:{
            Glib::RefPtr<Gst::MessageError> msgError =
                Glib::RefPtr<Gst::MessageError>::cast_static(message);
            if(msgError){
                Glib::Error err;
                err = msgError->parse();
                std::cerr << "Player Error: " << err.what() << std::endl;}
            else{
                std::cerr << "Player Error." << std::endl;}
            new_handler(false);
            return false;
            break;}

        case Gst::MESSAGE_TAG:{
            Glib::RefPtr<Gst::MessageTag> msg =
                Glib::RefPtr<Gst::MessageTag>::cast_static(message);
            Glib::ustring info = msg->get_structure().to_string();
            size_t found = info.find("video-codec");
            if (found!=std::string::npos){
                signal_video.emit();}
            signal_info_update.emit(info);
            break;}

        //elif message.type == gst.MESSAGE_BUFFERING:
        //    buf = int(message.structure["buffer-percent"])
        //    if buf < 100 and self.estado == gst.STATE_PLAYING:
        //        self.emit("loading-buffer", buf)
        //        self.__pause()
        //    elif buf > 99 and self.estado != gst.STATE_PLAYING:
        //        self.emit("loading-buffer", buf)
        //        self.play()

    }return true;}

void JAMediaPlayer::set_vol(double value){
    playbin->property_volume() = value;}

void JAMediaPlayer::play(){
    playbin->set_state(Gst::STATE_PLAYING);}

void JAMediaPlayer::pause_play(){
    //FIXME: Si esta stop y se da play no se reproduce a menos que se vuelva a presionar play
    if (estado == Gst::STATE_PLAYING){
        playbin->set_state(Gst::STATE_PAUSED);}
    else{
        playbin->set_state(Gst::STATE_PLAYING);}}

void JAMediaPlayer::stop(){
    new_handler(false);
    posicion = 0;
    playbin->set_state(Gst::STATE_NULL);
    signal_progress_update.emit(posicion);}

void JAMediaPlayer::load(Glib::ustring track, const gulong ventana_id){
    xid = ventana_id;
    posicion = 0;
    signal_progress_update.emit(posicion);
    //self.emit("loading-buffer", 100)
    if (gst_uri_is_valid(track.c_str())){
        playbin->property_uri() = track.c_str();
        progressbar = false;}
    else {
        playbin->property_uri() = Glib::filename_to_uri(track);
        progressbar = true;}}

void JAMediaPlayer::new_handler(bool reset){
    if (actualizador){
        actualizador.disconnect();}
    if (reset){
        actualizador = Glib::signal_timeout().connect(
        sigc::mem_fun(*this, &JAMediaPlayer::handler), 500);}}

bool JAMediaPlayer::handler(){
    if (progressbar){
        Gst::Format fmt = Gst::FORMAT_TIME;
        gint64 pos = 0;
        gint64 dur = 0;
        playbin->query_position(fmt, pos);
        playbin->query_duration(fmt, dur);
        pos /= Gst::SECOND;
        dur /= Gst::SECOND;
        pos = pos * 100 / dur;
        if (posicion != pos){
            posicion = pos;
            signal_progress_update.emit(posicion);}}
    return true;}

void JAMediaPlayer::seek_pos(gint64 val){
    Gst::Format fmt = Gst::FORMAT_TIME;
    gint64 pos = 0;
    gint64 dur = 0;
    playbin->query_position(fmt, pos);
    playbin->query_duration(fmt, dur);
    pos = dur * val / 100;
    playbin->seek(Gst::FORMAT_TIME, Gst::SEEK_FLAG_FLUSH, pos);}
    //Glib::RefPtr<Gst::Event> event = Gst::EventSeek::create(1.0, fmt,
    //    Gst::SEEK_FLAG_FLUSH, Gst::SEEK_TYPE_SET, pos, Gst::SEEK_TYPE_NONE, -1);
    //Glib::RefPtr<Gst::Element>::cast_static(playbin)->send_event(std::move(event))

void JAMediaPlayer::rotar(Glib::ustring valor){
    int rot;
    videoflip->get_property("method", rot);
    if (valor == "Derecha"){
        if (rot < 3){
            rot += 1;}
        else{
            rot = 0;}}
    else if (valor == "Izquierda"){
        if (rot > 0){
            rot -= 1;}
        else{
            rot = 3;}}
    videoflip->set_property("method", rot);}

void JAMediaPlayer::set_balance(Glib::ustring prop, double valor){
    if (prop == "Brillo"){
        double val = (2.0 * valor / 100.0) - 1.0;
        videobalance->set_property("brightness", val);}
    else if (prop == "Contraste"){
        double val = 2.0 * valor / 100.0;
        videobalance->set_property("contrast", val);}
    else if (prop == "Saturacion"){
        double val = 2.0 * valor / 100.0;
        videobalance->set_property("saturation", val);}
    else if (prop == "Matiz"){
        double val = (2.0 * valor / 100.0) - 1.0;
        videobalance->set_property("hue", val);}
    else if (prop == "Gamma"){
        double val = (10.0 * valor / 100.0);
        gamma->set_property("gamma", val);}}

void JAMediaPlayer::load_sub(Glib::ustring file){
    playbin->set_property("suburi", file);}
