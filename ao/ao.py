#!/usr/bin/env python
#
# @file ao.py
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
# ao module implements an active object as a subclass of hsm.
#

import logging
from multiprocessing import Queue
from Queue import Empty, Full
from tornado.ioloop import IOLoop

from hsm import hsm
from signals import dispatcher


def publish(evt):
    """Publish the given event to all subscribed hsms."""
    dispatcher.publish(evt.sig, evt)


class active_object(hsm):
    """active_object class implements the active-object design pattern.

    active_object is a subclass of hsm, so application developers are expected
    to implement state classes and state handler methods.
    """

    def __init__(self, io_loop):
        super(active_object, self).__init__()

        # active-object class members
        self._evt_q = Queue()
        self._io_loop = io_loop

        # always subscribe to Stop events
        self.subscribe([self.Stop()])

        # monitor the event queue for events
        self._io_loop.add_handler(self._evt_q._reader.fileno(),
                                  self._evt_handler,
                                  IOLoop.READ)

    def _evt_handler(self, fd, events):
        try:
            evt = self._evt_q.get_nowait()
        except Empty:
            logging.error("Active object event queue is empty.")

        # dispatch event to active_object's hsm
        self.dispatch(evt)

        # cleanup if event was a stop event
        if evt.sig == self.Stop:
            self._cleanup()

    def _cleanup(self):
        self.unsubscribe([self.Stop()])
        self.io_loop.remove_handler(self.evt_q._reader.fileno())

    def stop(self):
        self.post(self.Stop())

    def post(self, evt):
        try:
            self._evt_q.put_nowait(evt)
        except Full:
            logging.error("Active object event queue is full, dropping event.")

    def subscribe(self, evts):
        """Subscribe to all events passed in."""
        for evt in evts:
            dispatcher.subscribe(evt, self.post)

    def unsubscribe(self, evts):
        """Unsubscribe to all events passed in."""
        for evt in evts:
            dispatcher.unsubscribe(evt, self.post)
