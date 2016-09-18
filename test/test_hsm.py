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
from example_hsm import test, s, s1, s11, s2, s21, s211


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
        for evt in 'giaddceegii':
            self.test.dispatch(evt)
