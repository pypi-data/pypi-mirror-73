import numpy as np

from npbrain import profile
from npbrain.core.synapse import *
from npbrain.utils.helper import check_params
from npbrain.utils import conn

__all__ = [
    'GapJunction',
    'GapJunction_LIF',
]


def GapJunction(pre, post, weights, connection, **kwargs):
    """Gap junction, or, electrical synapse.

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
    """
    # base
    # ----
    name = kwargs.pop('name', 'gap_junction')
    var2index = {'pre_V': (0, 0), 'post_V': (1, -1)}
    num_pre = pre.num
    num_post = post.num
    dt = kwargs.pop('dt', profile.get_dt())
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)
    # The first last (num_pre, ) shape variable is "pre-neuron spike"
    # The second last (num_pre, ) shape variable is "pre-neuron potential"
    # The first last (num_post, ) shape variable is "post-neuron potential"
    state = initial_syn_state(delay_len, num_pre, num_post, num,
                              num_pre_shape_var=1,
                              num_post_shape_var=1)
    check_params(kwargs)

    # weights
    # -------
    if isinstance(weights, (int, float)):
        weights = np.ones(num) * weights
    elif isinstance(weights, np.ndarray):
        if np.size(weights) == 1:
            weights = np.ones(num) * weights
        elif np.size(weights) == num:
            weights = weights
        else:
            raise ValueError('Unknown weights shape.')
    else:
        raise ValueError('Unknown weights type.')

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # get synapse state
        pre_v = syn_state[0][-2]
        post_v = syn_state[1][-1]
        # get gap junction value
        g = np.zeros(num_post)
        for i_ in range(num_pre):
            start, end = pre_anchors[:, i_]
            post_idx = post_indexes[start: end]
            g[post_idx] += weights[start: end] * (pre_v[i_] - post_v[post_idx])
        # record
        record_conductance(syn_state, var_index, g)

    def output_synapse(syn_state, var_index, post_neu_state):
        output_idx = var_index[-2]
        g_val = syn_state[output_idx[0]][output_idx[1]]
        # post-neuron inputs
        post_neu_state[-1] += g_val

    def collect_spike(syn_state, pre_neu_state, post_neu_state):
        # spike
        syn_state[0][-1] = pre_neu_state[-3]
        # membrane potential of pre-synaptic neuron group
        syn_state[0][-2] = pre_neu_state[0]
        # membrane potential of post-synaptic neuron group
        syn_state[1][-1] = post_neu_state[0]

    return Synapses(**locals())


def GapJunction_LIF(pre, post, weights, connection, **kwargs):
    """Gap junction, or, electrical synapse for LIF neuron model.

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
    """
    # base
    # ----
    name = kwargs.pop('name', 'gap_junction_for_LIF')
    var2index = {'pre_V': (0, 0), 'post_V': (1, -1)}
    num_pre = pre.num
    num_post = post.num
    dt = kwargs.pop('dt', profile.get_dt())
    delay = kwargs.pop('delay', None)
    delay_len = format_delay(delay, dt)

    # parameters
    # -----------
    k_spikelet = kwargs.pop('k_spikelet', 0.1)
    k = k_spikelet * weights
    check_params(kwargs)

    # connections
    # -----------
    pre_indexes, post_indexes, pre_anchors = conn.format_connection(
        connection, num_pre=num_pre, num_post=num_post)
    num = len(pre_indexes)
    # The first last (num_pre, ) shape variable is "pre-neuron spike"
    # The second last (num_pre, ) shape variable is "pre-neuron potential"
    # The first last (num_post * 2, ) shape variable is "post-neuron potential"
    # Other (num_post * 2, ) shape variables are corresponding for delays
    state = initial_syn_state(delay_len, num_pre, num_post * 2, num,
                              num_pre_shape_var=1,
                              num_post_shape_var=1)

    # weights
    # -------
    if isinstance(weights, (int, float)):
        weights = np.ones(num) * weights
    elif isinstance(weights, np.ndarray):
        if np.size(weights) == 1:
            weights = np.ones(num) * weights
        elif np.size(weights) == num:
            weights = weights
        else:
            raise ValueError('Unknown weights shape.')
    else:
        raise ValueError('Unknown weights type.')

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # get synapse state
        spike = syn_state[0][-1]
        pre_v = syn_state[0][-2]
        post_v = syn_state[1][-1]
        # calculate synapse state
        spike_idx = np.where(spike > 0.)[0]
        g = np.zeros(num_post * 2)
        # get spikelet
        g1 = np.zeros(num_post)
        for i_ in spike_idx:
            start, end = pre_anchors[:, i_]
            post_idx = post_indexes[start: end]
            g1[post_idx] += k
        g[num_post:] = g1
        # get gap junction value
        g2 = np.zeros(num_post)
        for i_ in range(num_pre):
            start, end = pre_anchors[:, i_]
            post_idx = post_indexes[start: end]
            g2[post_idx] += weights[start: end] * (pre_v[i_] - post_v[post_idx])
        g[:num_post] = g2
        # record
        record_conductance(syn_state, var_index, g)

    def output_synapse(syn_state, var_index, post_neu_state):
        output_idx = var_index[-2]
        syn_val = syn_state[output_idx[0]][output_idx[1]]
        # post-neuron inputs
        post_neu_state[-1] += syn_val[:num_post]
        # post-neuron potential
        post_neu_state[0] += syn_val[num_post:]

    def collect_spike(syn_state, pre_neu_state, post_neu_state):
        # spike
        syn_state[0][-1] = pre_neu_state[-3]
        # membrane potential of pre-synaptic neuron group
        syn_state[0][-2] = pre_neu_state[0]
        # membrane potential of post-synaptic neuron group
        syn_state[1][-1, :num_post] = post_neu_state[0]

    return Synapses(**locals())
