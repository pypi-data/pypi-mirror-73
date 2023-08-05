import numpy as np

from npbrain import profile
from npbrain.core.synapse import *
from npbrain.utils import conn
from npbrain.utils.helper import clip
from npbrain.utils.helper import autojit
from npbrain.utils.helper import check_params

__all__ = [
    'STP',
]


def STP(pre, post, weights, connection, **kwargs):
    """Short-term plasticity proposed by Tsodyks and Markram (Tsodyks 98) [1]_.

    The model is given by

    .. math::

        \\frac{du}{dt} = -\\frac{u}{\\tau_f}+U(1-u^-)\\delta(t-t_{sp})

        \\frac{dx}{dt} = \\frac{1-x}{\\tau_d}-u^+x^-\\delta(t-t_{sp})

    where :math:`t_{sp}` denotes the spike time and :math:`U` is the increment
    of :math:`u` produced by a spike.

    The synaptic current generated at the synapse by the spike arriving
    at :math:`t_{sp}` is then given by

    .. math::

        \\Delta I(t_{sp}) = Au^+x^-

    where :math:`A` denotes the response amplitude that would be produced
    by total release of all the neurotransmitter (:math:`u=x=1`), called
    absolute synaptic efficacy of the connections.

    Parameters
    ----------
    pre : Neurons
        The pre-synaptic neuron group.
    post : Neurons
        The post-synaptic neuron group.
    weights : dict, np.ndarray, int, float
        The weighted coefficients of synapses.
    connection : dict, str, callable
        The connection method.
    kwargs : dict
        Synapse parameters.

    Returns
    -------
    synapse : Synapses
        The constructed electrical synapses.

    References
    ----------

    .. [1] Tsodyks, Misha, Klaus Pawelzik, and Henry Markram. "Neural networks
           with dynamic synapses." Neural computation 10.4 (1998): 821-835.
    """
    # base
    # ----
    num_pre = pre.num
    num_post = post.num
    dt = profile.get_dt()

    # essential
    # ---------
    name = kwargs.pop('name', 'short_term_plasticity')
    var2index = {'u': (2, 0), 'x': (2, 1)}
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # ----------
    U = kwargs.pop('U', 0.15)
    tau_f = kwargs.pop('tau_f', 1500)
    tau_d = kwargs.pop('tau_d', 200)
    init_u = kwargs.pop('init_u', 0.0)
    init_x = kwargs.pop('init_x', 1.0)
    check_params(kwargs)

    # integration functions
    # ---------------------
    int_u = autojit(lambda u, t: u - u / tau_f * dt)
    int_x = autojit(lambda x, t: x + (1 - x) / tau_d * dt)

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)

    # init state
    # ----------

    # The first (num_syn, ) shape variable is "u"
    # The second (num_syn, ) shape variable is "x"
    state = initial_syn_state(delay_len, num_pre, num_post, num, num_syn_shape_var=2)
    state[2][0] = np.ones(num) * init_u
    state[2][1] = np.ones(num) * init_x

    def init_state(syn_state, u, x):
        syn_state[2][0, :] = u
        syn_state[2][1, :] = x

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # get synapse state
        u_old = syn_state[2][0]
        x_old = syn_state[2][1]
        pre_spike = syn_state[0][0]
        # calculate synaptic state
        spike_idx = np.where(pre_spike > 0.)[0]
        u_new = int_u(u_old, t)
        x_new = int_x(x_old, t)
        for i in spike_idx:
            start, end = pre_anchors[:, i]
            u_new[start: end] += U * (1 - u_old[start: end])
            x_new[start: end] -= u_new[start: end] * x_old[start: end]
        u_new = clip(u_new, 0., 1.)
        x_new = clip(x_new, 0., 1.)
        syn_state[2][0] = u_new
        syn_state[2][1] = x_new
        # get post-synaptic values
        g = np.zeros(num_post)
        for i in range(num_pre):
            start, end = pre_anchors[:, i]
            post_idx = post_indexes[start: end]
            g[post_idx] += u_new[start: end] * x_new[start: end]
        record_conductance(syn_state, var_index, g)

    def output_synapse(syn_state, var_index, post_neu_state):
        output_idx = var_index[-2]
        syn_val = syn_state[output_idx[0]][output_idx[1]]
        post_neu_state[-1] += syn_val * weights

    return Synapses(**locals())

