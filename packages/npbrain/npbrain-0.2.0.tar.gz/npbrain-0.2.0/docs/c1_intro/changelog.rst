Release notes
=============


NumpyBrain 0.2.0
----------------

API changes
~~~~~~~~~~~

* Change `Synapses` API, making it more computationally efficient.
* Reformat connection methods.
* Change the fixed running order for "Neurons - Synapse - Monitors" to
  user defined orders in the function of `run()` in `Network`.
* remove "output_spike()" in "Neurons", add "collect_spike()" in "Synapses".
* add "variables" to Neurons and Synapse, change monitor corresponding API

Models and examples
~~~~~~~~~~~~~~~~~~~

* Add more `Neuron` examples, like Izhikevich model, HH model.
* Add AMPA synapses.
* Add GABAa and GABAb synapses.
* Add gap junction synapse.
* Add NMDA synapses.
* Add short-term plasticity synapses.

x Add more connection methods, such as `gaussian`.



NumpyBrain 0.1.0
----------------

This is the first release of NumpyBrain. Original NumpyBrain is a lightweight
SNN library only based on pure `NumPy <https://numpy.org/>`_. It is highly
highly highly flexible. However, for large-scale networks, this framework seems
slow. Recently, we changed the API to accommodate the
`Numba <http://numba.pydata.org/>`_ backend. Thus, when encountering large-scale
spiking neural network, the model can get the C or FORTRAN-like simulation speed.


