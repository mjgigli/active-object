#!/usr/bin/env python
#
# @file  signals.py
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
# signals is a publish-subscribe module that provides users the ability to
# subscribe to and publish events.
#

import inspect
from weakref import WeakSet, WeakKeyDictionary
from collections import defaultdict


class signal(object):
    """Data structure to store callbacks for a single signal or channel."""
    def __init__(self):
        self._functions = WeakSet()
        self._methods = WeakKeyDictionary()

    def __call__(self, *args, **kwargs):
        # call signal's regular module function callbacks
        for f in self._functions:
            f(*args, **kwargs)

        for obj, receivers in self._methods.iteritems():
            for f in receivers:
                f(obj, *args, **kwargs)

    def subscribe(self, receiver):
        """Subscribe the receiver with this signal."""
        if inspect.ismethod(receiver):
            if receiver.__self__ not in self._methods:
                self._methods[receiver.__self__] = set()

            self._methods[receiver.__self__].add(receiver.__func__)
        else:
            self._functions.add(receiver)

    def unsubscribe(self, receiver):
        """Unsubscribe the receiver from this signal."""
        if inspect.ismethod(receiver):
            if receiver.__self__ in self._methods:
                self._methods[receiver.__self__].remove(receiver.__func__)
        else:
            if receiver in self._functions:
                self._functions.remove(receiver)

    def unsubscribe_all(self):
        """Unsubscribe all receives from this signal."""
        self._functions.clear()
        self._methods.clear()


class signal_dispatcher(object):
    """Signal dispatcher class. Manages signals and their receivers."""
    def __init__(self):
        self.signals = defaultdict(signal)

    def publish(self, signal_id, *args, **kwargs):
        """Call all subscribed receivers with given signal."""
        self.signals[signal_id](*args, **kwargs)

    def subscribe(self, signal_id, receiver):
        """Subscribe the receiver function with the given signal."""
        self.signals[signal_id].subscribe(receiver)

    def unsubscribe(self, signal_id, receiver):
        """Unsubscribe the receiver function with the given signal."""
        self.signals[signal_id].unsubscribe(receiver)

    def unsubscribe_all(self, signal_id=None):
        """Unsubscribe either all receivers or all receivers for a signal.

        If signal_id is not given, unsubscribe ALL receivers.
        Otherwise, unsubscribe only the receivers from the given signal.
        """
        if signal_id is None:
            self.signals.clear()
        else:
            self.signals[signal_id].unsubscribe_all()


dispatcher = signal_dispatcher()
publish = dispatcher.publish
subscribe = dispatcher.subscribe
unsubscribe = dispatcher.unsubscribe
