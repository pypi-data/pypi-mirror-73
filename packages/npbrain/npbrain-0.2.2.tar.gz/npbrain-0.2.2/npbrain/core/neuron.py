import numpy as np

from npbrain import profile
from npbrain.utils import helper

__all__ = [
    'judge_spike',
    'initial_neu_state',
    'format_geometry',
    'format_refractory',
    'Neurons',
    'generate_fake_neuron'
]


neuron_no = 0


def judge_spike(neu_state, Vth, t):
    """Judge and record the neuron spikes.

    Parameters
    ----------
    neu_state : np.ndarray
        The state of the neuron group.
    Vth : float, int, np.ndarray
        The spike threshold.
    t : float
        The current time point.

    Returns
    -------
    spike_indexes : list
        The neuron indexes that are spiking.
    """
    above_threshold = neu_state[0] >= Vth
    prev_above_th = neu_state[-4].astype(np.bool_)
    spike_st = np.logical_and(above_threshold, np.logical_not(prev_above_th))
    spike_idx = np.where(spike_st)[0]
    neu_state[-4] = above_threshold.astype(np.float64)
    neu_state[-3] = spike_st.astype(np.float64)
    neu_state[-2][spike_idx] = t
    return spike_idx


if profile.is_numba_bk():
    from numba.core.dispatcher import Dispatcher

    judge_spike = helper.jit_function(judge_spike)


def initial_neu_state(num_var, num_neuron):
    """Initialize the state of the given neuron group.

    For each state:

    -------------    [[..........],
    variables         [..........],
    -------------     [..........],
    not refractory    [..........],
    above threshold   [..........],
    spike_state       [..........],
    spike_time        [..........],
    inputs            [..........]]

    Parameters
    ----------
    num_var : int
        Number of the dynamical, static and other variables.
    num_neuron : int
        Number of the neurons in the group.

    Returns
    -------
    state : np.ndarray
        The state of the neuron group.
    """
    state = np.zeros((num_var + 5, num_neuron))
    state[-2] = -np.inf
    state[-5] = 1.
    return state


def format_geometry(geometry):
    """Format the geometry of the neuron group.

    Parameters
    ----------
    geometry : int, list, tuple
        The size (geometry) of the neuron group.

    Returns
    -------
    num_and_geo : tuple
        (Number of neurons, geometry of the neuron group).
    """
    # define network geometry
    if isinstance(geometry, (int, float)):
        geometry = (1, int(geometry), 1)
    elif isinstance(geometry, (tuple, list)):
        # a tuple is given, can be 1 .. N dimensional
        width = int(geometry[0])
        height = int(geometry[1]) if len(geometry) >= 2 else 1
        depth = int(geometry[2]) if len(geometry) >= 3 else 1
        geometry = (width, height, depth)
    else:
        raise ValueError()
    num = int(np.prod(geometry))
    return num, geometry


def format_refractory(ref=None):
    """Format the refractory period in the given neuron group.

    Parameters
    ----------
    ref : None, int, float
        The refractory period.

    Returns
    -------
    tau_ref : float
        The formatted refractory period.
    """
    if ref is None:
        tau_ref = 0
    elif isinstance(ref, (int, float)):
        if ref > 0:
            tau_ref = float(ref)
        elif ref == 0:
            tau_ref = 0
        else:
            raise ValueError
    elif isinstance(ref, np.ndarray):
        assert np.alltrue(ref >= 0)
        tau_ref = ref
    else:
        raise ValueError()
    return tau_ref


class Neurons(object):
    """The base neurons class.

    Parameters
    ----------
    kwargs : dict
        Parameters of the neuron group.
    """
    def __init__(self, **kwargs):
        if 'kwargs' in kwargs:
            kwargs.pop('kwargs')
        for k, v in kwargs.items():
            setattr(self, k, v)

        # define external connections
        self.pre_synapses = []
        self.post_synapses = []
        self.pre_groups = []
        self.post_groups = []

        # check functions
        assert 'update_state' in kwargs
        if profile.is_numba_bk():
            if not isinstance(self.update_state, Dispatcher):
                self.update_state = helper.jit_function(self.update_state)

        # check `dt`
        if 'dt' not in kwargs:
            self.dt = profile.get_dt()

        # check `name`
        if 'name' not in kwargs:
            global neuron_no
            self.name = "Neurons-{}".format(neuron_no)
            neuron_no += 1

        # check `var2index`
        if 'var2index' not in kwargs:
            raise ValueError('Must define "var2index".')
        assert isinstance(self.var2index, dict), '"var2index" must be a dict.'
        default_variables = [('V', 0), ('Isyn', -1), ('spike_time', -2), ('spike', -3),
                             ('above_threshold', -4), ('not_refractory', -5)]
        for k, _ in default_variables:
            if k in self.var2index:
                if k == 'V':
                    assert self.var2index['V'] == 0, 'The position of "V" must be 0.'
                else:
                    raise ValueError('"{}" is a pre-defined variable, cannot '
                                     'be defined in "var2index".'.format(k))
        user_defined_variables = sorted(list(self.var2index.items()), key=lambda a: a[1])
        neu_variables = user_defined_variables + default_variables
        var_index = np.zeros((len(neu_variables), ), dtype=np.int32)
        vars = dict()
        for i, (var, index) in enumerate(neu_variables):
            var_index[i] = index
            vars[var] = i
        self.vars = vars
        self.var_index = var_index

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def available_monitors(self):
        return sorted(list(self.variables.keys()))


def generate_fake_neuron(num, V=0.):
    """Generate the fake neuron group for testing synapse function.

    Parameters
    ----------
    num : int
        Number of neurons in the group.
    V : int, float, numpy.ndarray
        Initial membrane potential.

    Returns
    -------
    neurons : dict
        An instance of ``Dict`` for simulating neurons.
    """
    neu = helper.Dict(state=np.zeros((5, num)), num=num,
                      post_groups=[], pre_groups=[],
                      pre_synapses=[], post_synapses=[])
    neu.state[0] = V
    neu.update_state = helper.jit_lambda(lambda neu_state, t: 1)
    global neuron_no
    neu.name = 'FakeNeurons-{}'.format(neuron_no)
    neuron_no += 1
    return neu
