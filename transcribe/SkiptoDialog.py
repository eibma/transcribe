# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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

import ctypes
import datetime

import gtk

from transcribe.helpers import get_builder, ns_to_time, time_to_ns, trim

import gettext
from gettext import gettext as _
gettext.textdomain('transcribe')

class SkiptoDialog(gtk.Dialog):
    __gtype_name__ = "SkiptoDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated SkiptoDialog object.
        """
        builder = get_builder('SkiptoDialog')
        new_object = builder.get_object('skipto_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a SkiptoDialog object with it in order to
        finish initializing the start of the new SkiptoDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)
        self.time_format = '%M:%S.%f'
        self.spinbutton = self.builder.get_object('spinbutton_time')
        
    def on_spinbutton_time_input(self, spinbutton, value_ptr):
        text = spinbutton.get_text()
        try:
            time = datetime.datetime.strptime(text, self.time_format).time()
        except ValueError:
            return -1
        double = ctypes.c_double.from_address(hash(value_ptr))
        double.value = float(time_to_ns(time))
        return True
        
    def on_spinbutton_time_output(self, spinbutton):
        time = ns_to_time(int(spinbutton.get_value()))
        text = trim(time.strftime(self.time_format))
        spinbutton.set_text(text)
        return True

    def ok(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns gtk.RESONSE_OK from run().
        """
        pass

    def cancel(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """
        pass


if __name__ == "__main__":
    dialog = SkiptoDialog()
    dialog.show()
    gtk.main()
