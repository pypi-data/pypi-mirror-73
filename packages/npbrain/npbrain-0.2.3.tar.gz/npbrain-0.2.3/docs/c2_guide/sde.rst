Numerical Integration of Stochastic Differential Equations
==========================================================

``NumpyBrain`` provides commonly used integration methods for
stochastic differential equations (SDEs). Before we diving into
the mathematical basis of implemented algorithms, let's distinguish
the differences between two kinds of integrals of SDEs.

Itô and Stratonovich SDEs
-------------------------

**Itô stochastic integral**

One-dimensional stochastic differentiable equation (SDE) is given by [6]_ [7]_

.. math::

    \frac{dX_t}{dt} = f(X_t, t) dt + g(X_t, t)dW_t

where :math:`X_t = X(t)` is the realization of a stochastic processor
random variable. :math:`f(X_t,t)` is called the *drift* coefficient, that
is the deterministic part of the SDE characterizing the local trend.
:math:`g(X_t,t)` denotes the *diffusion* coefficient, that is the stochastic
part which influences the average size of the fluctuations of :math:`X`.
The fluctuations themselves originate from the stochastic process
:math:`W_t` called Wiener process.

Interpreseted as an integral, we get

.. math::

    X_t = X_{t0} + \int_{t0}^{t}f(X_s, s) ds +
    \int_{t0}^{t}g(X_s, s) dW_s

where the first integral is an ordinary Riemann integral. As the sample
paths of a Wiener process are not differentiable, the Japanese
mathematician K. Itô defined in 1940s a new type of integral called
**Itô stochastic integral**.

**Stratonovich stochastic integral**

In 1960s, the Russian physicist R. L. Stratonovich proposed an other
kind of stochastic integral called **Stratonovich stochastic integral**
and used the symbol “:math:`\circ`” to distinct it from the former
Itô integral [1]_ [6]_.

.. math::

    \frac{dX_t}{dt} = f(X_t, t)dt + g(X_t, t)\circ dW_t \label{strat:sde} \\
    X_t = X_{t_0} + \int_{t0}^{t}f(X_s, s)ds + \int_{t0}^{t}g(X_s, s) \circ dW_s

**A general form**

Both two ingetrals can be written in **a general form** as [8]_

.. math::

    \int_{t0}^{t} g(X_s, s) dW_s = lim_{h\to 0}
    \sum_{k=0}^{m-1}g(X_{\tau_k}, \tau_k) [W(t_{k+1}) - W({t_k})]

where :math:`h=(t_{k+1} - t_k)` with intermediary points
:math:`\tau_k = (1-\lambda)t_k - \lambda t_{k+1}, \forall k
\in \{0, 1, \cdots, m-1\}, \lambda \in [0, 1]`.

In the stochastic integral of the Itô SDE, :math:`\lambda = 0`
leads to :math:`\tau_k = t_k` and hence to evaluate the stochastic
integral at the left-point of the intervals [8]_, i.e.,

.. math::

    \int_{t0}^{t} g(X_s, s) dW_s = lim_{h\to 0} \sum_{k=0}^{m-1}
    g(X_{t_k}, t_k)[W(t_{k+1}) - W({t_k})]

In the deﬁnition of the Stratonovich integral, :math:`\lambda = 1/2` and
so :math:`\tau_k = (t_{k+1} - t_k)/2`, which fixes the evaluations of the
integral at the mid-point of each intervals, i.e.,

.. math::

    \int_{t0}^{t} g(X_s, s) dW_s = lim_{h\to 0} \sum_{k=0}^{m-1}
    g(X_{(t_{k+1} - t_k)/2}, (t_{k+1} - t_k)/2)[W(t_{k+1}) - W({t_k})]

**The difference between the Itô and Stratonovich calculi**

To illustrate the difference between the Itô and Stratonovich calculi,
lets have a closer look at the stochastic integral

.. math::

    \int_{t0}^T W(s) dW_s &= lim_{m \to \infty} W(\tau_k) [W(t_{k+1}) - W(t_k)] \\
                          &= \frac{W(t)}{2} - (\lambda -\frac{1}{2}) T

By combining the above equation with the respective value of :math:`\lambda`
discussed above for both interpretations, we obtain [8]_

