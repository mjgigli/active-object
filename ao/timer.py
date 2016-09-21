#!/usr/bin/env python
#
# @file timer.py
#
# @author Matt Gigli <mjgigli@gmail.com>
#
# @section LICENSE
#
# The MIT License (MIT)
# Copyright (c) 2016 Matt Gigli
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# @section DESCRIPTION
#
# timer is a versatile class that provides both a one-shot and periodic timer
#

import tornado.ioloop
from functools import partial


class periodic(object):
    """Periodic timer class."""
    def __init__(self, io_loop, callback):
        self._io_loop = io_loop
        self._callback = callback
        self._periodic = None

    def expire_every(self, period, start_in=0):
        """Start the periodic timer with given period and delay.

        This method is safe to call from any thread.
        """
        # create a periodic timer
        self._periodic = tornado.ioloop.PeriodicCallback(self._callback,
                                                         period,
                                                         self._io_loop)
        if start_in > 0:
            # set timer to start the periodic timer
            add_timeout = partial(self._io_loop.add_timeout,
                                  start_in,
                                  self._periodic.start)
            self._io_loop.add_callback(add_timeout)
        else:
            # start timer right away
            self._io_loop.add_callback(self._periodic.start)

    def disarm(self):
        """Stop the periodic timer, if running.

        This method is safe to call from any thread.
        """
        self._io_loop.add_callback(self._stop)

    def _stop(self):
        if self._periodic:
            self._periodic.stop()
            self._periodic = None


class one_shot(object):
    """One shot timer class."""
    def __init__(self, io_loop, callback):
        # use the periodic timer to implement a one-shot timer
        self._timer = periodic(io_loop, self._handle_expire)
        self._callback = callback

    def _handle_expire(self):
        # disable the periodic timer, since this is a one-shot
        self._timer.disarm()
        self._callback()

    def expire_in(self, duration):
        """Start the one-shot timer to expire in duration seconds.

        This method is safe to call from any thread.
        """
        self._timer.expire_every(duration)

    def disarm(self):
        """Stop the one-shot timer, if running.

        This method is safe to call from any thread.
        """
        self._timer.disarm()
