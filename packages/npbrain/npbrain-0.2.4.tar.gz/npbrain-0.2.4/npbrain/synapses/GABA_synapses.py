import numpy as np

from npbrain import profile
from npbrain.core.synapse import *
from npbrain.utils.helper import check_params
from npbrain.utils.helper import autojit
from npbrain.utils.helper import clip
from npbrain.utils import conn

__all__ = [
    'GABAa_Ch1',
    'GABAa_Ch2',
    'GABAb_Ch1',
    'GABAb_Ch2',
]


def GABAa_Ch1(pre, post, connection, **kwargs):
    """GABAa conductance-based synapse (type 1).

    .. math::

        I_{syn}&=\\bar{g}_{syn} s (V-E_{syn})

        \\frac{ds}{dt}&=-\\frac{s}{\\tau_{decay}}+\\sum_{k} \\delta(t-t_{j}^{k})

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
        The constructed GABAa synapses.
    """
    # base
    # ----
    num_pre = pre.num
    num_post = post.num
    dt = profile.get_dt()

    # essential
    # ---------
    name = kwargs.pop('name', 'GABAa_Ch1')
    var2index = {'s': (2, 0)}
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # ----------
    g_max = kwargs.pop('g_max', 0.04)  # nS
    E = kwargs.pop('E', -80)  # mV
    tau_decay = kwargs.pop('tau_decay', 6)  # ms
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
        s = int_f(s, t)
        spike = syn_state[0][0]
        # calculate synaptic state
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


def GABAa_Ch2(pre, post, connection, **kwargs):
    """GABAa conductance-based synapse (type 2).

    .. math::

        I_{syn} &=\\bar{g}_{syn} s (V-E_{syn})

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
        The constructed GABAa synapses.
    """
    # base
    # ----
    num_pre = pre.num
    num_post = post.num
    dt = profile.get_dt()

    # essential
    # ---------
    name = kwargs.pop('name', 'GABAa_Ch2')
    var2index = {'s': (2, 0), 'pre_spike_time': (2, 1)}
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # ----------
    g_max = kwargs.pop('g_max', 0.04)  # nS
    E = kwargs.pop('E', -80)  # mV
    alpha = kwargs.pop('alpha', 0.53)
    beta = kwargs.pop('beta', 0.18)
    T = kwargs.pop('T', 1.)  # transmitter concentration, mM
    T_duration = kwargs.pop('T_duration', 1.)  # ms
    check_params(kwargs)

    # integration functions
    # ---------------------
    int_s = autojit(lambda s, t, TT: s + (alpha * TT * (1 - s) - beta * s) * dt)

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)
    # The first (num_syn, ) variable is ``s``
    # The second (num_syn, ) variable if the last_spike time
    state = initial_syn_state(
        delay_len, num_pre, num_post, num, num_syn_shape_var=2)
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
        s = int_s(s, t, TT)
        s = clip(s, 0., 1.)
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


def GABAb_Ch1(pre, post, connection, **kwargs):
    """GABAb conductance-based synapse (type 1).

    .. math::

        &\\frac{d[R]}{dt} = k_3 [T](1-[R])- k_4 [R]

        &\\frac{d[G]}{dt} = k_1 [R]- k_2 [G]

        I_{GABA_{B}} &=\\overline{g}_{GABA_{B}} (\\frac{[G]^{4}} {[G]^{4}+100}) (V-E_{GABA_{B}})


    - [G] is the concentration of activated G protein.
    - [R] is the fraction of activated receptor.
    - [T] is the transmitter concentration.

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
        The constructed GABAb synapses.
    """
    # base
    # ----
    num_pre = pre.num
    num_post = post.num
    dt = profile.get_dt()

    # essential
    # ---------
    name = kwargs.pop('name', 'GABAb_Ch1')
    var2index = {'R': (2, 0), 'G': (2, 1), 'pre_spike_time': (2, 2)}
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # ----------
    g_max = kwargs.pop('g_max', 0.02)  # nS
    E = kwargs.pop('E', -85)  # mV
    k1 = kwargs.pop('k1', 0.18)
    k2 = kwargs.pop('k2', 0.034)
    k3 = kwargs.pop('k3', 0.09)
    k4 = kwargs.pop('k4', 0.0012)
    T = kwargs.pop('T', 0.5)  # transmitter concentration, mM
    T_duration = kwargs.pop('T_duration', 0.3)  # ms
    check_params(kwargs)

    # integration functions
    # ---------------------
    int_R = autojit(lambda R, t, TT: R + (k3 * TT * (1 - R) - k4 * R) * dt)
    int_G = autojit(lambda G, t, R: G + (k1 * R - k2 * G) * dt)
    f_g = autojit(lambda G: g_max * (G ** 4 / (G ** 4 + 100)))

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)
    # The first (num_syn, ) variable is ``R``
    # The second (num_syn, ) variable is ``G``
    # The third (num_syn, ) variable if the last_spike time
    state = initial_syn_state(
        delay_len, num_pre, num_post, num, num_syn_shape_var=3)
    state[2][2] = -np.inf

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # get synaptic state
        spike = syn_state[0][0]
        R = syn_state[2][0]
        G = syn_state[2][1]
        last_spike = syn_state[2][2]
        # calculate synaptic state
        spike_idx = np.where(spike > 0.)[0]
        for i in spike_idx:
            start, end = pre_anchors[:, i]
            last_spike[start: end] = t
        TT = ((t - last_spike) < T_duration).astype(np.float64) * T
        R = clip(int_R(R, t, TT), 0., 1.)
        G = int_G(G, t, R)
        syn_state[2][0] = R
        syn_state[2][1] = G
        syn_state[2][2] = last_spike
        # get post-synaptic values
        G = f_g(G)
        g = np.zeros(num_post)
        for i in range(num_pre):
            start, end = pre_anchors[:, i]
            post_idx = post_indexes[start: end]
            g[post_idx] += G[start: end]
        # g = f_g(g)
        record_conductance(syn_state, var_index, g)

    def output_synapse(syn_state, var_index, post_neu_state):
        output_idx = var_index[-2]
        g_val = syn_state[output_idx[0]][output_idx[1]]
        post_val = - g_val * (post_neu_state[0] - E)
        post_neu_state[-1] += post_val

    return Synapses(**locals())