.. math::

    \int_{t0}^T W(s) dW_s &= \frac{1}{2} W(t) - \frac{1}{2}T \\
    \int_{t0}^{T} W(s) \circ dW_s &= \frac{1}{2}W(t)

Ypu can see that the Itô and Stratonovich representations
do not converge towards the same solution.

**5 Switch between the Itô and Stratonovich calculi**

Conversions from Itô and Stratonovich calculus and inversely
are possible in order to switch between the two different calculi.
This is achieved by adding a correction term to the drift
coefficients [1]_.

.. math::

    dX_t &= f(X_t)dt + g(X_t)dW_t  \quad {\text{It\hat{o} SDE}}  \\
    dx_t &= \underline{f}(X_t)dt + g(X_t)\circ dW_t \quad (\text{Stratonovich SDE}) \\

where :math:`\underline{f} = f - \frac{1}{2} g'g` is called the
Itô and Stratonovich drift correction formula, and
:math:`g' = \frac{dg(X_t)}{dX_t}` is the first derivative of :math:`g`.

**Conclusion**

Both integrals have their advantages and disadvantages and which one should
be used is more a modelling than mathematical issue. In financial
mathematics, the Itô interpretation is usually used since Itô calculus
only takes into account information about the past. The Stratonovich
interpretation is the most frequently used within the physical sciences [6]_.
An excellent discussion of this subject can be found in [10]_.

Explicit order 0.5 strong Taylor scheme
---------------------------------------

It is difficult to deal with the SDEs analytically because of the highly
non-differentiable character of the realization of the Wiener process.
There are different, iterative methods that can be used to integrate SDE
systems. The most widely-used ones are introduced in the following sections.

- Explicit order 0.5 strong Taylor scheme
    * Euler-Maruyama
    * Euler-Heun
- Explicit order 1.0 strong Taylor scheme
    * Milstein method
    * Derivative-free Milstein (Runge-Kutta approach)


Euler-Maruyama method
*********************

The simplest stochastic numerical approximation is the Euler-Maruyama
method that requires the problem to be described using the Itô scheme.

This approximation is a continuous time stochastic process that
satisfy the iterative scheme [9]_.

.. math::

    Y_{n+1} = Y_n + f(Y_n)h_n + g(Y_n)\Delta W_n

where :math:`n=0,1, \cdots , N-1`, :math:`Y_0=x_0`, :math:`Y_n = Y(t_n)`,
:math:`h_n = t_{n+1} - t_n` is the step size,
:math:`\Delta W_n = [W(t_{n+1}) - W(t_n)] \sim N(0, h_n)=\sqrt{h}N(0, 1)`
with :math:`W(t_0) = 0`.

For simplicity, we rewrite the above equation into

.. math::

    Y_{n+1} = Y_n + f_n h + g_n \Delta W_n

As the order of convergence for the Euler-Maruyama method is low (strong order of
convergence 0.5, weak order of convergence 1), the numerical results are inaccurate
unless a small step size is used. By adding one more term from the stochastic
Taylor expansion, one obtains a 1.0 strong order of convergence scheme known
as *Milstein scheme* [9]_.

.. literalinclude:: ../../npbrain/core/sde.py
    :start-after: Euler_method-start
    :end-before: Euler_method-end


Euler-Heun method
*****************

If a problem is described using the Stratonovich scheme, then the Euler-Heun
method cab be used [3]_ [6]_.

.. math::
    Y_{n+1} &= Y_n + f_n h + {1 \over 2}[g_n + g(\overline{Y}_n)] \Delta W_n \\
    \overline{Y}_n &= Y_n + g_n \Delta W_n

.. literalinclude:: ../../npbrain/core/sde.py
    :start-after: Heun_method-start
    :end-before: Heun_method-end


Or, it is written as [11]_

.. math::

    Y_1 &= y_n + f(y_n)h + g_n \Delta W_n \\
    y_{n+1} &= y_n + {1 \over 2}[f(y_n) + f(Y_1)]h + {1 \over 2} [g(y_n) + g(Y_1)] \Delta W_n

