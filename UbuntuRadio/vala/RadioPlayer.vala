/*
   RadioPlayer.vala por:
   Flavio Danesse <fdanesse@gmail.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

//http://references.valadoc.org/#!api=gstreamer-1.0/Gst.Element


public class UbuntuRadioPlayer : GLib.Object{
    /*
    Reproductor Gstreamer Básico de la Aplicación.
    */

    private dynamic Gst.Element player = Gst.ElementFactory.make(
        "playbin", "play");

    public double _volumen = 0.10;
    public string _uri = "";
    public string _estado = "None";

    public signal void endfile();
    public signal void estado(string estado);

    public UbuntuRadioPlayer(){

        Gst.Bus bus = this.player.get_bus();
        bus.enable_sync_message_emission();

        bus.sync_message.connect(this.sync_message);

        this.set_volumen(this._volumen);
    }

    public void set_volumen(double valor){

        this._volumen = valor;
        this.player.volume = this._volumen;
    }

    public void load(string uri){
        /*
        if os.path.exists(uri):
            direccion = Gst.filename_to_uri(uri)
            self.player.set_property("uri", direccion)

        else:
            if Gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
        */
        this.stop();
        this._uri = uri;
        this.player.set("uri", this._uri);
        this.play();
    }

    public void play(){

        if (this._uri != ""){
            this.player.set_state(Gst.State.PLAYING);
        }
    }

    public void stop(){

        this.player.set_state(Gst.State.NULL);
    }

    private void sync_message(Gst.Message message){

        switch(message.type){

            case Gst.MessageType.ERROR:
                GLib.Error err;
                string debug;
                message.parse_error(out err, out debug);
                stdout.printf("Error: %s\n", err.message);
                this.endfile();
                break;

            case Gst.MessageType.LATENCY:
                //FIXME: dynamic methods are not supported for `Gst.Element'
                //this.player.recalculate_latency();
                break;

            case Gst.MessageType.EOS:
                this.endfile();
                break;

            case Gst.MessageType.STATE_CHANGED:
                Gst.State oldstate;
                Gst.State newstate;
                Gst.State pending;

                message.parse_state_changed(
                    out oldstate, out newstate, out pending);

                if (oldstate == Gst.State.PAUSED &&
                    newstate == Gst.State.PLAYING){
                    if (this._estado != "playing"){
                        this._estado = "playing";
                        this.estado("playing");
                        }
                }
                else if (oldstate == Gst.State.READY &&
                    newstate == Gst.State.PAUSED){
                    if (this._estado != "paused"){
                        this._estado = "paused";
                        this.estado("paused");
                        }
                }
                else if (oldstate == Gst.State.READY &&
                    newstate == Gst.State.NULL){
                    if (this._estado != "None"){
                        this._estado = "None";
                        this.estado("None");
                        }
                }
                else if (oldstate == Gst.State.PLAYING &&
                    newstate == Gst.State.PAUSED){
                    if (this._estado != "paused"){
                        this._estado = "paused";
                        this.estado("paused");
                    }
                }

                break;

            default:
                break;
        }
    }
}
