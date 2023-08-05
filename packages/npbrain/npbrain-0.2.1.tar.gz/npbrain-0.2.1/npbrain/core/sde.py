import numpy as np

from npbrain import profile

if profile.is_numba_bk():
    import numba as nb

__all__ = [
    'sde_generator',
    'Euler_method', 'EM', 'Euler', 'Euler_Maruyama_method', 'EM_method',
    'Milstein_dfree_Ito',
    'Heun_method2',
    'Heun', 'Euler_Heun', 'Euler_Heun_method', 'Heun_method',
    'Milstein_dfree_Stra',
]


def sde_generator(f, g, dt=None, method=None, **kwargs):
    """Generate the one-step SDE integration function.

    Parameters
    ----------
    f : callable
        The drift coefficient, the deterministic part of the SDE.
    g : callable, float
        The diffusion coefficient, the stochastic part.
    dt : None, float
        Precision of numerical integration.
    method : None, str, callable
        Method of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    if dt is None:
        dt = profile.get_dt()
    if method is None:
        method = profile.get_sde_method()

    if isinstance(method, str):
        if method in ['Euler_method', 'Euler_Maruyama_method', 'Euler', 'euler', 'EM']:
            return Euler_method(f, g, dt)
        if method in ['Milstein_dfree_Ito']:
            return Milstein_dfree_Ito(f, g, dt)

        if method in ['Euler_Heun_method', 'Heun_method', 'Euler_Heun', 'Heun']:
            return Heun(f, g, dt)
        if method in ['Heun_method_2']:
            return Heun_method2(f, g, dt)
        if method in ['Milstein_dfree_Stra']:
            return Milstein_dfree_Stra(f, g, dt)

    elif callable(method):
        return method(f, g, dt, **kwargs)
    else:
        raise ValueError('Unknown method type.')


# Euler_method-start
def Euler_method(f, g, dt=None):
    """Itô stochastic integral. The simplest stochastic numerical approximation
    is the Euler-Maruyama method. Its is an order 0.5 strong Taylor schema.
    Also named as ``EM``, ``EM_method``, ``Euler``, ``Euler_Maruyama_method``.

    Parameters
    ----------
    f : callable
        The drift coefficient, the deterministic part of the SDE.
    g : callable, float
        The diffusion coefficient, the stochastic part.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    dt = profile.get_dt() if dt is None else dt
    dt_sqrt = np.sqrt(dt)

    if callable(g):
        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df = f(y0, t, *args) * dt
            dg = dt_sqrt * g(y0, t, *args) * dW
            return y0 + df + dg
    else:
        assert isinstance(g, (int, float, np.ndarray))

        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df = f(y0, t, *args) * dt
            dg = dt_sqrt * g * dW
            return y0 + df + dg

    if profile.is_numba_bk():
        int_fg = nb.jit(**profile.get_numba_profile())(int_fg)

    return int_fg
# Euler_method-end


EM = EM_method = Euler = Euler_Maruyama_method = Euler_method


