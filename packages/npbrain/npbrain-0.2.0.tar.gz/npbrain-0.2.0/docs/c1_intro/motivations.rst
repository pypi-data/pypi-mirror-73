Motivations
===========


A variety of Python SNN simulators are available in the internet, such as
`Brain2 <https://github.com/brian-team/brian2>`_,
`ANNarchy <https://github.com/ANNarchy/ANNarchy>`_,
`NEST <http://www.nest-initiative.org/>`_, etc.
However, several reasons motivate us
to write a NumPy-based simulator.

- First of all, using these simulators, a lot of garbage files are left after code compiling
  and running. In `Brain2`, such annoying rubbish can even accumulate to several GB.
- Second, the inner run-time mechanism is difficult to understand. The essence of these
  framework is that let you use python scripts to control the writing of c++/CUDA codes. Thus,
  if the users are not familiar with c++/CUDA codes and don't understand the inner mechanism
  of the framework, the data and logic flow control will be very complex and incomprehensible.
- Because of this, under these frameworks, on one hand, the codings of some models are weird,
  for example the `Gap Junction model` in `Brian2` (which dramatically different from other
  kinds of synapses); on the other hand, some models are wrongly coded and are hard to correct,
  such as the `Gap Junction model` for `LIF` (leaky integrate-and-fire) neurons
  in `Brian2` (see `some code.py <https://????>`_),
  `Hodgkin–Huxley neuron model` in `ANNarchy` (see
  :doc:`HH_model_in_ANNarchy.py <../c2_guide/files/HH_model_in_ANNarchy>`).

.. - Third, except ``Brian2``, other simulators are difficult to install.

Therefore, ``NumpyBrain`` wants to provide a highly flexible SNN simulation framework for
Python users. It endows the users with the fully data/logic flow control. Its design
overcomes the defects of other simulators, and are guided by the following principles:

- **Plug and play**. No garbage file will be left after any code-running.
  Just, use or not use.
- **Modularity**. A network can be broken down into various `neurons` and `synapses`.
  To inspect the inner dynamical structure of these elements, we need the `Monitor` to
  record the running trajectory for each object. In ``NumpyBrain``, there are only these
  three kinds of objects. Such objects can be plugged together almost arbitrarily (only
  with few restrictions) to form a new network.
- **Easy extensibility**. For each kind of object, new models (neurons or synapses) are
  simple to add, and existing models provide ample examples.
- **User friendliness**. The data flow in each object is transparent, and can be easily
  controlled by users. Users can define or modify the data or logical flow by themselves
  according to need.
