import numpy as np

from npbrain import profile
from npbrain.core.synapse import *
from npbrain.utils import conn
from npbrain.utils.helper import autojit
from npbrain.utils.helper import check_params

__all__ = [
    'NMDA_Ch',
]


def NMDA_Ch(pre, post, connection, **kwargs):
    """NMDA conductance-based synapse.

    .. math::

        I_{syn}&=\\bar{g}_{syn} s (V-E_{syn})

        g_{NMDA}(t) &=\\bar{g}_{NMDA} \\cdot (V-E_{syn}) \\cdot g_{\\infty}
        \\cdot \\sum_j s_j^{NMDA}(t) \\quad (3)

        g_{\\infty}(V,[{Mg}^{2+}]_{o}) & =(1+{e}^{-\\alpha V}
        [{Mg}^{2+}]_{o}/\\beta)^{-1}  \\quad (4)

        \\frac{d s_{j}^{NMDA}(t)}{dt} & =-\\frac{s_{j}^{NMDA}(t)}
        {\\tau_{NMDA,decay}}+a x_{j}(t)(1-s_{j}^{NMDA}(t))  \\quad (5)

        \\frac{d x_{j}(t)}{dt} & =-\\frac{x_{j}(t)}{\\tau_{NMDA,rise}}+
        \\sum_{k} \\delta(t-t_{j}^{k})  \\quad (6)

    where the decay time of NMDA currents is taken to be :math:`\\tau_{NMDA,decay}` =100 ms,
    :math:`a= 0.5 ms^{-1}`, and :math:`\\tau_{NMDA,rise}` =2 ms (Hestrin et al., 1990;
    Spruston et al., 1995).

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
    name = kwargs.pop('name', 'NMDA_Ch')
    var2index = {'x': (2, 0), 's': (2, 1), 'post_V': (1, -1)}
    num_pre = pre.num
    num_post = post.num
    dt = kwargs.pop('dt', profile.get_dt())
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # ----------
    # for Eq. 3
    g_max = kwargs.pop('g_max', 1.5)  # nS
    E = kwargs.pop('E', 0)  # mV
    # for Eq. 4
    alpha = kwargs.pop('alpha', 0.062)  # mV^-1
    beta = kwargs.pop('beta', 3.75)  # mM^-1
    cc_Mg = kwargs.pop('cc_Mg', 1.2)  # mM
    # for Eq. 5
    tau_decay = kwargs.pop('tau_decay', 100)  # ms
    a = kwargs.pop('a', 0.5)  # ms^-1
    # for Eq. 6
    tau_rise = kwargs.pop('tau_rise', 2)  # ms
    # checking
    check_params(kwargs)

    # integration functions
    # ---------------------
    int_x = autojit(lambda x, t: x + (-x / tau_rise) * dt)
    int_s = autojit(lambda s, t, x: s + (-s / tau_decay + a * x * (1 - s)) * dt)
    f_g_inf = autojit(lambda V: 1 + cc_Mg / beta * np.exp(-alpha * V))

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)
    # The first (num_syn, ) variable is ``x``
    # The second (num_syn, ) variable is ``s``
    # The first last (num_post, ) variable is the post-synaptic potential
    state = initial_syn_state(delay_len, num_pre, num_post, num,
                              num_post_shape_var=1, num_syn_shape_var=2)

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # get synapse state
        spike = syn_state[0][0]
        post_v = syn_state[1][-1]
        x = syn_state[2][0]
        s = syn_state[2][1]
        # calculate synaptic state
        spike_idx = np.where(spike > 0.)[0]
        for i in spike_idx:
            start, end = pre_anchors[:, i]
            x[start: end] += 1
        x = int_x(x, t)
        s = int_s(s, t, x)
        syn_state[2][0] = x
        syn_state[2][1] = s
        # get post-synaptic values
        g = np.zeros(num_post)
        for i in range(num_pre):
            start, end = pre_anchors[:, i]
            post_idx = post_indexes[start: end]
            g[post_idx] += s[start: end]
        g = f_g_inf(post_v) * g
        record_conductance(syn_state, var_index, g)

    def output_synapse(syn_state, var_index, post_neu_state):
        output_idx = var_index[-2]
        g_val = syn_state[output_idx[0]][output_idx[1]]
        post_val = - g_max * g_val * (post_neu_state[0] - E)
        post_neu_state[-1] += post_val

    def collect_spike(syn_state, pre_neu_state, post_neu_state):
        # spike
        syn_state[0][-1] = pre_neu_state[-3]
        # membrane potential of post-synaptic neuron group
        syn_state[1][-1] = post_neu_state[0]

    return Synapses(**locals())