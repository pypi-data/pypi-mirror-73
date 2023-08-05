"""
Connection toolkit.
"""

import numpy as np

__all__ = [
    'format_connection', 'from_conn_mat',

    'one2one', 'all2all',
    'grid_four', 'grid_eight', 'grid_N',
    'fixed_prob', 'fixed_prenum', 'fixed_postnum',

    'gaussian',
    'dog',
    'scale_free', 'small_world',
]

# -----------------------------------
# helper methods for connection
# -----------------------------------


def format_connection(connection, num_pre, num_post):
    if isinstance(connection, str):
        conn_name = connection
        i, j, a = _conn_by_name(conn_name, num_pre, num_post)
    elif isinstance(connection, dict):
        if 'method' in connection:
            conn_name = connection.pop('method')
            conn_pars = connection
            if callable(conn_name):
                i, j, a = conn_name(**conn_pars)
            else:
                i, j, a = _conn_by_name(conn_name, num_pre, num_post, **conn_pars)
        else:
            i, j = connection.pop('i'), connection.pop('j')
            if 'a' not in connection:
                i, j, a = from_ij(i, j, num_pre)
            else:
                a = connection.pop('a')
    elif callable(connection):
        i, j, a = connection(num_pre, num_post)
    else:
        raise ValueError()
    pre_indexes, post_indexes, pre_anchors = i, j, a
    return pre_indexes, post_indexes, pre_anchors


def _conn_by_name(name, num_pre, num_post, *args, **kwargs):
    if name in ['one_to_one', 'one2one']:
        i, j, a = one2one(num_pre, num_post)
    elif name in ['all_to_all', 'all2all']:
        i, j, a = all2all(num_pre, num_post, *args, **kwargs)

    elif name in ['grid_four', 'grid4']:
        i, j, a = grid_four(*args, **kwargs)
    elif name in ['grid_eight', 'grid8']:
        i, j, a = grid_eight(*args, **kwargs)
    elif name in ['grid_N', ]:
        i, j, a = grid_N(*args, **kwargs)

    elif name in ['fixed_prob', ]:
        i, j, a = fixed_prob(num_pre, num_post, *args, **kwargs)
    elif name in ['fixed_prenum']:
        i, j, a = fixed_prenum(num_pre, num_post, *args, **kwargs)
    elif name in ['fixed_postnum']:
        i, j, a = fixed_postnum(num_pre, num_post, *args, **kwargs)

    else:
        raise ValueError()
    return i, j, a


def from_conn_mat(conn_mat):
    """Get the connections from connectivity matrix.

    This function which create three arrays. The first one is the connected
    pre-synaptic neurons, a 1-D array. The second one is the connected
    post-synaptic neurons, another 1-D array. The third one is the start
    and the end indexes at the 1-D array for each pre-synaptic neurons.

    Parameters
    ----------
    conn_mat : numpy.ndarray
        Connectivity matrix with `(num_pre x num_post)` shape.

    Returns
    -------
    conn_tuple : tuple
        (Pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic
         neuron for each pre-synaptic neuron).
    """
    pre_indexes = []
    post_indexes = []
    pre_anchors = []
    ii = 0
    num_pre = conn_mat.shape[0]
    for pre_idx in range(num_pre):
        post_idxs = np.where(conn_mat[pre_idx] > 0)[0]
        post_indexes.extend(post_idxs)
        len_idx = len(post_idxs)
        pre_anchors.append([ii, ii + len_idx])
        pre_indexes.extend([pre_idx] * len(post_idxs))
        ii += len_idx
    post_indexes = np.array(post_indexes)
    pre_anchors = np.array(pre_anchors).T
    return pre_indexes, post_indexes, pre_anchors


def from_ij(i, j, num_pre=None):
    """Format complete connections from `i` and `j` indexes.

    Parameters
    ----------
    i : list, numpy.ndarray
        The pre-synaptic neuron indexes.
    j : list, numpy.ndarray
        The post-synaptic neuron indexes.
    num_pre : int, None
        The number of the pre-synaptic neurons.

    Returns
    -------
    conn_tuple : tuple
        (pre_indexes, post_indexes, pre_anchors).
    """
    conn_i = np.array(i)
    conn_j = np.array(j)
    num_pre = np.max(i) + 1 if num_pre is None else num_pre
    pre_indexes, post_indexes, pre_anchors = [], [], []
    ii = 0
    for i in range(num_pre):
        indexes = np.where(conn_i == i)[0]
        post_idx = conn_j[indexes]
        post_len = len(post_idx)
        pre_indexes.extend([i] * post_len)
        post_indexes.extend(post_idx)
        pre_anchors.append([ii, ii + post_len])
        ii += post_len
    pre_indexes = np.asarray(pre_indexes)
    post_indexes = np.asarray(post_indexes)
    pre_anchors = np.asarray(pre_anchors).T
    return pre_indexes, post_indexes, pre_anchors


