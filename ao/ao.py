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


class ao(hsm):
    """ao class implements the active-object design pattern.

    ao is a subclass of hsm, so application developers are expected to
    implement state classes and state handler methods.
    """

    def __init__(self, io_loop):
        super(ao, self).__init__()

        # active-object class members
        self._evt_q = Queue()
        self._io_loop = io_loop

        # monitor the event queue for events
        self._io_loop.add_handler(self._evt_q._reader.fileno(),
                                  self._evt_handler,
                                  IOLoop.READ)

    def _evt_handler(self, fd, events):
        try:
            evt = self._evt_q.get_nowait()
        except Empty:
            logging.error("Active object event queue is empty.")

        # dispatch event to ao's hsm
        self.dispatch(evt)

    def post(self, evt):
        try:
            self._evt_q.put_nowait(evt)
        except Full:
            logging.error("Active object event queue is full, dropping event.")
