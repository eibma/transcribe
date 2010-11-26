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

import logging
logger = logging.getLogger('fileinfo')

import gio

POSITION_ATTRIBUTE = "metadata::totem::position"
MSECOND = 1000000


class FileInfo (object):
    """
    Query and store information about a given file.
    
    This class abstracts several metadata storage systems in favor of a simple
    interface.
    
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self._position = None
        
    def _get_position(self):
        if self._position is not None:
            return self._position
        file = gio.File(path=self.filepath)
        info = file.query_info(POSITION_ATTRIBUTE)
        position = info.get_attribute_as_string(POSITION_ATTRIBUTE)
        if position:
            position = int(position) * MSECOND
        self._position = position
        logger.debug('Get position: %s' % position)
        return position
    
    def _set_position(self, position):
        logger.debug('Set position: %s' % position)
        self._position = position
        file = gio.File(path=self.filepath)
        info = file.query_info(POSITION_ATTRIBUTE)
        info.set_attribute_string(POSITION_ATTRIBUTE, str(position / MSECOND))
        file.set_attributes_from_info(info)
        
    position = property(_get_position, _set_position)