# Milstein_dfree_Ito-start
def Milstein_dfree_Ito(f, g, dt=None):
    """Itô stochastic integral. The derivative-free Milstein method is
    an order 1.0 strong Taylor schema.

    Parameters
    ----------
    f : callable
        The drift coefficient, the deterministic part of the SDE.
    g : callable, float
        The diffusion coefficient, the stochastic part.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    dt = profile.get_dt() if dt is None else dt
    dt_sqrt = np.sqrt(dt)

    if callable(g):
        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df = f(y0, t - dt, *args) * dt
            g_n = g(y0, t - dt, *args)
            dg = g_n * dW * dt_sqrt
            y_n_bar = y0 + df + g_n * dt_sqrt
            g_n_bar = g(y_n_bar, t, *args)
            y1 = y0 + df + dg + 0.5 * (g_n_bar - g_n) * (dW * dW * dt_sqrt - dt_sqrt)
            return y1

    else:
        assert isinstance(g, (int, float, np.ndarray))

        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df = f(y0, t - dt, *args) * dt
            dg = g * dW * dt_sqrt
            y_n_bar = y0 + df + g * dt_sqrt
            g_n_bar = g(y_n_bar, t, *args)
            y1 = y0 + df + dg + 0.5 * (g_n_bar - g) * (dW * dW * dt_sqrt - dt_sqrt)
            return y1

    if profile.is_numba_bk():
        int_fg = nb.jit(**profile.get_numba_profile())(int_fg)

    return int_fg
# Milstein_dfree_Ito-end


# Heun_method2-start
def Heun_method2(f, g, dt=None):
    """Stratonovich stochastic integral. Use the Stratonovich Heun algorithm
    to integrate Stratonovich equation,
    according to paper [1]_.

    Parameters
    ----------
    f : callable
        The drift coefficient, the deterministic part of the SDE.
    g : callable, float
        The diffusion coefficient, the stochastic part.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.

    References
    ----------
    .. [1] Burrage, Kevin, P. M. Burrage, and Tianhai Tian. "Numerical methods
           for strong solutions of stochastic differential equations: an overview."
           Proceedings of the Royal Society of London. Series A: Mathematical,
           Physical and Engineering Sciences 460.2041 (2004): 373-402.
    """
    dt = profile.get_dt() if dt is None else dt
    dt_sqrt = np.sqrt(dt)

    if callable(g):
        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df0 = f(y0, t - dt, *args) * dt
            dg0 = g(y0, t - dt, *args) * dW * dt_sqrt
            y_0 = y0 + df0 + dg0
            df1 = f(y_0, t, *args) * dt
            dg1 = g(y_0, t, *args) * dW * dt_sqrt
            y1 = y0 + 0.5 * (df0 + df1) + 0.5 * (dg0 + dg1)
            return y1

    else:
        assert isinstance(g, (int, float, np.ndarray))

        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df0 = f(y0, t - dt, *args) * dt
            dg = g * dW * dt_sqrt
            y_0 = y0 + df0 + dg
            df1 = f(y_0, t, *args) * dt
            y1 = y0 + 0.5 * (df0 + df1) + dg
            return y1

    if profile.is_numba_bk():
        int_fg = nb.jit(**profile.get_numba_profile())(int_fg)

    return int_fg
# Heun_method2-end


# Heun_method-start
def Heun_method(f, g, dt=None):
    """Stratonovich stochastic integral.Use the Stratonovich Heun algorithm
    to integrate Stratonovich equation,
    according to paper [2]_, [3]_.

    Parameters
    ----------
    f : callable
        The drift coefficient, the deterministic part of the SDE.
    g : callable, float
        The diffusion coefficient, the stochastic part.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.

    References
    ----------

    .. [2] H. Gilsing and T. Shardlow, SDELab: A package for solving stochastic differential
         equations in MATLAB, Journal of Computational and Applied Mathematics 205 (2007),
         no. 2, 1002{1018.
    .. [3] P.E. Kloeden, E. Platen, and H. Schurz, Numerical solution of SDE through computer
         experiments, Springer, 1994.
    """
    dt = profile.get_dt() if dt is None else dt
    dt_sqrt = np.sqrt(dt)

    if callable(g):
        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df = f(y0, t - dt, *args) * dt
            gn = g(y0, t - dt, *args)
            y_bar = y0 + gn * dW * dt_sqrt
            gn_bar = g(y_bar, t, *args)
            dg = 0.5 * (gn + gn_bar) * dW * dt_sqrt
            y1 = y0 + df + dg
            return y1
    else:
        assert isinstance(g, (int, float, np.ndarray))

        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df = f(y0, t - dt, *args) * dt
            dg = g * dW * dt_sqrt
            y1 = y0 + df + dg
            return y1

    if profile.is_numba_bk():
        int_fg = nb.jit(**profile.get_numba_profile())(int_fg)

    return int_fg
# Heun_method-end


Heun = Euler_Heun = Euler_Heun_method = Heun_method


# Milstein_dfree_Stra-start
def Milstein_dfree_Stra(f, g, dt=None):
    """Stratonovich stochastic integral. The derivative-free Milstein
    method is an order 1.0 strong Taylor schema.

    Parameters
    ----------
    f : callable
        The drift coefficient, the deterministic part of the SDE.
    g : callable, float
        The diffusion coefficient, the stochastic part.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    dt = profile.get_dt() if dt is None else dt
    dt_sqrt = np.sqrt(dt)

    if callable(g):
        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df = f(y0, t - dt, *args) * dt
            g_n = g(y0, t - dt, *args)
            dg = g_n * dW * dt_sqrt
            y_n_bar = y0 + df + g_n * dt_sqrt
            g_n_bar = g(y_n_bar, t, *args)
            extra_term = 0.5 * (g_n_bar - g_n) * (dW * dW * dt_sqrt)
            y1 = y0 + df + dg + extra_term
            return y1
    else:
        assert isinstance(g, (int, float, np.ndarray))

        def int_fg(y0, t, *args):
            dW = np.random.normal(0.0, 1.0, y0.shape)
            df = f(y0, t - dt, *args) * dt
            dg = g * dW * dt_sqrt
            y1 = y0 + df + dg
            return y1

    if profile.is_numba_bk():
        int_fg = nb.jit(**profile.get_numba_profile())(int_fg)

    return int_fg
# Milstein_dfree_Stra-end
