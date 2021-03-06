#!/usr/bin/env python
#
# @file event.py
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
# event module implements a generic event object for hsms and aos.
#


class event(object):
    """The event class is the base class for hsm events.

    The _sig class member can be overriden if the application developer wishes
    the sig of the event to be something other than the type of the event. e.g.
    they may wish to use a simple string as the sig, or some other object.

    The sig property can always be used to differentiate events from one
    another. It will detect whether the _sig member has been overriden; if
    it has, it will use the _sig value and if it hasn't it will return the
    event class type.
    """
    def __init__(self, _sig=None):
        self._sig = _sig

    @property
    def sig(self):
        if self._sig is None:
            return self.__class__
        else:
            return self._sig
