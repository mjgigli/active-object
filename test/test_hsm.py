#!/usr/bin/env python
#
# @file test_hsm.py
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
# hsm unit test.
#

import unittest
from ao.hsm import hsm, Entry, Init, Super, Exit


class test(hsm):
    def state_handler(self, evt):
        if evt == Init:
            self.foo = False
            self.inited.append(test)

            self.initial_transition(s2)
            return
        elif evt == Entry:
            self.inited = []
            self.entered = []
            self.exited = []
            self.entered.append(test)
            return
        elif evt == Exit:
            self.exited.append(test)
            return


class s(test):
    def state_handler(self, evt):
        if evt == Init:
            self.inited.append(s)
            self.initial_transition(s11)
            return
        elif evt == Entry:
            self.entered.append(s)
            return
        elif evt == Exit:
            self.exited.append(s)
            return
        elif evt == 'e':
            self.transition(s11)
            return
        elif evt == 'i':
            if self.foo is True:
                self.foo = False
                return

        # always return Super for unhandled events
        return Super


class s1(s):
    def state_handler(self, evt):
        if evt == Init:
            self.inited.append(s1)
            self.initial_transition(s11)
            return
        elif evt == Entry:
            self.entered.append(s1)
            return
        elif evt == Exit:
            self.exited.append(s1)
            return
        elif evt == 'a':
            self.transition(s1)
            return
        elif evt == 'b':
            self.transition(s11)
            return
        elif evt == 'c':
            self.transition(s2)
            return
        elif evt == 'd':
            if self.foo is False:
                self.foo = True
                self.transition(s)
                return
        elif evt == 'f':
            self.transition(s211)
            return
        elif evt == 'i':
            return

        # always return Super for unhandled events
        return Super


class s11(s1):
    def state_handler(self, evt):
        if evt == Init:
            self.inited.append(s11)
            return
        elif evt == Entry:
            self.entered.append(s11)
            return
        elif evt == Exit:
            self.exited.append(s11)
            return
        elif evt == 'd':
            if self.foo is True:
                self.foo = False
                self.transition(s1)
                return
        elif evt == 'g':
            self.transition(s211)
            return
        elif evt == 'h':
            self.transition(s)
            return

        # always return Super for unhandled events
        return Super


class s2(s):
    def state_handler(self, evt):
        if evt == Init:
            self.inited.append(s2)
            self.initial_transition(s211)
            return
        elif evt == Entry:
            self.entered.append(s2)
            return
        elif evt == Exit:
            self.exited.append(s2)
            return
        elif evt == 'c':
            self.transition(s1)
            return
        elif evt == 'f':
            self.transition(s11)
            return
        elif evt == 'i':
            if self.foo is False:
                self.foo = True
                return

        # always return Super for unhandled events
        return Super


class s21(s2):
    def state_handler(self, evt):
        if evt == Init:
            self.inited.append(s21)
            self.initial_transition(s211)
            return
        elif evt == Entry:
            self.entered.append(s21)
            return
        elif evt == Exit:
            self.exited.append(s21)
            return
        elif evt == 'a':
            self.transition(s21)
            return
        elif evt == 'b':
            self.transition(s211)
            return
        elif evt == 'g':
            self.transition(s11)
            return

        # always return Super for unhandled events
        return Super


class s211(s21):
    def state_handler(self, evt):
        if evt == Init:
            self.inited.append(s211)
            return
        elif evt == Entry:
            self.entered.append(s211)
            return
        elif evt == Exit:
            self.exited.append(s211)
            return
        elif evt == 'd':
            self.transition(s21)
            return
        elif evt == 'h':
            self.transition(s)
            return

        # always return Super for unhandled events
        return Super


def start_in_state(hsm_h, state):
    """Put hsm in given state, without performing transitions"""
    # set the state
    hsm_h.__class__ = state

    # reset the recording variables
    hsm_h.inited = []
    hsm_h.entered = []
    hsm_h.exited = []


class test_hsm(unittest.TestCase):
    def setUp(self):
        self.test = test()

    def test_init_transition(self):
        self.assertListEqual(self.test.inited, [test, s2, s211])
        self.assertListEqual(self.test.entered, [test, s, s2, s21, s211])
        self.assertListEqual(self.test.exited, [])

    def test_self_transition(self):
        start_in_state(self.test, s11)
        self.test.dispatch('a')
        self.assertListEqual(self.test.inited, [s1, s11])
        self.assertListEqual(self.test.entered, [s1, s11])
        self.assertListEqual(self.test.exited, [s11, s1])

    def test_super_to_substate_transition(self):
        start_in_state(self.test, s11)
        self.test.dispatch('b')
        self.assertListEqual(self.test.inited, [s11])
        self.assertListEqual(self.test.entered, [s11])
        self.assertListEqual(self.test.exited, [s11])

    def test_same_super_state_transition(self):
        start_in_state(self.test, s11)
        self.test.dispatch('c')
        self.assertListEqual(self.test.inited, [s2, s211])
        self.assertListEqual(self.test.entered, [s2, s21, s211])
        self.assertListEqual(self.test.exited, [s11, s1])

    def test_substate_to_super_transition(self):
        start_in_state(self.test, s211)
        self.test.dispatch('d')
        self.assertListEqual(self.test.inited, [s21, s211])
        self.assertListEqual(self.test.entered, [s211])
        self.assertListEqual(self.test.exited, [s211])

    def test_super_to_sub_substate_transition(self):
        start_in_state(self.test, s11)
        self.test.dispatch('e')
        self.assertListEqual(self.test.inited, [s11])
        self.assertListEqual(self.test.entered, [s1, s11])
        self.assertListEqual(self.test.exited, [s11, s1])

    def test_same_super_to_substate_transition(self):
        start_in_state(self.test, s11)
        self.test.dispatch('f')
        self.assertListEqual(self.test.inited, [s211])
        self.assertListEqual(self.test.entered, [s2, s21, s211])
        self.assertListEqual(self.test.exited, [s11, s1])

    def test_same_super_substate_to_substate_transition(self):
        start_in_state(self.test, s11)
        self.test.dispatch('g')
        self.assertListEqual(self.test.inited, [s211])
        self.assertListEqual(self.test.entered, [s2, s21, s211])
        self.assertListEqual(self.test.exited, [s11, s1])

    def test_many_dispatches(self):
        print 'Starting many inputs test'
        for evt in 'giaddceegii':
            self.test.dispatch(evt)
