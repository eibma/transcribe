# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) 2010 Frederik Elwert <frederik.elwert@web.de>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

"""Helpers for an Ubuntu application."""

__all__ = [
    'make_window',
    ]

import os
import datetime

import gtk
import gio

from transcribe.transcribeconfig import get_data_file

import gettext
from gettext import gettext as _
gettext.textdomain('transcribe')

def get_builder(builder_file_name):
    """Return a fully-instantiated gtk.Builder instance from specified ui 
    file
    
    :param builder_file_name: The name of the builder file, without extension.
        Assumed to be in the 'ui' directory under the data path.
    """
    # Look for the ui file that describes the user interface.
    ui_filename = get_data_file('ui', '%s.ui' % (builder_file_name,))
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.set_translation_domain('transcribe')
    builder.add_from_file(ui_filename)
    return builder

def trim(timestring, digits=1):
    """
    Trim a time string to contain only a given number of digits
    
    """
    pos = timestring.find('.')
    if pos > -1:
        return timestring[:pos+1+digits]
    else:
        return timestring

def ns_to_time(ns):
    """
    Converts nanoseconds to a datetime.time object.
    
    :Parameters:
        - `ns`: Nanoseconds as int.
    
    :Return:
        - A datetime.time object.
        
    """
    h = ns / (60 * 60 * 1000000000)
    mod = ns % (60 * 60 * 1000000000)
    m = mod / (60 * 1000000000)
    mod = mod % (60 * 1000000000)
    s = mod / 1000000000
    mod = mod % 1000000000
    ms = mod / 1000
    return datetime.time(h, m, s, ms)
    
def time_to_ns(time):
    """
    Converts a datetime.time object to nanoseconds.
    
    :Parameters:
        - `time`: A datetime.time object.
    
    :Return:
        - Nanoseconds as int.
        
    """
    values = []
    values.append(time.hour * 60 * 60 * 1000000000)
    values.append(time.minute * 60 * 1000000000)
    values.append(time.second * 1000000000)
    values.append(time.microsecond * 1000)
    return sum(values)
    
def filepath_to_uri(path):
    file = gio.File(path=path)
    return file.get_uri()

def uri_to_filepath(uri):
    file = gio.File(uri=uri)
    return file.get_path()

