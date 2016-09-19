#!/usr/bin/env python
#
# @file hsm.py
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
# hsm is a simple implementation of a hierarchical state machine (HSM).
#

import logging
from event import event


class Init(event):
    """Init signal for HSM Initial Transitions."""
    pass


class Entry(event):
    """Entry signal for HSM Entry events."""
    pass


class Exit(event):
    """Exit signal for HSM Exit events."""
    pass


class Super(event):
    """Super signal used to pass up current signal to the Super State."""
    pass


###############################################################################
class hsm(object):
    """Base class to inherit from to create a HSM."""
    Init = Init
    Entry = Entry
    Exit = Exit
    Super = Super

    def __init__(self):
        """Dispatch Entry and Init signals at HSM creation."""
        self.state_handler(Entry())
        self.state_handler(Init())

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__

    def dispatch(self, evt):
        """Public dispatch function used to dispatch events to state machine.

        This function calls the state state_handler function within the
        context of the caller,
        """
        # dispatch signal up the state hierarchy until it is handled
        for self.__state in self.__class__.__mro__:
            if self.__state.state_handler(self, evt) != Super:
                logging.debug("Handled %s from %s" % (evt, self.__state))
                return

    def state_handler(self, evt):
        """State handler function to be overridden by all hsm subclasses."""
        raise NotImplementedError()

    def initial_transition(self, state):
        logging.debug("Initial transition: %s" % self)
        # get target state hierarchy
        target_hierarchy = state.__mro__
        assert self.__class__ in target_hierarchy, \
            "Initial transition must be to a substate"

        # get target state hierarchy below current state
        idx = target_hierarchy.index(self.__class__)
        target_hierarchy = target_hierarchy[:idx]

        # enter nested states to the target
        for s in reversed(target_hierarchy):
            self.__class__ = s
            logging.debug("Enter: %s" % self)
            self.state_handler(Entry())

        # take the initial transition
        self.__class__ = state
        self.state_handler(Init())

    def transition(self, state):
        """Perform state transition.

        This will handle dispatching all exit events when leaving states,
        and all entry events when entering new states, as well as any
        initial transitions.
        """
        # save off hierarchy of transition target state
        target_hierarchy = state.__mro__

        # save off hierarchy of current state, excluding current state
        self_hierarchy = iter(self.__class__.__mro__[1:])

        # exit states until transition source
        while self.__class__ != self.__state:
            logging.debug("Exit: %s" % self)
            self.state_handler(Exit())
            self.__class__ = next(self_hierarchy)

        if self.__class__ == state:
            # special case: transition to self
            logging.debug("Exit: %s" % self)
            self.state_handler(Exit())
            logging.debug("Enter: %s" % self)
            self.state_handler(Entry())
        else:
            # more complicated transition...
            # exit states until finding the least common ancestor
            while (self.__class__ not in target_hierarchy):
                logging.debug("Exit: %s" % self)
                self.state_handler(Exit())
                self.__class__ = next(self_hierarchy)

            # enter the target state, if not already in target state
            if self.__class__ != state:
                start = target_hierarchy.index(self.__class__)
                transition_path = target_hierarchy[:start]
                for state in reversed(transition_path):
                    self.__class__ = state
                    logging.debug("Entry: %s" % self)
                    self.state_handler(Entry())

        # finally, take the initial transition
        self.state_handler(Init())
