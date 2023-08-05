import numpy as np
from npbrain.core.neuron import format_geometry
from npbrain.core.neuron import Neurons
from npbrain.core.neuron import initial_neu_state

from npbrain import profile

num_inputs = 0


__all__ = [
    'freq_inputs'
]


def freq_inputs(geometry, freq, start_time=0., **kwargs):
    # base
    # ------
    global num_inputs
    name = kwargs.pop('name', 'inputs-{}'.format(num_inputs))
    num_inputs += 1
    var2index = dict()
    dt = kwargs.pop('dt', profile.get_dt())
    num, geometry = format_geometry(geometry)

    # state
    # ------
    state = initial_neu_state(1, num)
    state[0, 0] = start_time

    # functions
    # ----------
    def update_state(neu_state, t):
        if t >= neu_state[0, 0]:
            neu_state[-3] = 1.
            neu_state[-2] = t
            neu_state[0, 0] += 1000 / freq
        else:
            neu_state[-3] = 0.

    return Neurons(**locals())

