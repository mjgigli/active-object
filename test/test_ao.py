#!/usr/bin/env python
#
# @file test_ao.py
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

from tornado import testing

import ao
from example_ao import test


class test_ao(testing.AsyncTestCase):
    def setUp(self):
        super(test_ao, self).setUp()

        self.test = test(self.io_loop, self.evt_cb)

    def tearDown(self):
        # we can't post the Stop event, because the io_loop is already stopped
        # at this point, which means we can't write to the evt_q handler.
        self.test.dispatch(self.test.Stop())

        super(test_ao, self).tearDown()

    def evt_cb(self, evt):
        self.stop(evt)

    def test_init_transition(self):
        # verify that ao is of hsm by verifying init transition
        self.assertEqual(self.test.foo, False)

    def test_direct_post(self):
        # verify that posting to event queue triggers ao's hsm
        self.test.post(ao.event('i'))

        evt = self.wait()
        self.assertEqual(evt.sig, 'i')

    def test_publish(self):
        ao.publish(ao.event('i'))

        evt = self.wait()
        self.assertEqual(evt.sig, 'i')
