.. npbrain documentation master file, created by
   sphinx-quickstart on Sat May 23 18:51:15 2020.
   You can adapt this file completely to your liking,
   but it should at least
   contain the root `toctree` directive.

NumpyBrain documentation
========================

``NumpyBrain`` is a micro-core framework for SNN (spiking neural network) simulation
purely based on **native** python. It only relies on `NumPy <https://numpy.org/>`_.
However, if you want to get faster CPU performance, or run codes on GPU, you can additionally
install `Numba <http://numba.pydata.org/>`_. With `Numba`, the speed of C or FORTRAN can
be gained in the simulation.



.. toctree::
   :maxdepth: 1
   :caption: Introduction

   c1_intro/installation
   c1_intro/motivations
   c1_intro/quick_start
   c1_intro/changelog

.. toctree::
   :maxdepth: 2
   :caption: User guides

   c2_guide/how_it_works
   c2_guide/neurons
   c2_guide/synapses
   c2_guide/ode
   c2_guide/sde

.. toctree::
   :maxdepth: 2
   :caption: API references

   c3_api/core
   c3_api/profile
   c3_api/neurons
   c3_api/synapses
   c3_api/utils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