def GABAb_Ch2(pre, post, connection, **kwargs):
    """GABAb conductance-based synapse (type 2).

    .. math::

        &\\frac{d[D]}{dt}=K_{4}[R]-K_{3}[D]

        &\\frac{d[R]}{dt}=K_{1}[T](1-[R]-[D])-K_{2}[R]+K_{3}[D]

        &\\frac{d[G]}{dt}=K_{5}[R]-K_{6}[G]

        I_{GABA_{B}}&=\\bar{g}_{GABA_{B}} \\frac{[G]^{n}}{[G]^{n}+K_{d}}(V-E_{GABA_{B}})

    where [R] and [D] are, respectively, the fraction of activated
    and desensitized receptor, [G] (in μM) the concentration of activated G-protein.

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
        The constructed GABAb synapses.
    """
    # base
    # ----
    num_pre = pre.num
    num_post = post.num
    dt = profile.get_dt()

    # essential
    # ---------
    name = kwargs.pop('name', 'GABAb_Ch2')
    var2index = {'D': (2, 0), 'R': (2, 1), 'G': (2, 2),
                 'pre_spike_time': (2, 2)}
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # ----------
    g_max = kwargs.pop('g_max', 0.2)  # nS
    E = kwargs.pop('E', -95)  # mV
    k1 = kwargs.pop('k1', 0.66)  # 6.6 x 10^5 M^-1 sec^-1
    k2 = kwargs.pop('k2', 0.02)  # 20 sec^-1
    k3 = kwargs.pop('k3', 0.0053)  # 5.3 sec^-1
    k4 = kwargs.pop('k4', 0.017)  # 17 sec^-1
    k5 = kwargs.pop('k5', 8.3e-5)  # 8.3 x 10^-5 M sec^-1
    k6 = kwargs.pop('k6', 7.9e-3)  # 7.9 sec^-1
    T = kwargs.pop('T', 0.5)  # transmitter concentration, mM
    T_duration = kwargs.pop('T_duration', 0.5)  # ms
    check_params(kwargs)

    # integration functions
    # ---------------------
    int_D = autojit(lambda D, t, R: D + (k4 * R - k3 * D) * dt)
    int_R = autojit(lambda R, t, TT, D: R + (k1 * TT * (1 - R - D) - k2 * R + k3 * D) * dt)
    int_G = autojit(lambda G, t, R: G + (k5 * R - k6 * G) * dt)
    f_g = autojit(lambda G: g_max * (G ** 4 / (G ** 4 + 100)))

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)
    # The first (num_syn, ) variable is ``D``
    # The second (num_syn, ) variable is ``R``
    # The third (num_syn, ) variable is ``G``
    # The fourth (num_syn, ) variable if the last_spike time
    state = initial_syn_state(delay_len, num_pre, num_post, num,
                              num_syn_shape_var=4)
    state[2][3] = -np.inf

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # calculate synaptic state
        spike = syn_state[0][0]
        D = syn_state[2][0]
        R = syn_state[2][1]
        G = syn_state[2][2]
        last_spike = syn_state[2][3]
        spike_idx = np.where(spike > 0.)[0]
        for i in spike_idx:
            start, end = pre_anchors[:, i]
            last_spike[start: end] = t
        TT = ((t - last_spike) < T_duration).astype(np.float64) * T
        D = int_D(D, t, R)
        R = int_R(R, t, TT, D)
        G = int_G(G, t, R)
        syn_state[2][0] = D
        syn_state[2][1] = R
        syn_state[2][2] = G
        syn_state[2][3] = last_spike
        # get post-synaptic values
        g = np.zeros(num_post)
        for i in range(num_pre):
            start, end = pre_anchors[:, i]
            post_idx = post_indexes[start: end]
            g[post_idx] += G[start: end]
        g = f_g(g)
        record_conductance(syn_state, var_index, g)

    def output_synapse(syn_state, var_index, post_neu_state):
        output_idx = var_index[-2]
        g_val = syn_state[output_idx[0]][output_idx[1]]
        post_val = - g_val * (post_neu_state[0] - E)
        post_neu_state[-1] += post_val

    return Synapses(**locals())