# -----------------------------------
# methods of connection
# -----------------------------------

def one2one(num_pre, num_post, **kwargs):
    """Connect two neuron groups one by one. This means
    The two neuron groups should have the same size.

    Parameters
    ----------
    num_pre : int
        Number of neurons in the pre-synaptic group.
    num_post : int
        Number of neurons in the post-synaptic group.
    kwargs : dict
        Other Parameters.

    Returns
    -------
    connection : tuple
        (pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic neuron
         for each pre-synaptic neuron)
    """
    assert num_pre == num_post
    pre_indexes = list(range(num_pre))
    post_indexes = list(range(num_post))
    pre_anchors = [[ii, ii + 1] for ii in range(num_post)]
    pre_indexes = np.asarray(pre_indexes)
    post_indexes = np.asarray(post_indexes)
    pre_anchors = np.asarray(pre_anchors).T
    return pre_indexes, post_indexes, pre_anchors


def all2all(num_pre, num_post, include_self=True, **kwargs):
    """Connect each neuron in first group to all neurons in the
    post-synaptic neuron groups. It means this kind of connection
    will create (num_pre x num_post) synapses.

    Parameters
    ----------
    num_pre : int
        Number of neurons in the pre-synaptic group.
    num_post : int
        Number of neurons in the post-synaptic group.
    include_self : bool
        Whether create (i, i) connection ?
    kwargs : dict
        Other Parameters.

    Returns
    -------
    connection : tuple
        (pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic neuron
         for each pre-synaptic neuron)
    """
    pre_indexes, post_indexes, pre_anchors = [], [], []
    ii = 0
    for i_ in range(num_pre):
        jj = 0
        for j_ in range(num_post):
            if (not include_self) and (i_ == j_):
                continue
            else:
                pre_indexes.append(i_)
                post_indexes.append(j_)
                jj += 1
        pre_anchors.append([ii, ii + jj])
        ii += jj
    pre_indexes = np.asarray(pre_indexes)
    post_indexes = np.asarray(post_indexes)
    pre_anchors = np.asarray(pre_anchors).T
    return pre_indexes, post_indexes, pre_anchors


def grid_four(height, width, include_self=False):
    """The nearest four neighbors connection method.

    Parameters
    ----------
    height : int
        Number of rows.
    width : int
        Number of columns.
    include_self : bool
        Whether create (i, i) connection ?

    Returns
    -------
    connection : tuple
        (pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic neuron
         for each pre-synaptic neuron)
    """
    conn_i = []
    conn_j = []
    for row in range(height):
        for col in range(width):
            i_index = (row * width) + col
            if 0 <= row - 1 < height:
                j_index = ((row - 1) * width) + col
                conn_i.append(i_index)
                conn_j.append(j_index)
            if 0 <= row + 1 < height:
                j_index = ((row + 1) * width) + col
                conn_i.append(i_index)
                conn_j.append(j_index)
            if 0 <= col - 1 < width:
                j_index = (row * width) + col - 1
                conn_i.append(i_index)
                conn_j.append(j_index)
            if 0 <= col + 1 < width:
                j_index = (row * width) + col + 1
                conn_i.append(i_index)
                conn_j.append(j_index)
            if include_self:
                conn_i.append(i_index)
                conn_j.append(i_index)
    conn_i = np.asarray(conn_i)
    conn_j = np.asarray(conn_j)

    pre_indexes = []
    post_indexes = []
    pre_anchors = []
    num_pre = height * width
    ii = 0
    for i in range(num_pre):
        indexes = np.where(conn_i == i)[0]
        post_idx = conn_j[indexes]
        post_len = len(post_idx)
        pre_indexes.extend([i] * post_len)
        post_indexes.extend(post_idx)
        pre_anchors.append([ii, ii + post_len])
        ii += post_len
    pre_indexes = np.asarray(pre_indexes)
    post_indexes = np.asarray(post_indexes)
    pre_anchors = np.asarray(pre_anchors).T
    return pre_indexes, post_indexes, pre_anchors


