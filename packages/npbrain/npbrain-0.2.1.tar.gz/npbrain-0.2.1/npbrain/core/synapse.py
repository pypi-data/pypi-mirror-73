from math import ceil
from typing import Union

import numpy as np

from npbrain import profile
from npbrain.utils import helper

__all__ = [
    'record_conductance',
    'format_delay',
    'initial_syn_state',
    'Synapses',
]


synapse_no = 0


def record_conductance(syn_state, var_index, g):
    """Record the conductance of the synapses.

    Parameters
    ----------
    syn_state : tuple
        The state of the synapses.
    var_index : np.ndarray
        The indexes of variables.
    g : np.ndarray
        The conductance to record at current time.
    """
    # get `delay_len`
    delay_len = var_index[-1, 0]
    # update `output_idx`
    output_idx = (var_index[-2, 1] + 1) % delay_len
    var_index[-2, 1] = output_idx
    # update `delay_idx`
    delay_idx = (var_index[-3, 1] + 1) % delay_len
    var_index[-3, 1] = delay_idx
    # update `conductance`
    syn_state[1][delay_idx] = g


if profile.is_numba_bk():
    from numba.core.dispatcher import Dispatcher

    record_conductance = helper.jit_function(record_conductance)


def format_delay(delay, dt=None):
    """Format the given delay and get the delay length.

    Parameters
    ----------
    delay : None, int, float, np.ndarray
        The delay.
    dt : float, None
        The precision of the numerical integration.

    Returns
    -------
    delay_len : int
        Delay length.
    """
    if delay is None:
        delay_len = 1
    elif isinstance(delay, (int, float)):
        dt = profile.get_dt() if dt is None else dt
        delay_len = int(ceil(delay / dt)) + 1
    else:
        raise ValueError()
    return delay_len


def initial_syn_state(delay_len: int,
                      num_pre: int,
                      num_post: int,
                      num_syn: int,
                      num_pre_shape_var: int = 0,
                      num_post_shape_var: int = 0,
                      num_syn_shape_var: int = 0):
    """For each state, it is composed by
    (pre_shape_state, post_shape_state, syn_shape_state).

    Parameters
    ----------
    delay_len : int
        The length of synapse delay.
    num_pre : int
        Number of neurons in pre-synaptic group.
    num_post : int
        Number of neurons in post-synaptic group.
    num_syn : int
        Number of synapses.
    num_pre_shape_var : int
        Number of variables with (num_pre, ) shape.
    num_post_shape_var : int
        Number of variables with (num_post, ) shape.
    num_syn_shape_var : int
        Number of variables with (num_syn, ) shape.

    Returns
    -------
    state : tuple
        Synapse state.
    """

    # state with (pre_num, ) shape #
    ################################
    # The state is:
    #   pre_spike                 [[..........],
    # --------------------------   [..........],
    #   vars with num_pre shape    [..........],
    # --------------------------   [..........]]
    pre_shape_state = np.zeros((1 + num_pre_shape_var, num_pre))

    # state with (post_num, ) shape #
    #################################
    # The state is:
    # ----------- [[..........],
    # delays       [..........],
    # -----------  [..........],
    # other vars   [..........],
    # -----------  [..........]]
    post_shape_state = np.zeros((delay_len + num_post_shape_var, num_post))

    # state with (num_syn, ) shape #
    ################################
    # The state is:
    # -------------------------  [[..........],
    #  vars with num_syn shape    [..........]
    # -------------------------   [..........]]
    syn_shape_state = np.zeros((num_syn_shape_var, num_syn))

    state = (pre_shape_state, post_shape_state, syn_shape_state)
    return state


class Synapses(object):
    """The base synapses class.

    Parameters
    ----------
    kwargs : dict
        Parameters of the synapses.
    """
    def __init__(self, **kwargs):
        if 'kwargs' in kwargs:
            kwargs.pop('kwargs')
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.pre.post_groups.append(self.post)
        self.post.pre_groups.append(self.pre)
        self.post.pre_synapses.append(self)
        self.pre.post_synapses.append(self)

        # check functions
        assert 'update_state' in kwargs, 'Must provide "update_state" function.'

        if 'output_synapse' not in kwargs:
            def f1(syn_state, var_index, neu_state):
                output_idx = var_index[-2]
                neu_state[-1] += syn_state[output_idx[0]][output_idx[1]]
            self.output_synapse = f1

        if 'collect_spike' not in kwargs:
            def f2(syn_state, pre_neu_state, post_neu_state):
                syn_state[0][-1] = pre_neu_state[-3]
            self.collect_spike = f2

        if profile.is_numba_bk():
            if not isinstance(self.update_state, Dispatcher):
                self.update_state = helper.jit_function(self.update_state)
            if not isinstance(self.output_synapse, Dispatcher):
                self.output_synapse = helper.jit_function(self.output_synapse)
            if not isinstance(self.collect_spike, Dispatcher):
                self.collect_spike = helper.jit_function(self.collect_spike)

        # check `name`
        if 'name' not in kwargs:
            global synapse_no
            self.name = "Synapses-{}".format(synapse_no)
            synapse_no += 1

        # check `delay_len`
        if 'delay_len' not in kwargs:
            if 'delay' not in kwargs:
                raise ValueError('Must define "delay".')
            else:
                dt = kwargs.get('dt', profile.get_dt())
                self.delay_len = format_delay(self.delay, dt)

        # check `var2index`
        if 'var2index' not in kwargs:
            raise ValueError('Must define "var2index".')
        assert isinstance(self.var2index, dict), '"var2index" must be a dict.'
        # "g" is the "delay_idx"
        # 'g_post' is the "output_idx"
        default_variables = [('pre_spike', (0, -1)), ('g', (1, self.delay_len - 1)),
                             ('g_post', (1, 0)),]
        for k, _ in default_variables:
            if k in self.var2index:
                raise ValueError('"{}" is a pre-defined variable, '
                                 'cannot be defined in "var2index".'.format(k))
        user_defined_variables = sorted(list(self.var2index.items()), key=lambda a: a[1])
        syn_variables = user_defined_variables + default_variables
        var_index = np.zeros((len(syn_variables) + 1, 2), dtype=np.int32)
        var_index[-1, 0] = self.delay_len
        vars = dict(delay_len=-1)
        for i, (var, index) in enumerate(syn_variables):
            var_index[i] = list(index)
            vars[var] = i
        self.vars = vars
        self.var_index = var_index

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def available_monitors(self):
        return sorted(list(self.vars.keys()))

    def pre_shape_state(self):
        return self.state[0]

    def post_shape_state(self):
        return self.state[1]

    def syn_shape_state(self):
        return self.state[2]
