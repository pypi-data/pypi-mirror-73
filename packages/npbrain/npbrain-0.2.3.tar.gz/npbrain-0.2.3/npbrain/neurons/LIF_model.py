import numpy as np

from npbrain.core import ode_generator
from npbrain.core import sde_generator
from npbrain.core.neuron import *
from npbrain.profile import get_dt
from npbrain.utils import helper

__all__ = [
    'LIF'
]


def LIF(geometry, method='euler', **kwargs):
    """Leaky integrate-and-fire neuron model.

    Parameters
    ----------
    geometry : int, list, tuple
        The geometry of neuron group. If an integer is given, it is the size
        of the population.
    method : str, callable, dict
        The numerical integration method. Either a string with the name of a
        registered method (e.g. "euler") or a function.
    kwargs : dict
        Neuron parameters.

    Returns
    -------
    neurons : Neurons
        The created neuron group.
    """
    # base
    # ----
    name = kwargs.pop('name', 'LIF')
    var2index = {'V': 0}
    num, geometry = format_geometry(geometry)
    dt = kwargs.pop('dt', get_dt())

    # parameters
    # ------------------
    tau = kwargs.pop('tau', 10.)
    V_reset = kwargs.pop('V_reset', 0.)
    Vth = kwargs.pop('Vth', 10.)
    noise = kwargs.pop('noise', 0.)
    ref = kwargs.pop('ref', 0.)
    # check parameters
    helper.check_params(kwargs)

    # integration function
    # --------------------
    f = helper.autojit(lambda V, t, Isyn: (-V + V_reset + Isyn) / tau)
    if noise == 0.:
        int_f = ode_generator(f, dt)
    else:
        int_f = sde_generator(f, noise / tau, dt, method)

    # init state
    # -----------
    state = initial_neu_state(1, num)
    state[0] = V_reset

    # update function
    # -------------------
    if ref > 0.:
        def update_state(neu_state, t):
            not_ref = (t - neu_state[-2]) > ref
            not_ref_idx = np.where(not_ref)[0]
            neu_state[-5] = not_ref
            V = neu_state[0][not_ref_idx]
            Isyn = neu_state[-1][not_ref_idx]
            V = int_f(V, t, Isyn)
            neu_state[0][not_ref_idx] = V
            spike_idx = judge_spike(neu_state, Vth, t)
            neu_state[0][spike_idx] = V_reset
    else:
        def update_state(neu_state, t):
            neu_state[0] = int_f(neu_state[0], t, neu_state[-1])
            spike_idx = judge_spike(neu_state, Vth, t)
            neu_state[0][spike_idx] = V_reset

    return Neurons(**locals())

