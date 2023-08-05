""" domain"""
import numpy as np
import scipy.sparse as scp

__all__ = ["Domain"]


class Domain:
    """
    Convention
    west-esat is the first dimension
    north-south is the second dimension

          ---> v 
               first dimension 
               east 0 to west max
               index i
     
      ______________
      |            |  ^
      |            |  | 
      |            |  |
      |            | 
      |            |  u   
      |            |  second dimension south 0 to north (max)' index i
      |____________|  south 0 to north (max)'
                      index j

    """

    def __init__(self, geo):

        self.geo = geo

        self.size_we, self.size_ns = self.geo.shape
        self.shp2d = self.geo.shape
        self.shp1d = self.size_we * self.size_ns

        self.periodic_ns = False
        self.periodic_we = False

    def compute_operators(self, second_order=True):
        """Compute the operators of the domain."""

        self._compute_metric()
        if second_order:
            self._compute_matrices_order2()
        else:
            self._compute_matrices_order1()

    def _compute_metric(self):
        """Invert the jacobian matrix."""
        jacob = self.geo.dxdu * self.geo.dydv - self.geo.dxdv * self.geo.dydu
        inv_jacob = np.reciprocal(jacob)
        self.invj_dxdu = inv_jacob * self.geo.dxdu
        self.invj_dxdv = inv_jacob * self.geo.dxdv
        self.invj_dydu = inv_jacob * self.geo.dydu
        self.invj_dydv = inv_jacob * self.geo.dydv

    def _compute_matrices_order1(self):
        # pylint: disable=too-many-locals
        """ compute the matrix form of operators """
        size_we = self.size_we
        size_ns = self.size_ns
        # vecteurs indiquant lindex du voisin
        # ip1,  a la position i, vaut i+1
        ip1 = np.arange(1, size_we + 1)
        jp1 = np.arange(1, size_ns + 1)
        im1 = np.arange(-1, size_we - 1)
        jm1 = np.arange(-1, size_ns - 1)
        # coeeficient aappliquer sur la positio i
        cfi_sb = np.ones(size_we) * 0.5
        cfj_sb = np.ones(size_ns) * 0.5
        # traite les bords
        if self.periodic_we:
            im1[0] = size_we - 1
            ip1[-1] = 1
        else:
            im1[0] = 0
            ip1[-1] = size_we - 1
            cfi_sb[0], cfi_sb[-1] = 1.0, 1.0
        if self.periodic_ns:
            jm1[0] = size_ns - 1
            jp1[-1] = 1
        else:
            jm1[0] = 0
            jp1[-1] = size_ns - 1
            cfj_sb[0], cfj_sb[-1] = 1.0, 1.0
        # repetition des vecteurs sur l'ensemble de la matrice
        cfi = np.repeat(cfi_sb, size_ns)
        cfj = np.tile(cfj_sb, size_we)
        # recupere les valeurs dans une matrice size x size
        iters_i = np.repeat(np.arange(size_we), size_ns)
        iters_j = np.tile(np.arange(size_ns), size_we)

        iters_ip1 = np.repeat(ip1, size_ns)
        iters_im1 = np.repeat(im1, size_ns)
        iters_jp1 = np.tile(jp1, size_we)
        iters_jm1 = np.tile(jm1, size_we)

        ijc_array = np.arange(self.shp1d)

        point_ij = ijc_array[iters_i * size_ns + iters_j]
        point_jp1 = ijc_array[iters_i * size_ns + iters_jp1]
        point_jm1 = ijc_array[iters_i * size_ns + iters_jm1]
        point_ip1 = ijc_array[iters_j + iters_ip1 * size_ns]
        point_im1 = ijc_array[iters_j + iters_im1 * size_ns]

        # Build gradient X
        column_x = np.concatenate(
            (
                point_ij[:, None],
                point_jm1[:, None],
                point_ij[:, None],
                point_im1[:, None],
            ),
            axis=1,
        ).ravel()
        array_x = np.concatenate(
            (
                (cfj * self.invj_dydv.ravel())[:, None],
                (-cfj * self.invj_dydv.ravel())[:, None],
                (-cfi * self.invj_dydu.ravel())[:, None],
                (cfi * self.invj_dydu.ravel())[:, None],
            ),
            axis=1,
        ).ravel()

        grad_x = scp.csr_matrix(
            (array_x, (np.repeat(ijc_array, 4), column_x)),
            shape=(self.shp1d, self.shp1d),
        )

        column_xp1 = np.concatenate(
            (
                point_jp1[:, None],
                point_ij[:, None],
                point_ip1[:, None],
                point_ij[:, None],
            ),
            axis=1,
        ).ravel()

        grad_xp1 = scp.csr_matrix(
            (array_x, (np.repeat(ijc_array, 4), column_xp1)),
            shape=(self.shp1d, self.shp1d),
        )

        # Build gradient Y
        column_y = np.concatenate(
            (
                point_ij[:, None],
                point_im1[:, None],
                point_ij[:, None],
                point_jm1[:, None],
            ),
            axis=1,
        ).ravel()
        column_yp1 = np.concatenate(
            (
                point_ip1[:, None],
                point_ij[:, None],
                point_jp1[:, None],
                point_ij[:, None],
            ),
            axis=1,
        ).ravel()
        array_y = np.concatenate(
            (
                (cfi * self.invj_dxdu.ravel())[:, None],
                (-cfi * self.invj_dxdu.ravel())[:, None],
                (-cfj * self.invj_dxdv.ravel())[:, None],
                (cfj * self.invj_dxdv.ravel())[:, None],
            ),
            axis=1,
        ).ravel()
        grad_y = scp.csr_matrix(
            (array_y, (np.repeat(ijc_array, 4), column_y)),
            shape=(self.shp1d, self.shp1d),
        )
        grad_yp1 = scp.csr_matrix(
            (array_y, (np.repeat(ijc_array, 4), column_yp1)),
            shape=(self.shp1d, self.shp1d),
        )

        self.grad_x_csr = grad_x
        self.grad_y_csr = grad_y

        self.lapl = grad_x.dot(grad_xp1) + grad_y.dot(grad_yp1)  # .tolil()

    def _compute_matrices_order2(self):
        # pylint: disable=too-many-locals
        """ compute the matrix form of operators """

        size_we = self.size_we
        size_ns = self.size_ns
        # vecteurs indiquant lindex du voisin
        # ip1,  a la position i, vaut i+1
        ip1 = np.arange(1, size_we + 1)
        jp1 = np.arange(1, size_ns + 1)
        im1 = np.arange(-1, size_we - 1)
        jm1 = np.arange(-1, size_ns - 1)
        # coeeficient aappliquer sur la positio i
        cfi_sb = np.ones(size_we) * 0.5
        cfj_sb = np.ones(size_ns) * 0.5
        # traite les bords
        if self.periodic_we:
            im1[0] = size_we - 1
            ip1[-1] = 1
        else:
            im1[0] = 0
            ip1[-1] = size_we - 1
            cfi_sb[0], cfi_sb[-1] = 1.0, 1.0
        if self.periodic_ns:
            jm1[0] = size_ns - 1
            jp1[-1] = 1
        else:
            jm1[0] = 0
            jp1[-1] = size_ns - 1
            cfj_sb[0], cfj_sb[-1] = 1.0, 1.0
        # repetition des vecteurs sur l'ensemble de la matrice
        cfi = np.repeat(cfi_sb, size_ns)
        cfj = np.tile(cfj_sb, size_we)
        # recupere les valeurs dans une matrice size x size
        iters_i = np.repeat(np.arange(size_we), size_ns)
        iters_j = np.tile(np.arange(size_ns), size_we)

        iters_ip1 = np.repeat(ip1, size_ns)
        iters_im1 = np.repeat(im1, size_ns)
        iters_jp1 = np.tile(jp1, size_we)
        iters_jm1 = np.tile(jm1, size_we)

        ijc_array = np.arange(self.shp1d)
        point_jp1 = ijc_array[iters_i * size_ns + iters_jp1]
        point_jm1 = ijc_array[iters_i * size_ns + iters_jm1]
        point_ip1 = ijc_array[iters_j + iters_ip1 * size_ns]
        point_im1 = ijc_array[iters_j + iters_im1 * size_ns]
        # Build gradient X
        column_x = np.concatenate(
            (
                point_jp1[:, None],
                point_jm1[:, None],
                point_ip1[:, None],
                point_im1[:, None],
            ),
            axis=1,
        ).ravel()
        array_x = np.concatenate(
            (
                (cfj * self.invj_dydv.ravel())[:, None],
                (-cfj * self.invj_dydv.ravel())[:, None],
                (-cfi * self.invj_dydu.ravel())[:, None],
                (cfi * self.invj_dydu.ravel())[:, None],
            ),
            axis=1,
        ).ravel()

        grad_x = scp.csr_matrix(
            (array_x, (np.repeat(ijc_array, 4), column_x)),
            shape=(self.shp1d, self.shp1d),
        )

        # Build gradient Y
        column_y = np.concatenate(
            (
                point_ip1[:, None],
                point_im1[:, None],
                point_jp1[:, None],
                point_jm1[:, None],
            ),
            axis=1,
        ).ravel()
        array_y = np.concatenate(
            (
                (cfi * self.invj_dxdu.ravel())[:, None],
                (-cfi * self.invj_dxdu.ravel())[:, None],
                (-cfj * self.invj_dxdv.ravel())[:, None],
                (cfj * self.invj_dxdv.ravel())[:, None],
            ),
            axis=1,
        ).ravel()
        grad_y = scp.csr_matrix(
            (array_y, (np.repeat(ijc_array, 4), column_y)),
            shape=(self.shp1d, self.shp1d),
        )
        self.lapl = grad_x.dot(grad_x) + grad_y.dot(grad_y)  # .tolil()
        self.grad_x_csr = grad_x
        self.grad_y_csr = grad_y

    def switch_bc_umin_dirichlet(self, dict_):
        """ set to a symmetry : null gradients."""
        self.bc_umin_type = "dirichlet"
        self.bc_umin_values = dict_

    def switch_bc_umax_dirichlet(self, dict_):
        """ set to a symmetry : null gradients."""
        self.bc_umax_type = "dirichlet"
        self.bc_umax_values = dict_

    def switch_bc_umax_neumann(self, neum_):
        """ set to a symmetry : null gradients."""
        self.bc_umax_type = "neumann"
        self.bc_umax_values = neum_

    def switch_bc_umin_neumann(self, neum_):
        """ set to a symmetry : null gradients."""
        self.bc_umin_type = "neumann"
        self.bc_umin_values = neum_

    def switch_bc_vmin_dirichlet(self, dict_):
        """ set to a symmetry : null gradients."""
        self.bc_vmin_type = "dirichlet"
        self.bc_vmin_values = dict_

    def switch_bc_vmax_dirichlet(self, dict_):
        """ set to a symmetry : null gradients."""
        self.bc_vmax_type = "dirichlet"
        self.bc_vmax_values = dict_

    def switch_bc_vmax_neumann(self, neum_):
        """ set to a symmetry : null gradients."""
        self.bc_vmax_type = "neumann"
        self.bc_vmax_values = neum_

    def switch_bc_vmin_neumann(self, neum_):
        """ set to a symmetry : null gradients."""
        self.bc_vmin_type = "neumann"
        self.bc_vmin_values = neum_

    def switch_bc_u_perio(self):
        """ set to a x-periodic domain."""
        self.bc_umax_type = "periodic"
        self.bc_umax_values = dict()
        self.bc_umin_type = "periodic"
        self.bc_umin_values = dict()
        self.periodic_ns = True

    def switch_bc_v_perio(self):
        """ set to a y-periodic domain."""
        self.bc_vmax_type = "periodic"
        self.bc_vmax_values = dict()
        self.bc_vmin_type = "periodic"
        self.bc_vmin_values = dict()
        self.periodic_we = True

    # TODO: symmetric condition is not validated
    def switch_bc_umin_symmetric(self):
        """ set to a symmetry : null gradients."""
        self.bc_umin_type = "symmetric"
        self.bc_umin_values = dict()

    def switch_bc_umax_symmetric(self):
        """ set to a symmetry : null gradients."""
        self.bc_umax_type = "symmetric"
        self.bc_umax_values = dict()

    def switch_bc_vmin_symmetric(self):
        """ set to a symmetry : null gradients."""
        self.bc_vmin_type = "symmetric"
        self.bc_vmin_values = dict()

    def switch_bc_vmax_symmetric(self):
        """ set to a symmetry : null gradients."""
        self.bc_vmax_type = "symmetric"
        self.bc_vmax_values = dict()
