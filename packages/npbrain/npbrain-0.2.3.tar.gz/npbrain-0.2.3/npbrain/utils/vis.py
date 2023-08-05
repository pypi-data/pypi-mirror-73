"""
Visualization toolkit.
"""

import matplotlib.pyplot as plt
from matplotlib import rcParams

from matplotlib.gridspec import GridSpec

from npbrain.core.monitor import raster_plot

__all__ = [
    'get_figure',

    'mpl_style1',

    'plot_value',
    'plot_potential',
    'plot_raster',

    'vector_field_2d_system',
]


def get_figure(n_row, n_col, len_row=3, len_col=6):
    fig = plt.figure(figsize=(n_col * len_col, n_row * len_row), constrained_layout=True)
    gs = GridSpec(n_row, n_col, figure=fig)
    return fig, gs

###############################
# plotting style
###############################


def mpl_style1(fontsize=22, axes_edgecolor='white', figsize='5,4', lw=1):
    rcParams['text.latex.preamble'] = [r"\usepackage{amsmath, lmodern}"]
    params = {
        'text.usetex': True,
        'font.family': 'lmodern',
        # 'text.latex.unicode': True,
        'text.color': 'black',
        'xtick.labelsize': fontsize - 2,
        'ytick.labelsize': fontsize - 2,
        'axes.labelsize': fontsize,
        'axes.labelweight': 'bold',
        'axes.edgecolor': axes_edgecolor,
        'axes.titlesize': fontsize,
        'axes.titleweight': 'bold',
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
        'axes.grid': False,
        'axes.facecolor': 'white',
        'lines.linewidth': lw,
        "figure.figsize": figsize,
    }
    rcParams.update(params)


###############################
# Neuron and Synapse plotting
###############################


def plot_value(ts, mon, key, val_index=None, ax=None):
    if val_index is None:
        val_index = [0]
    elif isinstance(val_index, int):
        val_index = [val_index]
    assert isinstance(val_index, (list, tuple))

    if ax is None:
        ax = plt
    for idx in val_index:
        ax.plot(ts, getattr(mon, key)[:, idx], label='{}-{}'.format(key, idx))
    if len(val_index) > 1:
        ax.legend()


def plot_potential(ts, mon, neuron_index=None, ax=None, label=True, show=False):
    if neuron_index is None:
        neuron_index = [0]
    elif isinstance(neuron_index, int):
        neuron_index = [neuron_index]
    assert isinstance(neuron_index, (list, tuple))

    if ax is None:
        ax = plt
    for idx in neuron_index:
        ax.plot(ts, mon.V[:, idx], label='N-{}'.format(idx))
    ax.legend()
    if label:
        plt.ylabel('Membrane potential')
        plt.xlabel('Time (ms)')
    if show:
        plt.show()


def plot_raster(mon, ax=None, markersize=2, color='k', label=True, show=False):
    index, time = raster_plot(mon)
    if ax is None:
        fig, gs = get_figure(1, 1)
        ax = fig.add_subplot(gs[0, 0])
    ax.plot(time, index, '.' + color, markersize=markersize)
    if label:
        plt.xlabel('Time (ms)')
        plt.ylabel('Neuron index')
    if show:
        plt.show()


def plot_synapse():
    pass


def plot_neuron():
    pass


############################
# Vector field plotting
############################


def vector_field_2d_system():
    pass

