import numpy as np

from npbrain.core import ode_generator
from npbrain.core import sde_generator
from npbrain.core.neuron import *
from npbrain.profile import get_dt
from npbrain.utils.helper import clip
from npbrain.utils.helper import autojit
from npbrain.utils.helper import check_params

__all__ = [
    'HH'
]


def HH(geometry, method='euler', **kwargs):
    """The Hodgkin–Huxley neuron model.

    The Hodgkin–Huxley model can be thought of as a differential equation
    with four state variables, :math:`v(t)`, :math;`m(t)`, :math:`n(t)`, and
    :math:`h(t)`, that change with respect to time :math:`t`.

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
    name = kwargs.pop('name', 'HH')
    var2index = {'V': 0, 'm': 1, 'h': 2, 'n': 3}
    dt = kwargs.pop('dt', get_dt())
    num, geometry = format_geometry(geometry)

    # parameters
    # ------------------
    # Na channel
    E_Na = kwargs.pop('E_Na', 50)
    g_Na = kwargs.pop('g_Na', 120)

    # K channel
    E_K = kwargs.pop('E_K', -77)
    g_K = kwargs.pop('g_K', 36)

    # Leak current
    E_Leak = kwargs.pop('E_Leak', -54.387)
    g_Leak = kwargs.pop('g_Leak', 0.03)

    # Membrane potential
    C = kwargs.pop('C', 1.0)
    Vr = kwargs.pop('Vr', -65.0)
    Vth = kwargs.pop('Vth', 20.0)

    # noise
    noise = kwargs.pop('noise', 0.)

    # others
    check_params(kwargs)

    # integration function
    # -----------------------
    # equation of INa
    f_m_alpha = autojit(lambda V: 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10)))
    f_m_beta = autojit(lambda V: 4.0 * np.exp(-(V + 65) / 18))
    f_h_alpha = autojit(lambda V: 0.07 * np.exp(-(V + 65) / 20.))
    f_h_beta = autojit(lambda V: 1 / (1 + np.exp(-(V + 35) / 10)))
    f_m = autojit(lambda m, t, V: f_m_alpha(V) * (1 - m) - f_m_beta(V) * m)
    f_h = autojit(lambda h, t, V: f_h_alpha(V) * (1 - h) - f_h_beta(V) * h)
    int_m = ode_generator(f_m, dt, method)
    int_h = ode_generator(f_h, dt, method)
    fo_INa = autojit(lambda V, m, h: g_Na * m * m * m * h * (V - E_Na))

    # equation of IK
    f_n_alpha = autojit(lambda V: 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10)))
    f_n_beta = autojit(lambda V: 0.125 * np.exp(-(V + 65) / 80))
    f_n = autojit(lambda n, t, V: f_n_alpha(V) * (1 - n) - f_n_beta(V) * n)
    int_n = ode_generator(f_n, dt, method)
    fo_IK = autojit(lambda V, n: g_K * n ** 4 * (V - E_K))

    # equation of ILeak
    fo_ILeak = autojit(lambda V: g_Leak * (V - E_Leak))

    # equation of V
    V_f = autojit(lambda V, t, Icur, Isyn: (Icur + Isyn) / C)
    if noise == 0.:
        int_V = ode_generator(V_f, dt, method)
    else:
        int_V = sde_generator(V_f, noise / C, dt, method)

    # init state
    # -----------
    def init_state(state_, Vr_):
        V = np.ones(num) * Vr_
        state_[0] = V  # V
        state_[1] = f_m_alpha(V) / (f_m_alpha(V) + f_m_beta(V))  # m
        state_[2] = f_h_alpha(V) / (f_h_alpha(V) + f_h_beta(V))  # h
        state_[3] = f_n_alpha(V) / (f_n_alpha(V) + f_n_beta(V))  # n

    state = initial_neu_state(4, num)
    init_state(state, Vr)

    # update function
    # -------------------
    def update_state(neu_state, t):
        V, m, h, n, Isyn = neu_state[0], neu_state[1], neu_state[2], neu_state[3], neu_state[-1]
        m = clip(int_m(m, t, V), 0., 1.)
        h = clip(int_h(h, t, V), 0., 1.)
        n = clip(int_n(n, t, V), 0., 1.)
        INa = fo_INa(V, m, h)
        IK = fo_IK(V, n)
        IL = fo_ILeak(V)
        Icur = - INa - IK - IL
        V = int_V(V, t, Icur, Isyn)
        neu_state[0] = V
        neu_state[1] = m
        neu_state[2] = h
        neu_state[3] = n
        judge_spike(neu_state, Vth, t)

    return Neurons(**locals())
