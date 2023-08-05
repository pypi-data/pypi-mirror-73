"""Calcifer API main module"""
import numpy as np
import scipy.sparse as scp
import scipy.sparse.linalg as linalg
import calcifer_pde.boundary as bndy

__all__ = ["heat_solve", "apply_bc"]


def heat_solve(dom, k_coeff=1.0, init_field=None, sterm_l=None, sterm_r=None):
    """
    :param dom: Calcifer domain
    :param k coeff: lambda_rho_cp
    :param sterm_l: LHS source term correction
    :param sterm_r: RHX source term correction
   
    :return:
        temperature field
    """
    if init_field is None:
        init_field = np.random.random_sample(dom.shp1d)

    if sterm_l is None:
        sterm_l = np.zeros_like(dom.lapl)

    if sterm_r is None:
        sterm_r = np.zeros(dom.shp1d)

    # Left Hand Side
    lhs_csr = dom.lapl * k_coeff + sterm_l
    # Right-Hand Side
    rhs_csr = np.zeros(dom.shp1d) + sterm_r

    lhs_csr_bc, rhs_csr_bc, grad_n_bc = apply_bc(dom, lhs_csr, rhs_csr)

    out_1d, info = scp.linalg.bicgstab(lhs_csr_bc, rhs_csr_bc, x0=init_field)
    if info == 0:
        print(".   ^_^ Resolution succesfull.")
    elif info > 0:
        print(".   t(-_-t) Resolution failed.")
    else:
        print(".   =_= Convergence not reached.")

    temp = out_1d.reshape(dom.shp2d)

    return temp


def apply_bc(dom, lhs, rhs):
    # pylint: disable=too-many-arguments
    """
    Give the altered version of LHS matrix and RHS vector to apply boundary
    conditions
    Parameters
    ----------
    lhs: left-hand side matrix (A in AX=B)
    rhs: right-hand side matrix (B in AX=B)
    metric: an instance of class Metrics2d containing gradient operators
    Returns
    -------
    lhs: modified left-hand side matrix
    rhs: modified right-hand side matrix
    """

    grad_n_bc = compute_normals(dom)
    bnd_nodes = dom.geo.bnd_nodes

    print("Apply Umin")
    lhs, rhs = umin_bnd(dom, lhs, rhs, bnd_nodes, grad_n_bc)

    print("Apply Umax")
    lhs, rhs = umax_bnd(dom, lhs, rhs, bnd_nodes, grad_n_bc)

    print("Apply Vmin")
    lhs, rhs = vmin_bnd(dom, lhs, rhs, bnd_nodes, grad_n_bc)

    print("Apply Vmax")
    lhs, rhs = vmax_bnd(dom, lhs, rhs, bnd_nodes, grad_n_bc)

    return lhs, rhs, grad_n_bc


def compute_normals(dom):
    # pylint: disabledom.ytoo-many-arguments
    """
    Compute unit normal vector over the boundaries
    Parameters
    ----------
    Arrays of unit normal vectors : nx and ny.
    """
    normal = np.zeros((dom.shp1d, 2))
    for bnd_name in ["umax", "umin", "vmax", "vmin"]:

        idx = dom.geo.bnd_nodes[bnd_name]
        vect = dom.geo.bnd_normal[bnd_name]
        norm = np.hypot(vect[:, 0], vect[:, 1])

        normal[idx, :] = vect / norm[:, np.newaxis]

    n_x = scp.csr_matrix(np.diag(normal[:, 0]))
    n_y = scp.csr_matrix(np.diag(normal[:, 1]))
    nx_grad_x = n_x.dot(dom.grad_x_csr)
    ny_grad_y = n_y.dot(dom.grad_y_csr)
    grad_n_bc = nx_grad_x + ny_grad_y

    return grad_n_bc


def umin_bnd(dom, lhs, rhs, bnd_nodes, grad_n):
    """boundary treatment verification"""
    type_bc = dom.bc_umin_type
    bc_value = dom.bc_umin_values
    nodes = bnd_nodes["umin"]
    if type_bc == "periodic":
        pass  # Nothing to do
    elif type_bc == "dirichlet":
        dirichlet_value = bc_value
        lhs, rhs = bndy.bc_dirichlet(lhs, rhs, nodes, grad_n, dirichlet_value)
    elif type_bc == "neumann":
        neumann_value = bc_value
        lhs, rhs = bndy.bc_neumann(lhs, rhs, nodes, grad_n, neumann_value)
    elif type_bc == "symmetric":
        pass  # Nothing to do
    else:
        raise NotImplementedError("BC type :", type_bc)
    return lhs, rhs


def umax_bnd(dom, lhs, rhs, bnd_nodes, grad_n):
    """boundary treatment verification"""
    type_bc = dom.bc_umax_type
    bc_value = dom.bc_umax_values
    nodes = bnd_nodes["umax"]
    if type_bc == "periodic":
        pass  # Nothing to do
    elif type_bc == "dirichlet":
        dirichlet_value = bc_value
        lhs, rhs = bndy.bc_dirichlet(lhs, rhs, nodes, grad_n, dirichlet_value)
    elif type_bc == "neumann":
        neumann_value = bc_value
        lhs, rhs = bndy.bc_neumann(lhs, rhs, nodes, grad_n, neumann_value)
    elif type_bc == "symmetric":
        pass  # Nothing to do
    else:
        raise NotImplementedError("BC type :", type_bc)

    return lhs, rhs


def vmin_bnd(dom, lhs, rhs, bnd_nodes, grad_n):
    """Boundary verification"""
    type_bc = dom.bc_vmin_type
    bc_value = dom.bc_vmin_values
    nodes = bnd_nodes["vmin"]
    if type_bc == "periodic":
        pass  # Nothing to do
    elif type_bc == "dirichlet":
        dirichlet_value = bc_value
        lhs, rhs = bndy.bc_dirichlet(lhs, rhs, nodes, grad_n, dirichlet_value)
    elif type_bc == "neumann":
        neumann_value = bc_value
        lhs, rhs = bndy.bc_neumann(lhs, rhs, nodes, grad_n, neumann_value)
    elif type_bc == "symmetric":
        pass  # Nothing to do
    else:
        raise NotImplementedError("BC type :", type_bc)

    return lhs, rhs


def vmax_bnd(dom, lhs, rhs, bnd_nodes, grad_n):
    """Boundary verification"""
    type_bc = dom.bc_vmax_type
    bc_value = dom.bc_vmax_values
    nodes = bnd_nodes["vmax"]
    if type_bc == "periodic":
        pass  # Nothing to do
    elif type_bc == "dirichlet":
        dirichlet_value = bc_value
        lhs, rhs = bndy.bc_dirichlet(lhs, rhs, nodes, grad_n, dirichlet_value)
    elif type_bc == "neumann":
        neumann_value = bc_value
        lhs, rhs = bndy.bc_neumann(lhs, rhs, nodes, grad_n, neumann_value)
    elif type_bc == "symmetric":
        pass  # Nothing to do
    else:
        raise NotImplementedError("BC type :", type_bc)

    return lhs, rhs
