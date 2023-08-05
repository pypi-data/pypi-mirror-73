import time

import numpy as np

from npbrain import profile
from npbrain.core.monitor import SpikeMonitor, StateMonitor, Monitor
from npbrain.core.neuron import Neurons
from npbrain.core.synapse import Synapses
from npbrain.utils.helper import Dict

__all__ = [
    'Network'
]


class Network(object):
    """The main simulation controller in ``NumpyBrain``.

    ``Network`` handles the running of a simulation. It contains a set of
    objects that are added with `~Network.add`. The `~Network.run` method
    actually runs the simulation. The main loop runs according to user add
    orders. The objects in the `Network` are accessible via their names, e.g.
    `net.name` would return the `object` (including neurons, synapses, and
    monitors) with this name.

    """
    def __init__(self, *args, **kwargs):
        # store and neurons and synapses
        self.neurons = []
        self.synapses = []
        self.monitors = []

        # store all objects
        self._objsets = Dict()
        self.objects = []

        # record the current step
        self.current_time = 0.

        # add objects
        self.add(*args, **kwargs)

    def _add_obj(self, obj):
        if isinstance(obj, Neurons):
            self.neurons.append(obj)
        elif isinstance(obj, Synapses):
            self.synapses.append(obj)
        elif isinstance(obj, Monitor):
            self.monitors.append(obj)
        else:
            raise ValueError('Unknown object type: {}'.format(type(obj)))
        self.objects.append(obj)

    def add(self, *args, **kwargs):
        """Add object (neurons or synapses or monitor) to the network.

        Parameters
        ----------
        args : list, tuple
            The nameless objects to add in the network.
        kwargs : dict
            The named objects to add in the network.
        """
        for obj in args:
            self._add_obj(obj)
        for name, obj in kwargs.items():
            self._add_obj(obj)
            self._objsets.unique_add(name, obj)
            if name in ['neurons', 'synapses', 'state_monitors',
                        'spike_monitors', '_objsets', 'objects',
                        'current_t', 'add', 'run', 'run_time']:
                raise ValueError('Invalid name: ', name)
            setattr(self, name, obj)

    def _check_run_order(self):
        for obj in self.objects:
            if isinstance(obj, Synapses):
                syn_order = self.objects.index(obj)
                pre_neu_order = self.objects.index(obj.pre)
                post_neu_order = self.objects.index(obj.post)
                if syn_order > post_neu_order or syn_order > pre_neu_order:
                    raise ValueError('Synapse "{}" must run before than the '
                                     'pre-/post-synaptic neurons.'.format(obj))

    def _format_inputs_and_receiver(self, inputs, duration):
        dt = profile.get_dt()
        # format inputs and receivers
        if len(inputs) > 1 and not isinstance(inputs[0], (list, tuple)):
            if isinstance(inputs[0], Neurons):
                inputs = [inputs]
            else:
                raise ValueError('Unknown input structure.')
        # ---------------------
        # classify input types
        # ---------------------
        # 1. iterable inputs
        # 2. fixed inputs
        iterable_inputs = []
        fixed_inputs = []
        neuron_with_inputs = []
        for input_ in inputs:
            # get "receiver", "input", "duration"
            if len(input_) == 2:
                obj, Iext  = input_
                dur = (0, duration)
            elif len(input_) == 3:
                obj, Iext, dur = input_
            else:
                raise ValueError
            err = 'You can assign inputs only for added object. "{}" is not in the network.'
            if isinstance(obj, str):
                try:
                    obj = self._objsets[obj]
                except:
                    raise ValueError(err.format(obj))
            assert isinstance(obj, Neurons), "You can assign inputs only for Neurons."
            assert obj in self.objects, err.format(obj)
            assert len(dur) == 2, "Must provide the start and the end simulation time."
            assert 0 <= dur[0] < dur[1] <= duration
            dur = (int(dur[0] / dt), int(dur[1] / dt))
            neuron_with_inputs.append(obj)

            # judge the type of the inputs.
            if isinstance(Iext, (int, float)):
                Iext = np.ones(obj.num) * Iext
                fixed_inputs.append([obj, Iext, dur])
                continue
            size = np.shape(Iext)[0]
            run_length = dur[1] - dur[0]
            if size != run_length:
                if size == 1: Iext = np.ones(obj.num) * Iext
                elif size == obj.num: Iext = Iext
                else: raise ValueError('Wrong size of inputs for', obj)
                fixed_inputs.append([obj, Iext, dur])
            else:
                input_size = np.size(Iext[0])
                err = 'The input size "{}" do not match with neuron ' \
                      'group size "{}".'.format(input_size, obj.num)
                assert input_size == 1 or input_size == obj.num, err
                iterable_inputs.append([obj, Iext, dur])
        # 3. no inputs
        no_inputs = []
        for neu in self.neurons:
            if neu not in neuron_with_inputs:
                no_inputs.append(neu)
        return iterable_inputs, fixed_inputs, no_inputs

    def _step(self, t, run_idx):
        for obj in self.objects:
            if isinstance(obj, Synapses):
                obj.update_state(obj.state, obj.var_index, t)
                obj.output_synapse(obj.state, obj.var_index, obj.post.state, )
                obj.collect_spike(obj.state, obj.pre.state, obj.post.state)
            elif isinstance(obj, Neurons):
                obj.update_state(obj.state, t)
            elif isinstance(obj, StateMonitor):
                vars_idx = obj.target_index_by_vars()
                obj.update_state(obj.target.state, obj.state, vars_idx, run_idx)
            elif isinstance(obj, SpikeMonitor):
                obj.update_state(obj.target.state, obj.time, obj.index, t)
            else:
                raise ValueError

    def run(self, duration, report=False, inputs=()):
        """Runs the simulation for the given duration.

        Parameters
        ----------
        duration : int, float
            The amount of simulation time to run for.
        report : bool
            Report the progress of the simulation.
        inputs : list, tuple
            The receivers, external inputs and durations.
        """
        # checking
        # --------
        self._check_run_order()

        # initialization
        # -----------------

        # time
        dt = profile.get_dt()
        ts = np.arange(self.current_time, self.current_time + duration, dt)
        run_length = len(ts)

        # monitors
        for mon in self.monitors:
            mon.init_state(run_length)

        # format external inputs
        # -------------------------
        iterable_inputs, fixed_inputs, no_inputs = self._format_inputs_and_receiver(inputs, duration)

        # run
        # ---------
        if report:
            report_gap = int(run_length / 10)
            t0 = time.time()

        for run_idx in range(run_length):
            t = ts[run_idx]

            # inputs
            for receiver, inputs, dur in iterable_inputs:
                if dur[0] <= run_idx <= dur[1]:
                    obj_idx = run_idx - dur[0]
                    receiver.state[-1] = inputs[obj_idx]
                else:
                    receiver.state[-1] = 0.
            for receiver, inputs, dur in fixed_inputs:
                if dur[0] <= run_idx <= dur[1]:
                    receiver.state[-1] = inputs
                else:
                    receiver.state[-1] = 0.
            for receiver in no_inputs:
                receiver.state[-1] = 0.

                # run objects orderly
            self._step(t, run_idx)

            # report
            if report and ((run_idx + 1) % report_gap == 0):
                percent = (run_idx + 1) / run_length * 100
                print('Run {:.1f}% using {:.3f} s.'.format(percent, time.time() - t0))
        if report:
            print('Done. ')

        # Finally
        # -------
        self.current_time += duration

    def run_time(self):
        """Get the time points of the network.

        Returns
        -------
        times : numpy.ndarray
            The running time-steps of the network.
        """
        return np.arange(0, self.current_time, profile.get_dt())


