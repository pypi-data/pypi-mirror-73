"""
Contains class and functions necessary to handle boundary conditions
"""

import numpy as np
import scipy.sparse as scp

__all__ = ["bc_dirichlet"]


def bc_robin(matrix_lhs, matrix_rhs, positions, grad_n_bc, a_val, b_val, c_val):
    """
    Function to enforce the Boundary Condition in the Robin formalism:

                    a * (df / dn) + b * f + c = O

    Parameters
    ----------
    matrix_lhs: Left Hand Side square matrix (shape (size_i_w * size_j_ns)^2)
    matrix_rhs: Right Hand Side vector (shape (size_i_w * size_j_ns))
    positions: indices of lines corresponding to the patch being processed
    grad_n_bc: normal gradient to boundary nodes
    a_val: value of the "a" Robin parameter
    b_val: value of the "b" Robin parameter
    c_val: value of the "a" Robin parameter

    Returns
    -------
    Altered left-hand side matrix and right-hand side vector
    """

    for row in positions:
        if grad_n_bc.count_nonzero():
            new_row = a_val * grad_n_bc.getrow(row).toarray().ravel()
            set_row_csr(matrix_lhs, row, new_row)

    diag_bc = np.zeros(matrix_rhs.shape)
    diag_bc[positions] = b_val
    mat_bc_b_csr = scp.csr_matrix(np.diag(diag_bc))
    matrix_lhs += mat_bc_b_csr

    matrix_rhs[positions] = -c_val

    return matrix_lhs, matrix_rhs


def bc_neumann(matrix_lhs, matrix_rhs, positions, grad_n_bc, target_gradient):
    """
    Function to enforce the Neumann Boundary Condition in the Robin formalism:

                    a * (df / dn) + b * f + c = O

    Parameters
    ----------
    grad_n_bc
    target_gradient
    matrix_lhs : Left Hand Side square matrix (shape (size_i_w * size_j_ns)^2)
    matrix_rhs : Right Hand Side vector (shape (size_i_w * size_j_ns))
    positions : indices of lines corresponding to the patch being processed

    Returns
    -------
    Altered left-hand side matrix and right-hand side vector
    """

    print("Neumann bc target -->", target_gradient)

    lhs_out, rhs_out = bc_robin(
        matrix_lhs, matrix_rhs, positions, grad_n_bc, 1.0, 0.0, -target_gradient
    )

    return lhs_out, rhs_out


def bc_dirichlet(matrix_lhs, matrix_rhs, positions, grad_n_bc, target_value):
    """
    Function to enforce Dirichlet Boundary Condition in the Robin formalism:

                    a * (df / dn) + b * f + c = O

    Parameters
    ----------
    target_value
    matrix_lhs : Left Hand Side square matrix (shape (size_i_w * size_j_ns)^2)
    matrix_rhs : Right Hand Side vector (shape (size_i_w * size_j_ns))
    positions : indices of lines corresponding to the patch being processed

    Returns
    -------
    Altered left-hand side matrix and right-hand side vector
    """
    print("Dirichlet bc target -->", target_value)

    # lhs_out, rhs_out = bc_robin_csr(matrix_lhs, matrix_rhs, positions,
    #                                 grad_n_bc, 0., 1., -target_value)
    lhs_out, rhs_out = bc_robin(
        matrix_lhs, matrix_rhs, positions, grad_n_bc, 0.0, 1.0, -target_value
    )

    return lhs_out, rhs_out


def set_row_csr(csr, row_idx, new_row):
    """
    Replace a row in a CSR sparse matrix A.

    Parameters
    ----------
    csr: csr_matrix
        Matrix to change
    row_idx: int
        index of the row to be changed
    new_row: np.array
        list of new values for the row of A

    Returns
    -------
    None (the matrix A is changed in place)

    Prerequisites
    -------------
    The row index shall be smaller than the number of rows in A
    The number of elements in new row must be equal to the number of columns in
    matrix A
    """

    assert scp.isspmatrix_csr(csr), "A shall be a csr_matrix"
    assert (
        row_idx < csr.shape[0]
    ), "The row index ({0}) shall be smaller than the number of rows in A ({1})".format(
        row_idx, csr.shape[0]
    )
    try:
        n_elements_new_row = len(new_row)
    except TypeError:
        msg = "Argument new_row shall be a list or numpy array, is now a {0}".format(
            type(new_row)
        )
        raise AssertionError(msg)
    n_cols = csr.shape[1]
    assert n_cols == n_elements_new_row, (
        "The number of elements in new row ({0}) must be equal to "
        "the number of columns in matrix A ({1})".format(n_elements_new_row, n_cols)
    )

    idx_start = csr.indptr[row_idx]
    idx_end = csr.indptr[row_idx + 1]
    additional_nnz = n_cols - (idx_end - idx_start)

    # Substitute dense data
    csr.data = np.r_[csr.data[:idx_start], new_row, csr.data[idx_end:]]

    # Correct indices
    csr.indices = np.r_[
        csr.indices[:idx_start], np.arange(n_cols), csr.indices[idx_end:]
    ]

    # Correct indptr
    csr.indptr = np.r_[
        csr.indptr[: row_idx + 1], csr.indptr[(row_idx + 1) :] + additional_nnz
    ]
