import numpy as np

from npbrain import profile
from npbrain.core.synapse import *
from npbrain.utils.helper import check_params
from npbrain.utils.helper import autojit
from npbrain.utils.helper import clip
from npbrain.utils import conn

__all__ = [
    'AMPA_Ch1',
    'AMPA_Ch2',
]


def AMPA_Ch1(pre, post, connection, **kwargs):
    """AMPA conductance-based synapse (type 1).

    .. math::

        I_{syn}&=\\bar{g}_{syn} s (V-E_{syn})

        \\frac{d s}{d t}&=-\\frac{s}{\\tau_{decay}}+\\sum_{k} \\delta(t-t_{j}^{k})

    Parameters
    ----------
    pre : Neurons
        The pre-synaptic neuron group.
    post : Neurons
        The post-synaptic neuron group.
    connection : dict, str, callable
        The connection method.
    kwargs : dict
        Synapse parameters.

    Returns
    -------
    synapse : Synapses
        The constructed AMPA synapses.
    """
    # base
    # ----
    num_pre = pre.num
    num_post = post.num
    dt = profile.get_dt()

    # essential
    # ---------
    name = kwargs.pop('name', 'AMPA_Ch1')
    var2index = {'s': (2, 0)}
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # ----------
    g_max = kwargs.pop('g_max', 0.10)  # nS
    E = kwargs.pop('E', 0.)  # mV
    tau_decay = kwargs.pop('tau_decay', 2)  # ms
    check_params(kwargs)

    # integration functions
    # ---------------------
    int_f = autojit(lambda s, t: s - s / tau_decay * dt)

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)
    state = initial_syn_state(
        delay_len, num_pre, num_post, num, num_syn_shape_var=1)

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # get synaptic state
        s = syn_state[2][0]
        spike = syn_state[0][0]
        # calculate synaptic state
        s = int_f(s, t)
        spike_idx = np.where(spike > 0.)[0]
        for i in spike_idx:
            start, end = pre_anchors[:, i]
            s[start: end] += 1
        syn_state[2][0] = s
        # get post-synaptic values
        g = np.zeros(num_post)
        for i in range(num_pre):
            start, end = pre_anchors[:, i]
            post_idx = post_indexes[start: end]
            g[post_idx] += s[start: end]
        record_conductance(syn_state, var_index, g)

    def output_synapse(syn_state, var_index, post_neu_state):
        output_idx = var_index[-2]
        g_val = syn_state[output_idx[0]][output_idx[1]]
        post_val = - g_max * g_val * (post_neu_state[0] - E)
        post_neu_state[-1] += post_val

    return Synapses(**locals())


def AMPA_Ch2(pre, post, connection, **kwargs):
    """AMPA conductance-based synapse (type 2).

    .. math::

        I_{syn}&=\\bar{g}_{syn} s (V-E_{syn})

        \\frac{ds}{dt} &=\\alpha[T](1-s)-\\beta s

    Parameters
    ----------
    pre : Neurons
        The pre-synaptic neuron group.
    post : Neurons
        The post-synaptic neuron group.
    connection : dict, str, callable
        The connection method.
    kwargs : dict
        Synapse parameters.

    Returns
    -------
    synapse : Synapses
        The constructed AMPA synapses.
    """
    # base
    # ----
    num_pre = pre.num
    num_post = post.num
    dt = profile.get_dt()

    # essential
    # ---------
    name = kwargs.pop('name', 'AMPA_Ch2')
    var2index = {'s': (2, 0), 'pre_spike_time': (2, 1)}
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # ----------
    E = kwargs.pop('E', 0)  # mV
    g_max = kwargs.pop('g_max', 0.42)  # nS
    alpha = kwargs.pop('alpha', 0.98)
    beta = kwargs.pop('beta', 0.18)
    T = kwargs.pop('T', 0.5)  # transmitter concentration, mM
    T_duration = kwargs.pop('T_duration', 0.5)  # ms
    check_params(kwargs)

    # integration functions
    # ---------------------
    int_s = autojit(lambda s, t, TT: s + (alpha * TT * (1 - s) - beta * s) * dt)

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)
    state = initial_syn_state(
        delay_len, num_pre, num_post, num, num_syn_shape_var=2)
    # The first (num_syn, ) variable is ``s``
    # The second (num_syn, ) variable if the last_spike time
    state[2][1] = -np.inf

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # get synaptic state
        spike = syn_state[0][0]
        s = syn_state[2][0]
        last_spike = syn_state[2][1]
        # calculate synaptic state
        spike_idx = np.where(spike > 0.)[0]
        for i in spike_idx:
            start, end = pre_anchors[:, i]
            last_spike[start: end] = t
        TT = ((t - last_spike) < T_duration).astype(np.float64) * T
        s = clip(int_s(s, t, TT), 0., 1.)
        syn_state[2][0] = s
        syn_state[2][1] = last_spike
        # get post-synaptic values
        g = np.zeros(num_post)
        for i in range(num_pre):
            start, end = pre_anchors[:, i]
            post_idx = post_indexes[start: end]
            g[post_idx] += s[start: end]
        record_conductance(syn_state, var_index, g)

    def output_synapse(syn_state, var_index, post_neu_state):
        output_idx = var_index[-2]
        g_val = syn_state[output_idx[0]][output_idx[1]]
        post_val = - g_max * g_val * (post_neu_state[0] - E)
        post_neu_state[-1] += post_val

    return Synapses(**locals())
