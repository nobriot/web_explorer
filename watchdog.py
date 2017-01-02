# -*- coding: utf-8 -*-
"""
watchdog.py
Small module allowing to throw exceptions when a script hangs up
Copyright (C) 2016  Nicolas Obriot - Sabrina Woltmann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

@author: Sabrina Woltmann, Nicolas Obriot
Created on Mon Jan  2 17:28:55 2017
Last modified : 02/01/2017 by Nicolas Obriot
"""

# Imports
from threading import Timer

#Watchdog timeout exception
class watchdogException(Exception):
    ''' This class is the error '''
    def __init__(self, message):
        # Call the base class constructor (exception) with the parameters it needs
        super(watchdogException, self).__init__(message)


# Our watchdog class
class Watchdog():
    ''' Watchdog class, used to ensure that the script execution is still alive'''
    def __init__(self, timeout=60):
        ''' Class constructor. Initialize the timeout in case the watchdog is 
        not "kicked" with the kick() function. Timeout is in seconds and the 
        default is a minute. '''
        self._timeout = timeout

    def kick(self):
        ''' Function that's used to kick the watchdog. i.e. preventing that it
        reaches the timeout. '''
        #Bascially just restart the timer
        self.stop()
        self.start()
        
    def start(self):
        ''' Starts the watchdog timer. '''
        self._timer = Timer(self._timeout, self._default_exception_handler)
        self._timer.daemon = True
        self._timer.start()
        return

    def stop(self):
        ''' Stops the watchdog timer. '''
        self._timer.cancel()
        
        
    def _default_exception_handler(self):
        ''' The exception that is raised when the Watchdog is not kicked '''
        raise watchdogException("Watchdog was not kicked in "+str(self._timeout) + " seconds")


        
        
