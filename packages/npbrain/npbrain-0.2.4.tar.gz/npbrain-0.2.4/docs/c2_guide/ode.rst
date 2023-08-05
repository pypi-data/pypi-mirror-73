Numerical Integration of Ordinary Differential Equations
========================================================

``NumpyBrain`` provides several explicit and implicit methods for
the numerical integration of Ordinary Differential Equations (ODEs).
Here, we will present the mathematical details of the implemented
methods.

Moreover, if users want to implement their own algorithms, please see
the third sections.

Explicit methods
----------------

Forward Euler method
********************

The simplest way for solving ordinary differential equations is "the
Euler method" by Press et al. (1992) [1]_ :

.. math::

    y_{n+1} = y_n + f(y_n, t_n) \Delta t

This formula advances a solution from :math:`y_n` to :math:`y_{n+1}=y_n+h`.
Note that the method increments a solution through an interval :math:`h`
while using derivative information from only the beginning of the interval.
As a result, the step's error is :math:`O(h^2)`.

.. literalinclude:: ../../npbrain/core/ode.py
    :start-after: euler-start
    :end-before: euler-end


RK2: Second-order Runge-Kutta method
************************************

``NumpyBrain`` also provides the second-order explicit RK method.
It is given in parametric form by [2]_

.. math::

    k_1	&=	f(y_n, t_n)  \\
    k_2	&=	f(y_n + \beta \Delta t k_1, t_n + \beta \Delta t) \\
    y_{n+1} &= y_n + \Delta t [(1-\frac{1}{2\beta})k_1+\frac{1}{2\beta}k_2]


Classical choices for :math:`\beta` are ``1/2`` (explicit midpoint method),
``2/3`` (Ralston’s method), and ``1`` (Heun’s method, also known
as the ``explicit trapezoid rule``).

.. literalinclude:: ../../npbrain/core/ode.py
    :start-after: rk2-start
    :end-before: rk2-end


RK3: Third-order Runge-Kutta method
***********************************

Runge-Kutta’s third-order method is given by [3]_ [4]_ [5]_

.. math::

    k_1 &= f(y_n, t_n) \\
    k_2 &= f(y_n + \frac{\Delta t}{2}k_1, tn+\frac{\Delta t}{2}) \\
    k_3 &= f(y_n -\Delta t k_1 + 2\Delta t k_2, t_n + \Delta t) \\
    y_{n+1} &= y_{n} + \frac{\Delta t}{6}(k_1 + 4k_2+k_3)

.. literalinclude:: ../../npbrain/core/ode.py
    :start-after: rk3-start
    :end-before: rk3-end


RK4: Fourth-order Runge-kutta method
************************************

The classical fourth-order Runge–Kutta (RK4) [3]_ [4]_ [5]_, which is
the most popular of the RK methods, is

.. math::

    k_1 &= f(y_n, t_n) \\
    k_2 &= f(y_n + \frac{\Delta t}{2}k_1, t_n + \frac{\Delta t}{2}) \\
    k_3 &= f(y_n + \frac{\Delta t}{2}k_2, t_n + \frac{\Delta t}{2}) \\
    k_4 &= f(y_n + \Delta t k_3, t_n + \Delta t) \\
    y_{n+1} &= y_n + \frac{\Delta t}{6}(k_1 + 2*k_2 + 2* k_3 + k_4)


.. literalinclude:: ../../npbrain/core/ode.py
    :start-after: rk4-start
    :end-before: rk4-end



RK4 alternative ("3/8" rule)
****************************

There is an alternative for RK4 method. It is a less often used fourth-order
explicit RK method, and was also proposed by Kutta [6]_:

.. math::

    k_1 &= f(y_n, t_n) \\
    k_2 &= f(y_n + \frac{\Delta t}{3}k_1, t_n + \frac{\Delta t}{3}) \\
    k_3 &= f(y_n - \frac{\Delta t}{3}k_1 + \Delta t k_2, t_n + \frac{2 \Delta t}{3}) \\
    k_4 &= f(y_n + \Delta t k_1 - \Delta t k_2 + \Delta t k_3, t_n + \Delta t) \\
    y_{n+1} &= y_n + \frac{\Delta t}{8}(k_1 + 3*k_2 + 3* k_3 + k_4)

.. literalinclude:: ../../npbrain/core/ode.py
    :start-after: rk4_alternative-start
    :end-before: rk4_alternative-end


Explicit Euler method
*********************

The explicit midpoint method [7]_ is given by the formula

.. math::

    k1 &= f(y_n, t_n) \\
    k2 &= f(y_n + \frac{\Delta t}{2}k1, t_n + \frac{\Delta t}{2}) \\
    y_{n+1} &= y_n + \Delta t k_2

Or, in one line

.. math::

    y_{n+1} = y_n + \Delta t f(y_n + \frac{\Delta t}{2}f(y_n, t_n),
    t_n + \frac{\Delta t}{2})

The explicit midpoint method is also known as the modified Euler method.

.. literalinclude:: ../../npbrain/core/ode.py
    :start-after: modified_Euler-start
    :end-before: modified_Euler-end