def grid_eight(height, width, include_self=False):
    """The nearest eight neighbors connection method.

    Parameters
    ----------
    height : int
        Number of rows.
    width : int
        Number of columns.
    include_self : bool
        Whether create (i, i) connection ?

    Returns
    -------
    connection : tuple
        (pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic neuron
         for each pre-synaptic neuron)
    """
    return grid_N(height, width, 1, include_self)


def grid_N(height, width, N=1, include_self=False):
    """The nearest (2*N+1) * (2*N+1) neighbors connection method.

    Parameters
    ----------
    height : int
        Number of rows.
    width : int
        Number of columns.
    N : int
        Extend of the connection scope. For example:
        When N=1,
            [x x x]
            [x I x]
            [x x x]
        When N=2,
            [x x x x x]
            [x x x x x]
            [x x I x x]
            [x x x x x]
            [x x x x x]
    include_self : bool
        Whether create (i, i) connection ?

    Returns
    -------
    connection : tuple
        (pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic neuron
         for each pre-synaptic neuron)
    """
    conn_i = []
    conn_j = []
    for row in range(height):
        for col in range(width):
            i_index = (row * width) + col
            for row_diff in [-N, 0, N]:
                for col_diff in [-N, 0, N]:
                    if (not include_self) and (row_diff == col_diff == 0):
                        continue
                    if 0 <= row + row_diff < height and 0 <= col + col_diff < width:
                        j_index = ((row + row_diff) * width) + col + col_diff
                        conn_i.append(i_index)
                        conn_j.append(j_index)
    conn_i = np.asarray(conn_i)
    conn_j = np.asarray(conn_j)

    pre_indexes = []
    post_indexes = []
    pre_anchors = []
    num_pre = height * width
    ii = 0
    for i in range(num_pre):
        indexes = np.where(conn_i == i)[0]
        post_idx = conn_j[indexes]
        post_len = len(post_idx)
        pre_indexes.extend([i] * post_len)
        post_indexes.extend(post_idx)
        pre_anchors.append([ii, ii + post_len])
        ii += post_len
    pre_indexes = np.asarray(pre_indexes)
    post_indexes = np.asarray(post_indexes)
    pre_anchors = np.asarray(pre_anchors).T
    return pre_indexes, post_indexes, pre_anchors


def fixed_prob(pre, post, prob, include_self=True, **kwargs):
    """Connect the post-synaptic neurons with fixed probability.

    Parameters
    ----------
    pre : int, list
        Number of neurons in the pre-synaptic group.
    post : int, list
        Number of neurons in the post-synaptic group.
    prob : float
        The connection probability.
    include_self : bool
        Whether create (i, i) connection ?
    kwargs : dict
        Other Parameters.

    Returns
    -------
    connection : tuple
        (pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic neuron
         for each pre-synaptic neuron)
    """
    if isinstance(pre, int):
        num_pre = pre
        all_pre = list(range(pre))
    elif isinstance(pre, (list, tuple)):
        all_pre = list(pre)
        num_pre = len(all_pre)
    else:
        raise ValueError
    if isinstance(post, int):
        num_post = post
        all_post = list(range(post))
    elif isinstance(post, (list, tuple)):
        all_post = list(post)
        num_post = len(all_post)
    else:
        raise ValueError
    assert isinstance(prob, (int, float)) and 0. <= prob <= 1.
    pre_indexes = []
    post_indexes = []
    pre_anchors = np.zeros((2, np.max(all_pre) + 1), dtype=np.int32)
    ii = 0
    for pre_idx in all_pre:
        random_vals = np.random.random(num_post)
        idx_selected = list(np.where(random_vals < prob)[0])
        if (not include_self) and (pre_idx in idx_selected):
            idx_selected.remove(pre_idx)
        for post_idx in idx_selected:
            pre_indexes.append(pre_idx)
            post_indexes.append(all_post[post_idx])
        size_post = len(idx_selected)
        pre_anchors[:, pre_idx] = [ii, ii + size_post]
        ii += size_post
    pre_indexes = np.asarray(pre_indexes)
    post_indexes = np.asarray(post_indexes)
    pre_anchors = np.asarray(pre_anchors)
    return pre_indexes, post_indexes, pre_anchors


