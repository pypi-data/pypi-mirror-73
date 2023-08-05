import numpy as np

from npbrain.core import ode_generator
from npbrain.core import sde_generator
from npbrain.core.neuron import *
from npbrain.profile import get_dt
from npbrain.utils.helper import autojit
from npbrain.utils.helper import check_params

__all__ = [
    'Izhikevich'
]


def Izhikevich(geometry, mode=None, method='euler', **kwargs):
    """Izhikevich two-variable neuron model.

    Parameters
    ----------
    mode : None, str
        At least twenty firing modes have beed provides by Izhikevich.
        One can specify the preferred firing mode to get the corresponding
        neuron group.
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
    # ---------
    name = kwargs.pop('name', 'Izhikevich')
    var2index = {'V': 0, 'u': 1}
    num, geometry = format_geometry(geometry)
    dt = kwargs.pop('dt', get_dt())

    # mode
    # ---------
    if mode is None:
        pars = [0.02, 0.20, -65., 8.]
    elif mode in ['tonic', 'tonic spiking']:
        pars = [0.02, 0.40, -65.0, 2.0]
    elif mode in ['phasic', 'phasic spiking']:
        pars = [0.02, 0.25, -65.0, 6.0]
    elif mode in ['tonic bursting']:
        pars = [0.02, 0.20, -50.0, 2.0]
    elif mode in ['phasic bursting']:
        pars = [0.02, 0.25, -55.0, 0.05]
    elif mode in ['mixed mode']:
        pars = [0.02, 0.20, -55.0, 4.0]
    elif mode in ['SFA', 'spike frequency adaptation']:
        pars = [0.01, 0.20, -65.0, 8.0]
    elif mode in ['Class 1', 'class 1']:
        pars = [0.02, -0.1, -55.0, 6.0]
    elif mode in ['Class 2', 'class 2']:
        pars = [0.20, 0.26, -65.0, 0.0]
    elif mode in ['spike latency', ]:
        pars = [0.02, 0.20, -65.0, 6.0]
    elif mode in ['subthreshold oscillation', ]:
        pars = [0.05, 0.26, -60.0, 0.0]
    elif mode in ['resonator', ]:
        pars = [0.10, 0.26, -60.0, -1.0]
    elif mode in ['integrator', ]:
        pars = [0.02, -0.1, -55.0, 6.0]
    elif mode in ['rebound spike', ]:
        pars = [0.03, 0.25, -60.0, 4.0]
    elif mode in ['rebound burst', ]:
        pars = [0.03, 0.25, -52.0, 0.0]
    elif mode in ['threshold variability', ]:
        pars = [0.03, 0.25, -60.0, 4.0]
    elif mode in ['bistability', ]:
        pars = [1.00, 1.50, -60.0, 0.0]
    elif mode in ['DAP', 'depolarizing afterpotential']:
        pars = [1.00, 0.20, -60.0, -21.0]
    elif mode in ['accomodation', ]:
        pars = [0.02, 1.00, -55.0, 4.0]
    elif mode in ['inhibition-induced spiking', ]:
        pars = [-0.02, -1.00, -60.0, 8.0]
    elif mode in ['inhibition-induced bursting', ]:
        pars = [-0.026, -1.00, -45.0, 0.0]
    else:
        raise ValueError('Unknown spiking mode: "{}"'.format(mode))

    # parameters
    # --------------
    a = kwargs.pop('a', pars[0])
    b = kwargs.pop('b', pars[1])
    c = kwargs.pop('c', pars[2])
    d = kwargs.pop('d', pars[3])

    ref = kwargs.pop('ref', 0.)
    noise = kwargs.pop('noise', 0.0)
    Vth = kwargs.pop('Vth', 30.)
    Vr = kwargs.pop('Vr', -65.)
    check_params(kwargs)

    # integration functions
    # ----------------------
    f_u = autojit(lambda u, t, V: a * (b * V - u))
    int_u = ode_generator(f_u, dt, method)
    f_V = autojit(lambda V, t, u, Isyn: 0.04 * V * V + 5 * V + 140 - u + Isyn)
    if noise == 0.:
        int_V = ode_generator(f_V, dt, method)
    else:
        int_V = sde_generator(f_V, noise, dt, method)

    # init state
    # ----------------------

    def init_state(state_, Vr_):
        state_[0] = np.ones(num) * Vr_
        state_[1] = state_[0] * b

    state = initial_neu_state(2, num)
    init_state(state, Vr)

    # update state
    # ----------------------

    if ref > 0.:
        def update_state(neu_state, t):
            not_ref = (t - neu_state[-2]) > ref
            not_ref_idx = np.where(not_ref)[0]
            V = neu_state[0][not_ref_idx]
            u = neu_state[1][not_ref_idx]
            Isyn = neu_state[-1][not_ref_idx]
            u_new = int_u(u, t, V)
            V_new = int_V(V, t, u, Isyn)
            neu_state[0] = V_new
            neu_state[1] = u_new
            spike_idx = judge_spike(neu_state, Vth, t)
            neu_state[0][spike_idx] = c
            neu_state[1][spike_idx] += d
    else:
        def update_state(neu_state, t):
            V, u, Isyn = neu_state[0], neu_state[1], neu_state[-1]
            neu_state[0] = int_V(V, t, u, Isyn)
            neu_state[1] = int_u(u, t, V)
            spike_idx = judge_spike(neu_state, Vth, t)
            neu_state[0][spike_idx] = c
            neu_state[1][spike_idx] += d

    return Neurons(**locals())
