#!/usr/bin/env python
#
# @file example_hsm.py
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


class test_evt(ao.event):
    def __init__(self, arg):
        super(test_evt, self).__init__()
        self.arg = arg


class test(ao.hsm):
    def state_handler(self, evt):
        if evt.sig == self.Init:
            self.foo = False
            self.inited.append(test)

            self.initial_transition(s2)
            return
        elif evt.sig == self.Entry:
            self.inited = []
            self.entered = []
            self.exited = []
            self.entered.append(test)
            return
        elif evt.sig == self.Exit:
            self.exited.append(test)
            return


class s(test):
    def state_handler(self, evt):
        if evt.sig == self.Init:
            self.inited.append(s)
            self.initial_transition(s11)
            return
        elif evt.sig == self.Entry:
            self.entered.append(s)
            return
        elif evt.sig == self.Exit:
            self.exited.append(s)
            return
        elif evt.sig == test_evt:
            if evt.arg == 'e':
                self.transition(s11)
                return
            elif evt.arg == 'i':
                if self.foo is True:
                    self.foo = False
                    return

        # always return self.Super for unhandled events
        return self.Super


class s1(s):
    def state_handler(self, evt):
        if evt.sig == self.Init:
            self.inited.append(s1)
            self.initial_transition(s11)
            return
        elif evt.sig == self.Entry:
            self.entered.append(s1)
            return
        elif evt.sig == self.Exit:
            self.exited.append(s1)
            return
        elif evt.sig == test_evt:
            if evt.arg == 'a':
                self.transition(s1)
                return
            elif evt.arg == 'b':
                self.transition(s11)
                return
            elif evt.arg == 'c':
                self.transition(s2)
                return
            elif evt.arg == 'd':
                if self.foo is False:
                    self.foo = True
                    self.transition(s)
                    return
            elif evt.arg == 'f':
                self.transition(s211)
                return
            elif evt.arg == 'i':
                return

        # always return self.Super for unhandled events
        return self.Super


class s11(s1):
    def state_handler(self, evt):
        if evt.sig == self.Init:
            self.inited.append(s11)
            return
        elif evt.sig == self.Entry:
            self.entered.append(s11)
            return
        elif evt.sig == self.Exit:
            self.exited.append(s11)
            return
        elif evt.sig == test_evt:
            if evt.arg == 'd':
                if self.foo is True:
                    self.foo = False
                    self.transition(s1)
                    return
            elif evt.arg == 'g':
                self.transition(s211)
                return
            elif evt.arg == 'h':
                self.transition(s)
                return

        # always return self.Super for unhandled events
        return self.Super


class s2(s):
    def state_handler(self, evt):
        if evt.sig == self.Init:
            self.inited.append(s2)
            self.initial_transition(s211)
            return
        elif evt.sig == self.Entry:
            self.entered.append(s2)
            return
        elif evt.sig == self.Exit:
            self.exited.append(s2)
            return
        elif evt.sig == test_evt:
            if evt.arg == 'c':
                self.transition(s1)
                return
            elif evt.arg == 'f':
                self.transition(s11)
                return
            elif evt.arg == 'i':
                if self.foo is False:
                    self.foo = True
                    return

        # always return self.Super for unhandled events
        return self.Super


class s21(s2):
    def state_handler(self, evt):
        if evt.sig == self.Init:
            self.inited.append(s21)
            self.initial_transition(s211)
            return
        elif evt.sig == self.Entry:
            self.entered.append(s21)
            return
        elif evt.sig == self.Exit:
            self.exited.append(s21)
            return
        elif evt.sig == test_evt:
            if evt.arg == 'a':
                self.transition(s21)
                return
            elif evt.arg == 'b':
                self.transition(s211)
                return
            elif evt.arg == 'g':
                self.transition(s11)
                return

        # always return self.Super for unhandled events
        return self.Super


class s211(s21):
    def state_handler(self, evt):
        if evt.sig == self.Init:
            self.inited.append(s211)
            return
        elif evt.sig == self.Entry:
            self.entered.append(s211)
            return
        elif evt.sig == self.Exit:
            self.exited.append(s211)
            return
        elif evt.sig == test_evt:
            if evt.arg == 'd':
                self.transition(s21)
                return
            elif evt.arg == 'h':
                self.transition(s)
                return

        # always return self.Super for unhandled events
        return self.Super
