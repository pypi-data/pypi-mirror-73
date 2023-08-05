import numpy as np

from npbrain import profile
from npbrain.core.neuron import Neurons
from npbrain.core.synapse import Synapses
from npbrain.utils import helper

if profile.get_backend().startswith('numba'):
    from numba import typed, types
    from numba.core.dispatcher import Dispatcher

__all__ = [
    'Monitor',
    'SpikeMonitor',
    'StateMonitor',
    'raster_plot',
]


class Monitor(object):
    """Base monitor class.

    """
    def __init__(self, target):
        self.target = target

        if profile.is_numba_bk():
            if not isinstance(self.update_state, Dispatcher):
                self.update_state = helper.jit_function(self.update_state)

    def init_state(self, *args, **kwargs):
        raise NotImplementedError()



class SpikeMonitor(Monitor):
    """Monitor class to record spikes.

    target : Neurons
        The neuron group to monitor.
    """
    def __init__(self, target):
        # check `variables`
        self.vars = ('index', 'time')

        # check `target`
        assert isinstance(target, Neurons), 'Cannot monitor spikes in synapses.'

        # fake initialization
        self.index = []
        self.time = []
        self.state = self.time
        self.vars_idx = self.index

        # super class initialization
        super(SpikeMonitor, self).__init__(target)

    def init_state(self, length):
        self.index = []
        self.time = []
        if profile.is_numba_bk():
            self.index = typed.List.empty_list(types.int64)
            self.time = typed.List.empty_list(types.float64)
        self.state = self.time
        self.vars_idx = self.index

    @staticmethod
    def update_state(obj_state, mon_time, mon_index, t):
        spike_idx = np.where(obj_state[-3] > 0.)[0]
        for idx in spike_idx:
            mon_index.append(idx)
            mon_time.append(t)


class StateMonitor(Monitor):
    """Monitor class to record states.

    target : Neurons, Synapses
        The object to monitor.
    vars : str, list, tuple
        The variable need to be recorded for the ``target``.
    """
    def __init__(self, target, vars=None):
        # check `variables`
        if vars is None:
            if isinstance(target, Neurons):
                vars = ['V']
            elif isinstance(target, Synapses):
                vars = ['g']
            else:
                raise ValueError('When `vars=None`, NumpyBrain only supports the recording '
                                 'of "V" for Neurons and "g" for Synapses.')
        if isinstance(vars, str):
            vars = [vars]
        assert isinstance(vars, (list, tuple))
        vars = tuple(vars)
        for var in vars:
            if var not in target.vars:
                raise ValueError('Variable "{}" is not in target "{}".'.format(var, target))
        self.vars = vars
        self.vars_idx = np.array([target.vars[v] for v in vars])

        # fake initialization
        for k in self.vars:
            setattr(self, k, np.zeros((1, 1)))
        self.state = []

        # function of update state
        def record_neu_state(obj_state, mon_states, vars_idx, i):
            var_len = len(vars_idx)
            for j in range(var_len):
                index = vars_idx[j]
                v = obj_state[index]
                mon_states[j][i] = v

        def record_syn_state(obj_state, mon_states, vars_idx, i):
            var_len = len(vars_idx)
            for j in range(var_len):
                index = vars_idx[j]
                v = obj_state[index[0]][index[1]]
                mon_states[j][i] = v

        if isinstance(target, Neurons):
            self.update_state = record_neu_state
        elif isinstance(target, Synapses):
            self.update_state = record_syn_state
        else:
            raise ValueError('Unknown type.')

        # super class initialization
        super(StateMonitor, self).__init__(target)

    def target_index_by_vars(self):
        return self.target.var_index[self.vars_idx]

    def init_state(self, length):
        assert isinstance(length, int)

        vars_idx = self.target_index_by_vars()
        mon_states = []
        for i, k in enumerate(self.vars):
            index = vars_idx[i]
            if isinstance(self.target, Synapses):
                v = self.target.state
                for idx in index:
                    v = v[idx]
            else:
                v = self.target.state[index]
            shape = (length, ) + v.shape
            state = np.zeros(shape)
            setattr(self, k, state)
            mon_states.append(state)
        self.state = tuple(mon_states)


def raster_plot(mon):
    """Get spike raster plot which displays the spiking activity
    of a group of neurons over time.

    Parameters
    ----------
    mon : Monitor
        The monitor which record spiking activities.

    Returns
    -------
    raster_plot : tuple
        Include (neuron index, spike time).
    """
    if isinstance(mon, StateMonitor):
        elements = np.where(mon.spike > 0.)
        index = elements[1]
        time = mon.spike_time[elements]
    elif isinstance(mon, SpikeMonitor):
        index = np.array(mon.index)
        time = np.array(mon.time)
    else:
        raise ValueError
    return index, time