.. literalinclude:: ../../npbrain/core/sde.py
    :start-after: Heun_method2-start
    :end-before: Heun_method2-end


Explicit order 1.0 strong Taylor scheme
---------------------------------------

Milstein method
***************

The Milstein scheme is slightly different whether it is the Itô or
Stratonovich representation that is used [3]_ [6]_ [7]_. It can be
proved that Milstein scheme converges strongly with order 1
(and weakly with order 1) to the solution of the SDE.

In Itô scheme, the Milstein method is described as

.. math::

    Y_{n+1} = Y_n + f_n h + g_n \Delta W_n + {1 \over 2}g_n g_n' [(\Delta W_n)^2 - h] \\

where :math:`g_n' = {dg(Y_n) \over dY_n}` is the first derivative of :math:`g_n`.

In Stratonovich schema, it is written as

.. math::

    Y_{n+1} = Y_n + f_n h + g_n \Delta W_n + {1 \over 2} g_n g_n' (\Delta W_n)^2

Note that when *additive noise* is used, i.e. when :math:`g_n` is constant and not
anymore a function of :math:`Y_n`, then both Itô and Stratonovich interpretations
are equivalent (:math:`g_n'= 0`).

Derivative-free Milstein method
*******************************

The drawback of the previous method is that it requires the analytic derivative
of :math:`g(Y_n)`$`, analytic expression that can become quickly highly complex.
The following implementation approximates this derivative thanks to a
Runge-Kutta approach [6]_.

In Itô scheme, it is expressed as

.. math::

    Y_{n+1} = Y_n + f_n h + g_n \Delta W_n + {1 \over 2\sqrt{h}}
    [g(\overline{Y_n}) - g_n] [(\Delta W_n)^2-h]

where :math:`\overline{Y_n} = Y_n + f_n h + g_n \sqrt{h}`.

.. literalinclude:: ../../npbrain/core/sde.py
    :start-after: Milstein_dfree_Ito-start
    :end-before: Milstein_dfree_Ito-end



In Stratonovich scheme, it is expressed as

.. math::

    Y_{n+1} = Y_n + f_n h + g_n\Delta W_n +  {1 \over 2\sqrt{h}}
    [g(\overline{Y_n}) - g_n] (\Delta W_n)^2

.. literalinclude:: ../../npbrain/core/sde.py
    :start-after: Milstein_dfree_Stra-start
    :end-before: Milstein_dfree_Stra-end


Customize SDE methods
---------------------

Here, you can customize your own SDE methods.


**References**

.. [1] K.E.S. Abe, W. Shaw, and M. Giles, Pricing Exotic Options using Local,
        Implied and Stochastic Volatility obtained from Market Data, (2004).
.. [2] P.M. Burrage, Runge-Kutta methods for stochastic differential
        equations, (1999).
.. [3] H. Gilsing and T. Shardlow, SDELab: A package for solving stochastic
        differential equations in MATLAB, Journal of Computational and Applied
        Mathematics 205 (2007), no. 2, 1002{1018.
.. [4] D.J. Higham, An algorithmic introduction to numerical simulation of
        stochastic differential equations, SIAM review (2001), 525-546.
.. [5] R.L. Honeycutt, Stochastic runge-kutta algorithms. I. White noise,
        Physical Review A 45 (1992), no. 2, 600{603.
.. [6] P.E. Kloeden, E. Platen, and H. Schurz, Numerical solution of SDE
        through computer experiments, Springer, 1994.
.. [7] H. Lamba, Stepsize control for the Milstein scheme using rst-exit-times.
.. [8] L. Panzar and E.C. Cipu, Using of stochastic Ito and Stratonovich
        integrals derived security pricing, (2005).
.. [9] U. Picchini, Sde toolbox: Simulation and estimation of stochastic
        differential equations with matlab.
.. [10] N. G. Van Kampen, Stochastic processes in physics and chemistry,
        North-Holland, 2007.
.. [11] Burrage, Kevin, P. M. Burrage, and Tianhai Tian. "Numerical methods
        for strong solutions of stochastic differential equations:
        an overview." Proceedings of the Royal Society of London. Series
        A: Mathematical, Physical and Engineering Sciences 460.2041 (2004):
        373-402.