Implicit methods
----------------

Backward Euler method
*********************

The backward Euler method (or implicit Euler method) [8]_ [9]_
provide a different way for the
approximation of ordinary differential equations comparing with
the (standard) Euler method. The backward Euler method has error of
order ``1`` in time, it computes the approximations using

.. math::

    y_{n+1}=y_{n}+hf(t_{n+1},y_{n+1}).

This differs from the (forward) Euler method in that the latter
uses :math:`f(t_{n},y_{n})` in place of :math:`f(t_{n+1},y_{n+1})`.

**Solution**

The backward Euler method is an implicit method: the new approximation
:math:`y_{n+1}` appears on both sides of the equation, and thus the method
needs to solve an algebraic equation for the unknown :math:`y_{n+1}`.
For non-stiff problems, this can be done with fixed-point iteration:

.. math::

    y_{n+1}^{(0)} & =y_{n} \\
    y_{n+1}^{(i+1)} & =y_{n}+hf(t_{n+1},y_{n+1}^{(i)}).

If this sequence converges (within a given tolerance), then the method
takes its limit as the new approximation :math:`y_{n+1}`.

Alternatively, we can use the Newton–Raphson method to solve the
algebraic equation.

**Algorithmic summary of Backward Euler method**

For each timestep :math:`n`, do the following:

1, Initialize:

.. math::

    y_{n+1}^{(0)} &\leftarrow y_{n} \\
    i &\leftarrow 0

2, Update:

.. math::

    k &\leftarrow f(y_{n+1}^{(i)}, t_{n+1}) \\
    i &\leftarrow i + 1 \\
    y_{n+1}^{(i)} &= y_n + \Delta t k

3, If :math:`u^{(i)}_{n+1}` is “close” to :math:`u^{(i-1)}_{n+1}`,
the method has converged and the solution is complete. Jump to step 6.

4, If :math:`i = i_{max}`, the method did not converge. No solution
obtained; raise an exception.

5, Next iteration. Continue from step 2.

6, Set the solution obtained as

.. math::

    y_{n+1} \leftarrow y_{n+1}^{(i)}


.. literalinclude:: ../../npbrain/core/ode.py
    :start-after: backward_Euler-start
    :end-before: backward_Euler-end



Trapezoidal rule
****************

In numerical analysis and scientific computing,
the trapezoidal rule [10]_ is a numerical method to solve ordinary
differential equations derived from the trapezoidal rule for
computing integrals. The trapezoidal rule is an implicit
second-order method, which can be considered as both a
Runge–Kutta method and a linear multistep method.

The trapezoidal rule is given by the formula

.. math::

    y_{{n+1}}=y_{n}+{\tfrac 12}\Delta t
    {\Big (}f(t_{n},y_{n})+f(t_{{n+1}},y_{{n+1}}){\Big )}.

This is an implicit method: the value :math:`y_{n+1}` appears on both
sides of the equation, and to actually calculate it, we have to solve
an equation which will usually be nonlinear. One possible method for
solving this equation is Newton's method. We can use the Euler method
to get a fairly good estimate for the solution, which can be used as
the initial guess of Newton's method.


.. literalinclude:: ../../npbrain/core/ode.py
    :start-after: trapezoidal_rule-start
    :end-before: trapezoidal_rule-end


Implicit midpoint rule
**********************

The implicit midpoint method [11]_ is given by

.. math::

    y_{n+1} = y_n + \Delta t f(\frac{1}{2}(y_n + y_{n+1}),
    t_n + \frac{\Delta t}{2})

The implicit method is the most simple collocation method, and, applied to Hamiltonian dynamics, a symplectic integrator.


Customize ODE methods
---------------------

Here, you can customize your own ODE methods.


**References**

.. [1] W. H.; Flannery, B. P.; Teukolsky, S. A.; and Vetterling,
        W. T. Numerical Recipes in FORTRAN: The Art of Scientific
        Computing, 2nd ed. Cambridge, England: Cambridge University
        Press, p. 710, 1992.
.. [2] https://lpsa.swarthmore.edu/NumInt/NumIntSecond.html
.. [3] http://mathworld.wolfram.com/Runge-KuttaMethod.html
.. [4] https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
.. [5] https://zh.wikipedia.org/wiki/龙格－库塔法
.. [6] https://en.wikipedia.org/wiki/List_of_Runge%E2%80%93Kutta_methods
.. [7] https://en.wikipedia.org/wiki/Midpoint_method
.. [8] Forward and Backward Euler Methods,
       http://web.mit.edu/10.001/Web/Course_Notes/Differential_Equations_Notes/node3.html
.. [9] Butcher, John C. (2003), Numerical Methods for Ordinary
       Differential Equations, New York: John Wiley & Sons, ISBN 978-0-471-96758-3.
.. [10] Trapezoidal rule (differential equations),
        https://en.wikipedia.org/wiki/Trapezoidal_rule_(differential_equations)
.. [11] https://en.wikipedia.org/wiki/Midpoint_method
