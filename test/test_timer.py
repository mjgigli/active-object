#!/usr/bin/env python
#
# @file test_timer.py
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

PERIOD = 5


class test_ao(testing.AsyncTestCase):
    def setUp(self):
        super(test_ao, self).setUp()

        self.count = -1
        self.periodic = ao.timer.periodic(self.io_loop, self.callback)
        self.one_shot = ao.timer.one_shot(self.io_loop, self.callback)

    def callback(self):
        if self.count > -1 and self.count < PERIOD:
            self.count += 1
        else:
            self.stop('timer done')

    def test_periodic_timer(self):
        self.count = 0
        self.periodic.expire_every(PERIOD)
        msg = self.wait()
        self.assertEqual(self.count, PERIOD)
        self.assertEqual('timer done', msg)

    def test_one_shot_timer(self):
        self.one_shot.expire_in(PERIOD)
        msg = self.wait()
        self.assertEqual('timer done', msg)
