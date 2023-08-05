#------------------------------------------------------------------------------
# Copyright (c) 2018, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
"""Test the signal connectors.

"""
import gc
import operator
import sys

import pytest
from atom.api import Atom, Signal, Int


def test_signalconnector_lifecycle():
    """Test creating and destroying an event binder.

    We create enough event binder to exceed the freelist length and fully
    deallocate some.

    """
    class SignalAtom(Atom):
        s = Signal()

    signal_connectors = [SignalAtom.s for i in range(512)]
    for i, e in enumerate(signal_connectors):
        signal_connectors[i] = None
        del e
        gc.collect()

    atom = SignalAtom()
    sc = atom.s
    assert gc.get_referents(sc) == [SignalAtom.s, atom]


def test_signalconnector_cmp():
    """Test comparing event binders.

    """
    class EventAtom(Atom):
        s1 = Signal()
        s2 = Signal()

    a = EventAtom()
    assert a.s1 == a.s1
    assert not a.s1 == a.s2
    assert not a.s1 == 1

    if sys.version_info >= (3,):
        for op in ('lt', 'le', 'gt', 'ge'):
            with pytest.raises(TypeError):
                getattr(operator, op)(a.s1, 1)
