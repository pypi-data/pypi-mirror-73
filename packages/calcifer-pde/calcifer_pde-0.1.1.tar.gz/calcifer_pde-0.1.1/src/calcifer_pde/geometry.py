""" geometriesforcalcifer

In these geometries

x (resp y) is the absolute coordinate.
u (resp v) is the local coordinate aligned with the grid.



"""
import numpy as np
from calcifer_pde.diff import diff_first_dim, diff_scnd_dim

__all__ = ["Square", "Donut", "Donut_Local", "Staggered", "Sphere", "Shell"]


class Square:
    """Square geometry.

    ::
          u = x --->

      ______________
      |            |  ^
      |            |  | 
      |            |  |
      |            | 
      |            | v = y
      |            |
      |____________|

    """

    def __init__(self, nx, ny, len_x, len_y, auto_metric=True):

        self.shape = (ny, nx)
        self.bnd_nodes = get_bnd_nodes(self.shape)
        x_vec = np.linspace(0.0, len_x, self.shape[1], endpoint=True)
        y_vec = np.linspace(0.0, len_y, self.shape[0], endpoint=True)
        self.x_coor, self.y_coor = np.meshgrid(x_vec, y_vec)
        self.z_coor = np.zeros(self.shape)

        if auto_metric:
            self.dxdu = diff_scnd_dim(self.x_coor)
            self.dydu = diff_scnd_dim(self.y_coor)
            self.dxdv = diff_first_dim(self.x_coor)
            self.dydv = diff_first_dim(self.y_coor)
        else:
            self.dxdu = len_x / (nx - 1) * np.ones_like(self.x_coor)
            self.dydv = len_y / (ny - 1) * np.ones_like(self.x_coor)
            self.dxdv = 0.0 * np.zeros_like(self.x_coor)
            self.dydu = 0.0 * np.zeros_like(self.x_coor)

        self.bnd_normal = {}
        idx = self.bnd_nodes["umax"]
        self.bnd_normal["umax"] = -np.stack(
            (self.dxdu.ravel()[idx], self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["umin"]
        self.bnd_normal["umin"] = -np.stack(
            (-self.dxdu.ravel()[idx], -self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmax"]
        self.bnd_normal["vmax"] = -np.stack(
            (self.dxdv.ravel()[idx], self.dydv.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmin"]
        self.bnd_normal["vmin"] = -np.stack(
            (-self.dxdv.ravel()[idx], -self.dydv.ravel()[idx]), axis=1
        )


class Staggered:
    """Stagerred Square geometry.

    ::
          u = x --->

      ______________
      |            |  ^
      |            |  | 
      |            |  |
      |            | 
      |            | v = y
      |            |
      |____________|

    Shows that autoatic differenciation does not work 
    on varable sampling meshes

    """

    def __init__(self, nx, ny, len_x, len_y):
        self.shape = (ny, nx)
        self.bnd_nodes = get_bnd_nodes(self.shape)
        x_vec = np.linspace(0.0, len_x, self.shape[1], endpoint=True)
        y_vec = np.linspace(0.0, len_y, self.shape[0], endpoint=True)
        self.x_coor, self.y_coor = np.meshgrid(x_vec, y_vec)
        self.z_coor = np.zeros(self.shape)

        jam_x = np.random.random_sample(self.shape) - 0.5
        jam_y = np.random.random_sample(self.shape) - 0.5
        jam_x[0, :] = 0
        jam_x[-1, :] = 0
        jam_x[:, 0] = 0
        jam_x[:, -1] = 0
        jam_y[0, :] = 0
        jam_y[-1, :] = 0
        jam_y[:, 0] = 0
        jam_y[:, -1] = 0

        self.x_coor += jam_x * len_x / nx * 0.4
        self.y_coor += jam_y * len_y / nx * 0.4
        self.dxdu = diff_scnd_dim(self.x_coor)
        self.dydu = diff_scnd_dim(self.y_coor)
        self.dxdv = diff_first_dim(self.x_coor)
        self.dydv = diff_first_dim(self.y_coor)

        self.bnd_normal = {}
        idx = self.bnd_nodes["umax"]
        self.bnd_normal["umax"] = -np.stack(
            (self.dxdu.ravel()[idx], self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["umin"]
        self.bnd_normal["umin"] = -np.stack(
            (-self.dxdu.ravel()[idx], -self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmax"]
        self.bnd_normal["vmax"] = -np.stack(
            (self.dxdv.ravel()[idx], self.dydv.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmin"]
        self.bnd_normal["vmin"] = -np.stack(
            (-self.dxdv.ravel()[idx], -self.dydv.ravel()[idx]), axis=1
        )


class Donut:
    """Donut geometry.

    x and y and the absolute coordinates
    dxdu, dydu dxdv dydv are the absolute jacobian
    ::
           x --->

             _____         ^
                  '-. umax |
       vmax      .   '.    | y
                / u    \
             "-.        ;
                \   .   ;
         umin       ;   \v ;

                  vmin

    """

    def __init__(
        self, nr, ntheta, r_min, r_max, theta_min, theta_max, auto_metric=True
    ):

        self.shape = (ntheta, nr)
        self.bnd_nodes = get_bnd_nodes(self.shape)
        radius = np.linspace(r_min, r_max, nr, endpoint=True)
        azimuth = np.linspace(theta_min, theta_max, ntheta, endpoint=True)
        r_coor, theta_coor = np.meshgrid(radius, azimuth)

        self.x_coor = r_coor * np.cos(theta_coor)
        self.y_coor = r_coor * np.sin(theta_coor)
        self.z_coor = np.zeros_like(self.y_coor)

        self.dr = np.full(self.shape, (r_max - r_min) / nr)
        self.dtheta = np.full(self.shape, (theta_max - theta_min) / ntheta)
        self.radius = np.ones(self.shape) * radius[np.newaxis, :]
        self.rdtheta = self.dtheta * self.radius

        self.analytic = np.tile(
            np.log(radius / r_min) / np.log(r_max / r_min) * (500 - 200) + 200,
            (self.shape[0], 1),
        )

        if auto_metric:
            self.dxdu = diff_scnd_dim(self.x_coor)
            self.dydu = diff_scnd_dim(self.y_coor)
            self.dxdv = diff_first_dim(self.x_coor)
            self.dydv = diff_first_dim(self.y_coor)
        else:
            self.dxdu = self.dr * self.x_coor / self.radius
            self.dxdv = -self.rdtheta * self.y_coor / self.radius
            self.dydu = self.dr * self.y_coor / self.radius
            self.dydv = self.rdtheta * self.x_coor / self.radius

        self.bnd_normal = {}
        idx = self.bnd_nodes["umax"]
        self.bnd_normal["umax"] = -np.stack(
            (self.dxdu.ravel()[idx], self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["umin"]
        self.bnd_normal["umin"] = -np.stack(
            (-self.dxdu.ravel()[idx], -self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmax"]
        self.bnd_normal["vmax"] = -np.stack(
            (self.dxdv.ravel()[idx], self.dydv.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmin"]
        self.bnd_normal["vmin"] = -np.stack(
            (-self.dxdv.ravel()[idx], -self.dydv.ravel()[idx]), axis=1
        )


class Donut_Local(Donut):
    """Same as donut, but with a local frame

    x and y and the absolute coordinates
    dxdu, dydu dxdv dydv are the LOCAL frame jacobian
    """

    def __init__(self, nr, ntheta, r_min, r_max, theta_min, theta_max):
        super().__init__(nr, ntheta, r_min, r_max, theta_min, theta_max)

        # Override jacobian components by alignement on local frame.
        self.dxdu = self.dr
        self.dxdv = np.zeros(self.shape)
        self.dydu = np.zeros(self.shape)
        self.dydv = self.rdtheta

        self.bnd_normal = {}
        idx = self.bnd_nodes["umax"]
        self.bnd_normal["umax"] = -np.stack(
            (self.dxdu.ravel()[idx], self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["umin"]
        self.bnd_normal["umin"] = -np.stack(
            (-self.dxdu.ravel()[idx], -self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmax"]
        self.bnd_normal["vmax"] = -np.stack(
            (self.dxdv.ravel()[idx], self.dydv.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmin"]
        self.bnd_normal["vmin"] = -np.stack(
            (-self.dxdv.ravel()[idx], -self.dydv.ravel()[idx]), axis=1
        )


class Sphere:
    def __init__(self, nphi, ntheta, rad):
        self.shape = (ntheta, nphi)
        self.bnd_nodes = get_bnd_nodes(self.shape)
        radius = np.full(self.shape, rad)
        angle_theta = np.linspace(-np.pi, np.pi, ntheta, endpoint=True)
        phi_max = 0.9 * np.pi
        phi_min = 0.1 * np.pi
        angle_phi = np.linspace(phi_min, phi_max, nphi, endpoint=True)

        self.x_coor = (
            radius
            * np.cos(angle_theta[:, np.newaxis])
            * np.sin(angle_phi[np.newaxis, :])
        )
        self.y_coor = (
            radius
            * np.sin(angle_theta[:, np.newaxis])
            * np.sin(angle_phi[np.newaxis, :])
        )
        self.z_coor = -radius * np.cos(angle_phi[np.newaxis, :])
        self.du = np.full(self.shape, rad * (phi_max - phi_min) / nphi)
        self.dr = self.du * np.cos(angle_phi[np.newaxis, :])
        # self.dz = np.full(self.shape, 10/nr)
        self.dtheta = np.full(self.shape, (2 * np.pi) / ntheta)
        self.radius = radius * np.sin(angle_phi[np.newaxis, :])
        self.rdtheta = self.dtheta * self.radius

        self.dxdu = self.du
        self.dxdv = np.zeros(self.shape)
        self.dydu = np.zeros(self.shape)
        self.dydv = self.rdtheta

        coefmin = np.log(np.tan(phi_min / 2.0))
        coefmax = np.log(np.tan(phi_max / 2.0))
        dum_a = (500.0 - 200.0) / (coefmax - coefmin)
        dum_b = 200.0 - coefmin * dum_a
        dum = np.log(np.tan(angle_phi / 2.0)) * dum_a + dum_b

        self.analytic = np.tile(dum, (self.shape[0], 1))
        # self.analytic = np.tile(np.log(radius / r_min) / np.log(r_max / r_min) * (500 - 200) + 200,
        #                        (self.shape[0], 1))

        self.bnd_normal = {}
        idx = self.bnd_nodes["umax"]
        self.bnd_normal["umax"] = -np.stack(
            (self.dxdu.ravel()[idx], self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["umin"]
        self.bnd_normal["umin"] = -np.stack(
            (-self.dxdu.ravel()[idx], -self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmax"]
        self.bnd_normal["vmax"] = -np.stack(
            (self.dxdv.ravel()[idx], self.dydv.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmin"]
        self.bnd_normal["vmin"] = -np.stack(
            (-self.dxdv.ravel()[idx], -self.dydv.ravel()[idx]), axis=1
        )


class Shell:
    """Arnica Shell geometry.

    ::
          u = x --->
    longitudinal direction
      ______________
      |            |  ^
      |            |  |
      |            |  |
      |            |
      |            | v = y
      |            |azimuthal direction
      |____________|

    """

    def __init__(self, shell_):

        self.shape = shell_.shape
        self.bnd_nodes = get_bnd_nodes(self.shape)
        self.x_coor = shell_.xyz[:, :, 0]
        self.y_coor = shell_.xyz[:, :, 1]
        self.z_coor = shell_.xyz[:, :, 2]
        self.dxdu = shell_.du
        self.dxdv = np.zeros_like(shell_.du)
        self.dydu = np.zeros_like(shell_.du)
        self.dydv = shell_.dv

        self.bnd_normal = {}
        idx = self.bnd_nodes["umax"]
        self.bnd_normal["umax"] = -np.stack(
            (self.dxdu.ravel()[idx], self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["umin"]
        self.bnd_normal["umin"] = -np.stack(
            (-self.dxdu.ravel()[idx], -self.dydu.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmax"]
        self.bnd_normal["vmax"] = -np.stack(
            (self.dxdv.ravel()[idx], self.dydv.ravel()[idx]), axis=1
        )
        idx = self.bnd_nodes["vmin"]
        self.bnd_normal["vmin"] = -np.stack(
            (-self.dxdv.ravel()[idx], -self.dydv.ravel()[idx]), axis=1
        )


def get_bnd_nodes(shape):
    """
    Gives node number of boundary patches

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
    size_ns = shape[1]
    size_we = shape[0]

    # Flip of numpy array necessary to compute the normals
    i_we = size_we - 1
    # north = np.flip(
    east = np.flip(np.array([(j_idx + size_ns * i_we) for j_idx in range(size_ns)]))
    # Flip of numpy array necessary to compute the normals
    j_ns = 0
    # west = np.flip(
    south = np.flip(np.array([(j_ns + size_ns * i_idx) for i_idx in range(size_we)]))
    i_we = 0
    # south = np.array(
    west = np.array([(j_idx + size_ns * i_we) for j_idx in range(size_ns)])

    j_ns = size_ns - 1
    # east = np.array(
    north = np.array([(j_ns + size_ns * i_idx) for i_idx in range(size_we)])

    bnd_nodes = {}

    # TODO: check the directions to be clear
    bnd_nodes["vmax"] = east
    bnd_nodes["umin"] = south
    bnd_nodes["vmin"] = west
    bnd_nodes["umax"] = north

    return bnd_nodes