def fixed_prenum(num_pre, num_post, num, include_self=True, **kwargs):
    """Connect the pre-synaptic neurons with fixed number for each
    post-synaptic neuron.

    Parameters
    ----------
    num_pre : int
        Number of neurons in the pre-synaptic group.
    num_post : int
        Number of neurons in the post-synaptic group.
    num : int
        The fixed connection number.
    include_self : bool
        Whether create (i, i) connection ?
    kwargs : dict
        Other Parameters.

    Returns
    -------
    connection : tuple
        (pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic neuron
         for each pre-synaptic neuron)
    """
    assert isinstance(num_pre, int)
    assert isinstance(num_post, int)
    assert isinstance(num, int)

    conn_i = []
    conn_j = []
    for j in range(num_post):
        idx_selected = np.random.choice(num_pre, num, replace=False).tolist()
        if (not include_self) and (j in idx_selected):
            idx_selected.remove(j)
        size_pre = len(idx_selected)
        conn_i.extend(idx_selected)
        conn_j.extend([j] * size_pre)
    conn_i = np.asarray(conn_i)
    conn_j = np.asarray(conn_j)

    pre_indexes = []
    post_indexes = []
    pre_anchors = []
    ii = 0
    for i in range(num_pre):
        indexes = np.where(conn_i == i)[0]
        post_idx = conn_j[indexes]
        post_len = len(post_idx)
        pre_indexes.extend([i] * post_len)
        post_indexes.extend(post_idx)
        pre_anchors.append([ii, ii + post_len])
        ii += post_len
    pre_indexes = np.asarray(pre_indexes)
    post_indexes = np.asarray(post_indexes)
    pre_anchors = np.asarray(pre_anchors).T
    return pre_indexes, post_indexes, pre_anchors


def fixed_postnum(num_pre, num_post, num, include_self=True, **kwargs):
    """Connect the post-synaptic neurons with fixed number for each
    pre-synaptic neuron.

    Parameters
    ----------
    num_pre : int
        Number of neurons in the pre-synaptic group.
    num_post : int
        Number of neurons in the post-synaptic group.
    num : int
        The fixed connection number.
    include_self : bool
        Whether create (i, i) connection ?
    kwargs : dict
        Other Parameters.

    Returns
    -------
    connection : tuple
        (pre-synaptic neuron indexes,
         post-synaptic neuron indexes,
         start and end positions of post-synaptic neuron
         for each pre-synaptic neuron)
    """
    assert isinstance(num_pre, int)
    assert isinstance(num_post, int)
    assert isinstance(num, int)

    pre_indexes = []
    post_indexes = []
    pre_anchors = []
    ii = 0
    for i in range(num_pre):
        idx_selected = np.random.choice(num_post, num, replace=False).tolist()
        if (not include_self) and (i in idx_selected):
            idx_selected.remove(i)
        size_post = len(idx_selected)
        pre_indexes.extend([i] * size_post)
        post_indexes.extend(idx_selected)
        pre_anchors.append([ii, ii + size_post])
        ii += size_post
    pre_indexes = np.asarray(pre_indexes)
    post_indexes = np.asarray(post_indexes)
    pre_anchors = np.asarray(pre_anchors).T
    return pre_indexes, post_indexes, pre_anchors


def gaussian(num_pre, num_post, **kwargs):
    i, j = [], []
    return i, j


def dog(num_pre, num_post, **kwargs):
    i, j = [], []
    return i, j


def scale_free(num_pre, num_post, **kwargs):
    conn_i = []
    conn_j = []
    return conn_i, conn_j


def small_world(num_pre, num_post, **kwargs):
    conn_i = []
    conn_j = []
    return conn_i, conn_j


if __name__ == '__main__':
    from npbrain.utils import Dict

    # ii, jj, _ = one_to_one(6, 6)
    # ii, jj, _ = all_to_all(6, 6)
    # ii, jj, _ = all_to_all_no_equal(6, 6)

    # ii, jj, _ = grid_eight(2, 2)
    # ii, jj, _ = grid_eight(3, 3)
    # ii, jj, _ = grid_four(3, 3)

    # ii, jj, _ = fixed_prob(10, 10, 0.2)
    # ii, jj, _ = fixed_prob(10, 10, 0.35)
    # ii, jj, _ = fixed_prob_neq(10, 10, 0.2)
    # ii, jj, _ = fixed_prob_neq(10, 10, 0.35)

    # ii, jj, _ = fixed_prenum(10, 10, 2)
    # ii, jj, _ = fixed_prenum_neq(10, 10, 2)

    ii, jj, _ = fixed_postnum(10, 10, 2)
    # ii, jj, _ = fixed_postnum_neq(10, 10, 2)

    print('ii =', ii)
    print("jj =", jj)
    print('length =', len(ii))
