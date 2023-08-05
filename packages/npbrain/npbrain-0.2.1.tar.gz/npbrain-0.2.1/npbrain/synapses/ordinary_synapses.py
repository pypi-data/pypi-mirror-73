import numpy as np

from npbrain import profile
from npbrain.core.synapse import *
from npbrain.utils import helper
from npbrain.utils import conn

__all__ = [
    'VoltageJumpSynapse',
]


def VoltageJumpSynapse(pre, post, weights, connection, **kwargs):
    """Normal synapse.

    .. math::

        I_{syn} = \sum J \delta(t-t_j)

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
        The constructed ordinary synapses.
    """
    # base
    # ----
    name = kwargs.pop('name', 'VoltageJumpSynapse')
    var2index = dict()
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
    state = initial_syn_state(delay_len, num_pre, num_post, num)
    helper.check_params(kwargs)

    # functions
    # ---------
    def update_state(syn_state, var_index, t):
        # get synapse state
        spike = syn_state[0][-1]
        # calculate synaptic state
        spike_idx = np.where(spike > 0)[0]
        # get post-synaptic values
        g = np.zeros(num_post)
        for i_ in spike_idx:
            start, end = pre_anchors[:, i_]
            post_idx = post_indexes[start: end]
            g[post_idx] += weights
        record_conductance(syn_state, var_index, g)

    if hasattr(post, 'ref') and getattr(post, 'ref') > 0.:
        def output_synapse(syn_state, var_index, post_neu_state, ):
            output_idx = var_index[-2]
            g_val = syn_state[output_idx[0]][output_idx[1]]
            post_neu_state[0] += (g_val * post_neu_state[-5])
    else:
        def output_synapse(syn_state, var_index, post_neu_state, ):
            output_idx = var_index[-2]
            g_val = syn_state[output_idx[0]][output_idx[1]]
            post_neu_state[0] += g_val

    return Synapses(**locals())




