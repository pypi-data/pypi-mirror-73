import numpy as np
from npbrain.core.neuron import format_geometry
from npbrain.core.neuron import Neurons
from npbrain.core.neuron import initial_neu_state

from npbrain import profile

num_inputs = 0

__all__ = [
    'FreqInput',
    'TimeInput',
]


def FreqInput(geometry, freq, start_time=0., **kwargs):
    """The input neuron group characterized by frequency.

    For examples:

    >>> FreqInput(2, 10.)
    >>> # or
    >>> FreqInput(2, 10., 50.)

    Parameters
    ----------
    geometry : int, list, tuple
        The geometry of neuron group.
    freq : int, float
        The output spike frequency.
    start_time : float
        The time of the first spike.
    kwargs : dict
        Neuron parameters.

    Returns
    -------
    neurons : Neurons
        The created neuron group.
    """
    # base
    # ------
    global num_inputs
    name = kwargs.pop('name', 'inputs-{}'.format(num_inputs))
    num_inputs += 1
    var2index = dict()
    dt = kwargs.pop('dt', profile.get_dt())
    num, geometry = format_geometry(geometry)

    # state
    # ------
    state = initial_neu_state(1, num)
    state[0, 0] = start_time

    # functions
    # ----------
    def update_state(neu_state, t):
        if t >= neu_state[0, 0]:
            neu_state[-3] = 1.
            neu_state[-2] = t
            neu_state[0, 0] += 1000 / freq
        else:
            neu_state[-3] = 0.

    return Neurons(**locals())


def TimeInput(geometry, times, indices=None, **kwargs):
    """The input neuron group characterized by specific times.

    For examples:

    >>> TimeInput(2, [10, 20])
    >>> # or
    >>> TimeInput(2, [10, 20], 0)
    >>> # or
    >>> TimeInput(2, [10, 20, 30], [0, 1, 0])
    >>> # or
    >>> TimeInput(2, [10, 20, 30], [0, [0, 1], 1])

    Parameters
    ----------
    geometry : int, list, tuple
        The geometry of neuron group.
    times : list
        The time points which generate the spikes.
    indices : None, int, list, tuple
        The neuron indices at each time point.
    kwargs : dict
        Neuron parameters.

    Returns
    -------
    neurons : Neurons
        The created neuron group.
    """
    # base
    # ------
    global num_inputs
    name = kwargs.pop('name', 'inputs-{}'.format(num_inputs))
    num_inputs += 1
    var2index = dict()
    dt = kwargs.pop('dt', profile.get_dt())
    num, geometry = format_geometry(geometry)

    # parameters
    # -----------
    # times
    assert (isinstance(times, (list, tuple)) and
            isinstance(times[0], (int, float))) or \
           (isinstance(times, np.ndarray) and
            np.ndim(times) == 1)
    times = np.array(times)
    num_times = len(times)
    # indices
    if indices is None:
        indices = np.ones((len(times), num), dtype=np.bool_)
    elif isinstance(indices, int):
        idx = indices
        indices = np.zeros((len(times), num), dtype=np.bool_)
        indices[:, idx] = True
    elif isinstance(indices, (tuple, list)):
        old_idx = indices
        indices = np.zeros((len(times), num), dtype=np.bool_)
        for i, it in enumerate(old_idx):
            if isinstance(it, int):
                indices[i, it] = True
            elif isinstance(it, (tuple, list)):
                indices[i][it] = True
            else:
                raise ValueError('Unknown type.')
    else:
        raise ValueError('Unknown type.')

    # state
    # ------
    state = initial_neu_state(1, num)
    state[0, 0] = 0.  # current index

    # functions
    # ----------
    def update_state(neu_state, t):
        current_idx = int(neu_state[0, 0])
        if (current_idx < num_times) and (t >= times[current_idx]):
            idx = np.where(indices[current_idx])[0]
            neu_state[-3][idx] = 1.
            neu_state[-2][idx] = t
            neu_state[0, 0] += 1
        else:
            neu_state[-3] = 0.

    return Neurons(**locals())
