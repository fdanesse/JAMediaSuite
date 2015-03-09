#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   HelpWidget.py por:
#       Flavio Danesse      <fdanesse@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from HELP import get_help


def format_SUGAR(buffer_help, tags_table):
    pass


def format_SINROOT(buffer_help, tags_table):
    pass


def format_STANDARD(buffer_help, tags_table):
    pass


def format_RPM(buffer_help, tags_table):
    pass


def format_DEB(buffer_help, tags_table):
    pass


def format_INSTALADORES(buffer_help, tags_table):
    tag1 = Gtk.TextTag.new("1")
    tag1.set_property("weight", Pango.Weight.BOLD)
    tags_table.add(tag1)

    tag2 = Gtk.TextTag.new("2")
    tag2.set_property("weight", Pango.Weight.BOLD)
    tag2.set_property("background-gdk", Gdk.Color(0, 0, 0))
    tag2.set_property("foreground-gdk", Gdk.Color(65000, 65000, 65000))
    tags_table.add(tag2)

    tag3 = Gtk.TextTag.new("3")
    tag3.set_property("weight", Pango.Weight.BOLD)
    tag3.set_property("background-gdk", Gdk.Color(60000, 60000, 60000))
    tags_table.add(tag3)

    tag4 = Gtk.TextTag.new("4")
    #tag4.set_property("weight", Pango.Weight.BOLD)
    tag4.set_property("foreground-gdk", Gdk.Color(0, 0, 65000))
    tags_table.add(tag4)

    tag5 = Gtk.TextTag.new("5")
    #tag5.set_property("weight", Pango.Weight.BOLD)
    tag5.set_property("foreground-gdk", Gdk.Color(65000, 0, 0))
    tags_table.add(tag5)

    tit2 = [1, 18, 72, 93]
    tit3 = [20, 24, 28, 36, 76]
    code1 = [31, 32, 58, 60, 62, 64, 69, 70, 77, 78, 79, 80, 81, 82,
        83, 84, 85, 86, 87, 88, 89]
    code2 = [42, 44, 52, 54]

    __apply_tag(buffer_help, 1, tag1)

    for _id in tit2:
        __apply_tag(buffer_help, _id, tag2)

    for _id in tit3:
        __apply_tag(buffer_help, _id, tag3)

    for _id in code1:
        __apply_tag(buffer_help, _id, tag4)

    for _id in code2:
        __apply_tag(buffer_help, _id, tag5)


def __apply_tag(buffer_help, _id, tag):
    iter_inicio = buffer_help.get_iter_at_line(_id)
    iter_fin = buffer_help.get_iter_at_line(_id + 1)
    buffer_help.apply_tag(tag, iter_inicio, iter_fin)


class HelpWidget(Gtk.EventBox):

    #__gtype_name__ = 'HelpWidget'

    def __init__(self, help):

        Gtk.EventBox.__init__(self)

        _dict = {
            "help instaladores": format_INSTALADORES,
            "help deb": format_DEB,
            "help rmp": format_RPM,
            "help standard": format_STANDARD,
            "help sin root": format_SINROOT,
            "help sugar": format_SUGAR,
            }

        tags_table = Gtk.TextTagTable()
        buffer_help = Gtk.TextBuffer.new(tags_table)
        textview = Gtk.TextView()
        textview.set_buffer(buffer_help)
        textview.set_editable(False)
        textview.set_border_width(15)
        buffer_help.set_text(get_help(help))
        _dict[help](buffer_help, tags_table)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(textview)

        self.add(scroll)
        self.show_all()
