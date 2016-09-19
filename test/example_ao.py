#!/usr/bin/env python
#
# @file example_ao.py
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

import ao


test_sigs = [
    'i',
]


class test(ao.ao):
    def __init__(self, io_loop, cb=None):
        super(test, self).__init__(io_loop)

        self.cb = cb

    def state_handler(self, evt):
        if evt.sig == self.Init:
            self.initial_transition(s)
            return
        elif evt.sig == self.Entry:
            # any ao initialization can go here
            self.subscribe(test_sigs)
            self.foo = False
            return
        elif evt.sig == self.Stop:
            # any ao destruction can go here
            self.unsubscribe(test_sigs)


class s(test):
    def state_handler(self, evt):
        if evt.sig == 'i':
            self.foo = True
            if self.cb is not None:
                self.cb(evt)
            return

        # always return self.Super for unhandled events
        return self.Super
