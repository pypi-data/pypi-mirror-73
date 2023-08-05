from math import ceil, factorial, sqrt

import astropy.units as u
import numpy as np
from scipy.optimize import minimize

from . import logging

__all__ = ['zernike', 'zernike_j', 'fit_zernikes_j', 'fit_zernikes_j_lstsq',
           'construct_wavefront_from_js']

logger = logging.get_standard_logger(__name__)


def zernike_j(j, rho, theta, normalize=True, fill_value=0):
    """Calculates zernike polynomial for given indices j index (OSA) for rho
    and theta. Implementation based on [1]. If normalize is `True` output is
    normalized following Noll's convention [2].

    :param j: OSA index
    :type j: int
    :param rho: radial coordinates of the plane,
    :type rho: numpy.array
    :param theta: angle coordinate of the plane
    :type theta: numpy.array
    :param normalize: Should output be normalized following Noll's convention?
    :type normalize: bool
    :param fill_value: what value should be put for r > 1
    :type fill_value: numeric
    :return: resulting zernike distribution
    :rtype: numpy.array


    **Example**

    >>> import astropy.units as u
    >>> import pyoptica as po
    >>>
    >>> npix = 101
    >>> pixel_scale = 0.5 * u.m
    >>> x, y = po.utils.mesh_grid(npix, pixel_scale)
    >>> r_max = .5 * npix * pixel_scale
    >>> r, theta = po.utils.cart2pol(x, y)
    >>> r = r / r_max
    >>> j = 8  # Y-Coma
    >>> z = po.zernikes.zernike_j(j, r, theta)

    **References**

    [1] Vasudevan Lakshminarayanan and Andre Fleck (2011) -
    *Zernike polynomials: a guide*, Journal of Modern Optics
    
    [2] Robert J. Noll (1976) -
    "*Zernike polynomials and atmospheric turbulence*," J. Opt. Soc. Am. 66, 207-211

    """
    m, n = j_to_mn(j)
    return zernike(m, n, rho, theta, normalize, fill_value)


def zernike(m, n, rho, theta, normalize=True, fill_value=0):
    """Calculates zernike polynomial for given indices m, n for rho and theta.
    Implementation based on [1]. If normalize is `True` output is normalized
    following Noll's convention [2].


    :param m: zernike m-degree, angular frequency
    :type m: int
    :param n: zernike n-degree, radial order
    :type n: int
    :param rho: radial coordinates of the plane,
    :type rho: numpy.array
    :param theta: angle coordinate of the plane
    :type theta: numpy.array
    :param normalize: Should output be normalized following Noll's convention?
    :type normalize: bool
    :param fill_value: what value should be put for r > 1
    :type fill_value: numeric
    :return: resulting zernike distribution
    :rtype: numpy.array

    **Example**

    >>> import astropy.units as u
    >>> import pyoptica as po
    >>>
    >>> npix = 101
    >>> pixel_scale = 0.5 * u.m
    >>> x, y = po.utils.mesh_grid(npix, pixel_scale)
    >>> r_max = .5 * npix * pixel_scale
    >>> r, theta = po.utils.cart2pol(x, y)
    >>> r = r / r_max
    >>> m, n =  1, 3
    >>> z = po.zernikes.zernike(m, n, r, theta)

    **References**

    [1] Vasudevan Lakshminarayanan and Andre Fleck (2011) -
    *Zernike polynomials: a guide*, Journal of Modern Optics

    [2] Robert J. Noll (1976) -
    "*Zernike polynomials and atmospheric turbulence*," J. Opt. Soc. Am. 66, 207-211

    """
    if n < 0:
        raise ValueError(f"Radial order n = {n} < 0! Must be n > 0.")
    if m > n:
        raise ValueError(f"Radial order n > m angular frequency: {n} > {m}.")
    if (n - m) % 2 != 0:
        raise ValueError(f"Radial order n - m angular frequency is not even: "
                         f"{n} - {m} = {n - m}")
    if isinstance(rho, u.Quantity):
        rho = rho.value
    if isinstance(theta, u.Quantity):
        theta = theta.value
    flat_disk = np.ones_like(rho)
    flat_disk[rho > 1] = fill_value
    radial_function = R(m, n, rho) * flat_disk
    if m >= 0:
        output = radial_function * np.cos(m * theta)
    else:
        output = radial_function * np.sin(-m * theta)

    if normalize:
        output *= norm_coefficient(m, n)

    return output


def R(m, n, rho):
    r"""The radial function described by:

    :math: `R_{n}^{m}(r)=\sum_{l=0}^{(n-m) / 2} \frac{(-1)^{l}(n-l) !}{l !\left[\frac{1}{2}(n+m)-l\right] !\left[\frac{1}{2}(n-m)-l\right] !} r^{n-2 l}`


    The definition was taken from [1], however, good description of zernikes
    can be found in almost all textbooks.

    :param m: zernike m-degree, angular frequency
    :type m: int
    :param n: zernike n-degree, radial order
    :type n: int
    :param rho: r coordinates of the plane,
    :type rho: numpy.array
    :return: calculated radial function
    :rtype: numpy.array

    **Example**

    >>> import astropy.units as u
    >>> import pyoptica as po
    >>>
    >>> npix = 101
    >>> pixel_scale = 0.5 * u.m
    >>> x, y = po.utils.mesh_grid(npix, pixel_scale)
    >>> r_max = .5 * npix * pixel_scale
    >>> r, _ = po.utils.cart2pol(x, y)
    >>> r = r / r_max
    >>> m, n =  1, 3
    >>> radial_poly = po.zernikes.R(m, n, r)

    **References**

    [1] Vasudevan Lakshminarayanan and Andre Fleck (2011) -
    *Zernike polynomials: a guide*, Journal of Modern Optics

    """

    m = abs(m)  # For Zm and Z-m, Rm is the same
    range_stop = (n - m) // 2 + 1
    output = np.zeros_like(rho)
    for l in range(range_stop):
        numerator = (-1.) ** l * factorial(n - l)
        denominator = factorial(l)
        denominator *= factorial((n + m) / 2. - l)
        denominator *= factorial((n - m) / 2. - l)
        output += numerator / denominator * rho ** (n - 2. * l)
    return output


def norm_coefficient(m, n):
    """Calculate normalizaiton coeficient of each zernikes; Rn+-m(1) = 1 for
    all n, m. THhe folowing euqtion is used (eq. 4 in [1]):

    :math:`N_{n}^{m}=\left(\frac{2(n+1)}{1+\delta_{m 0}}\right)^{1 / 2}`

    :param m: zernike m-degree, angular frequency
    :type m: int
    :param n: zernike n-degree, radial order
    :type n: int
    :return: calculate normalization coefficient
    :rtype: float

    **Example**

    >>> import pyoptica as po
    >>>
    >>> m, n = 1, 3
    >>> po.zernikes.norm_coefficient(m, n)
    >>> 2.8284271247461903

    **References**

    [1] Vasudevan Lakshminarayanan and Andre Fleck (2011) -
    *Zernike polynomials: a guide*, Journal of Modern Optics

    """
    numerator = 2 * (n + 1)
    denominator = 2 if m == 0 else 1
    norm = (numerator / denominator) ** 0.5
    return norm


def mn_to_j(m, n):
    """Conversion of m, n indices to OSA index j [1]:
        j = (n * (n + 2) + m) // 2

    :param m: zernike m-degree, angular frequency
    :type m: int
    :param n: zernike n-degree, radial order
    :type n: int
    :return: j-index
    :rtype: int

    **Example**

    >>> import pyoptica as po
    >>>
    >>> m, n = 1, 3
    >>> j = po.zernikes.mn_to_j(m, n)
    >>> 8

    **References**

    [1] Vasudevan Lakshminarayanan and Andre Fleck (2011) -
    *Zernike polynomials: a guide*, Journal of Modern Optics

    """
    j = (n * (n + 2) + m) // 2
    logger.debug(f"Converted (m={m}, n={n}) -> j={j}.")
    return j


def j_to_mn(j):
    """Conversion of j index to m, n [1]:
        n = roundup((-3 + sqrt(9 +8j))/2)
        m = 2j - n(n+2)
    :param j: j index (OSA convention)
    :type j int
    :return: m, n - angular frequency and radial order
    :rtype: Tuple(int, int)

    **Example**

    >>> import pyoptica as po
    >>>
    >>> j = 8
    >>> m, n = po.j_to_mn(j)
    >>> 1, 3

    **References**

    [1] Vasudevan Lakshminarayanan and Andre Fleck (2011) -
    *Zernike polynomials: a guide*, Journal of Modern Optics

    """
    n = ceil((-3 + sqrt((9 + 8 * j))) / 2)
    m = 2 * j - n * (n + 2)
    logger.debug(f"Converted j={j} -> (m={m}, n={n}).")
    return m, n


def construct_wavefront_from_js(
        js_coefs_dict, rho, theta, normalize=True, fill_value=0):
    """Sums up zernikes with given coefs to form the final wavefront:
    wf = sum(coef_j * zernike_j(j, rho, theta) for j, coef_j in js_coefs_dict.items())

    :param js_coefs_dict: a dict with corresponding coefficients
    :type js_coefs_dict: dict
    :param rho: r coordinates of the plane,
    :type rho: numpy.array
    :param theta: calculated radial function
    :type theta: numpy.array
    :param normalize: should wavefront be normalized?
    :type normalize: bool
    :return: fitted wf (summed zernikes)
    :rtype: numpy.array

    **Example**

    Let's import all necessary packages
    >>> import astropy.units as u
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> import pyoptica as po
    >>> # Now we construct array which will be used for fitting
    >>> npix = 101
    >>> pixel_scale = 0.5 * u.m
    >>> x, y = po.utils.mesh_grid(npix, pixel_scale)
    >>> r_max = .5 * npix * pixel_scale
    >>> r, theta = po.utils.cart2pol(x, y)
    >>> r = r / r_max
    >>> r, theta = r.value, theta.value
    >>> # Now it is time to construct a wf (sum up zernikes):
    >>> coefs = [0.1] * 12
    >>> js = list(range(12))
    >>> js_coefs_dict = dict(zip(js, coefs))
    >>> wf = po.zernikes.construct_wavefront_from_js(js_coefs_dict,r, theta)

    """
    wf = np.zeros(rho.shape)
    for j, w in js_coefs_dict.items():
        wf += w * zernike_j(j, rho, theta, normalize, fill_value=fill_value)
    return wf


def fit_zernikes_j(
        wf, js, rho, theta, normalize=True, cache=True, method='COBYLA',
        **kwargs):
    """Fits zernikes to the given wf -- for given `js` finds corresponding
    coefficients `c_j` that when summed form fitted_wf:
        fitted_wf = sum((c_j * zernike_j(j, rho, theta, normalize))
    for which the difference (more specifically: l2-norm of the difference) is
    minimized.

    For the minimization routine `scipy.optimize.minimize` is used. For details
    please go to: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html

    :param wf: a wavefront to be fitted
    :type wf: numpy.array
    :param js: a list of zernikes to be fitted
    :type js: iterable
    :param rho: r coordinates of the plane,
    :type rho: numpy.array
    :param theta: calculated radial function
    :type theta: numpy.array
    :param normalize: should wavefront be normalized?
    :type normalize: bool
    :param cache: should zernikes be cached?
    :type cache: bool
    :param method: method of `scipy.optimize.minimize`
    :type method: str
    :param kwargs: remaining arguments for `scipy.optimize.minimize`
    :return: (found coefficients, minimization results)
    :rtype: Tuple(dict, OptimizeResult)

    **Example**

    Let's import all necessary packages
    >>> import astropy.units as u
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> # And from pyoptica
    >>> import pyoptica as po
    >>> # Now we construct array which will be used for fitting
    >>> npix = 101
    >>> pixel_scale = 0.5 * u.m
    >>> x, y = po.utils.mesh_grid(npix, pixel_scale)
    >>> r_max = .5 * npix * pixel_scale
    >>> r, theta = po.utils.cart2pol(x, y)
    >>> r = r / r_max
    >>> r, theta = r.value, theta.value
    >>> # Now it is time to construct a wf (sum up zernikes):
    >>> coefs = [0.1] * 12
    >>> js = list(range(12))
    >>> js_coefs_dict = dict(zip(js, coefs))
    >>> wf = po.zernikes.construct_wavefront_from_js(js_coefs_dict, r, theta)
    >>> fit, res = po.zernikes.fit_zernikes_j(wf, js, r, theta, cache=True)
    >>> fit
        {0: 0.09999999466400215,
         1: 0.09999998903721308,
         2: 0.09999999890069368,
         3: 0.09999999483945994,
         4: 0.09999999212142557,
         5: 0.0999999933147726,
         6: 0.0999999933135079,
         7: 0.09999999519388976,
         8: 0.09999999575002586,
         9: 0.0999999900420963,
         10: 0.09999999224797648,
         11: 0.0999999967091342}

    """
    if np.isnan(wf).any():
        raise ValueError(
            'Nan values are not accepted in the fitting routine. Please use'
            ' a different `fill_value` while constructing input wf!'
        )
    initial_coefs = np.zeros(len(js))
    if cache:
        cached_zernikes = [zernike_j(j, rho, theta, normalize) for j in js]
        res = minimize(
            _l2_norm_of_aberration_wavefront_cache,
            x0=initial_coefs,
            args=(wf, cached_zernikes),
            method=method,
            **kwargs)
    else:
        res = minimize(
            _l2_norm_of_aberration_wavefront,
            x0=initial_coefs,
            args=(js, wf, rho, theta, normalize),
            method=method,
            **kwargs)
    return dict(zip(js, res.x)), res


def fit_zernikes_j_lstsq(wf, js, rho, theta, normalize=True):
    """ Fits zernikes using the least squares method:

            Zi * ci = wf
    Where Zi and ci represent vectors with zernikes and coefficients
    respectively.

    This is the recommended method to fit a wavefront.

    :param wf: a wavefront to be fitted
    :type wf: numpy.array
    :param js: a list of zernikes to be fitted
    :type js: iterable
    :param rho: r coordinates of the plane,
    :type rho: numpy.array
    :param theta: calculated radial function
    :type theta: numpy.array
    :param normalize: should wavefront be normalized?
    :type normalize: bool
    :return: fitted coeffs in a dict, (residuals, rank, singular_values)
    :rtype: Tuple(dict, tuple)

        **Example**

    Let's import all necessary packages
    >>> import astropy.units as u
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> # And from pyoptica
    >>> import pyoptica as po
    >>> # Now we construct array which will be used for fitting
    >>> npix = 101
    >>> pixel_scale = 0.5 * u.m
    >>> x, y = po.utils.mesh_grid(npix, pixel_scale)
    >>> r_max = .5 * npix * pixel_scale
    >>> r, theta = po.utils.cart2pol(x, y)
    >>> r = r / r_max
    >>> r, theta = r.value, theta.value
    >>> # Now it is time to construct a wf (sum up zernikes):
    >>> coefs = [0.1] * 12
    >>> js = list(range(12))
    >>> js_coefs_dict = dict(zip(js, coefs))
    >>> wf = po.zernikes.construct_wavefront_from_js(js_coefs_dict, r, theta)
    >>> fit, res = po.zernikes.fit_zernikes_j_lstsq(wf, js, r, theta, cache=True)
    >>> fit
        {0: 0.10000000000000002,
         1: 0.10000000000000016,
         2: 0.10000000000000019,
         3: 0.1,
         4: 0.09999999999999987,
         5: 0.10000000000000009,
         6: 0.09999999999999998,
         7: 0.10000000000000002,
         8: 0.10000000000000009,
         9: 0.10000000000000003,
         10: 0.1,
         11: 0.10000000000000003}

    """

    # It is not possible to work on 2D arrays... Therefore the need to be
    # flattened. That doesn't matter though -- it is just a way of data
    # representation.
    zernikes = np.array(
        [zernike_j(j, rho, theta, normalize).flatten() for j in js]
    ).T
    coefs, *res = np.linalg.lstsq(zernikes, wf.flatten(), rcond=None)
    return dict(zip(js, coefs)), res


def _l2_norm_of_aberration_wavefront_cache(coefs, wf, cached_zernikes):
    """Calculates l2-norm between wavefront and a sum of zernikes in
    `cached_zernikes` and corresponding coefficients `coefs`.

    To be used in an optimization routine.

    :param coefs: a list of coefficients corresponding to zernikes
    :type coefs: iterable
    :param wf: a wavefront with which l2-norm is calculated
    :type wf: numpy.array
    :param cached_zernikes: a list of precalculated zernikes
    :type cached_zernikes: iterable
    :return: l2-norm of the difference between the two wavefronts
    :type: float

    """
    constructed_wf = np.zeros_like(wf)
    for z_dist, w in zip(cached_zernikes, coefs):
        constructed_wf += w * z_dist
    norm = np.linalg.norm(wf - constructed_wf)
    logger.debug(f"L2-norm = {norm}")
    return norm


def _l2_norm_of_aberration_wavefront(
        coefs, js, wavefront, rho, theta, normalize):
    """
    Calculates l2-norm between wavefront and a sum of zernikes of indices `js`
    and corresponding coefficients `coefs`.

    To be used in an optimization routine.

    :param coefs: a list of coefficients corresponding to zernikes
    :type coefs: iterable
    :param js: a list of zernikes
    :type js: iterable
    :param wavefront: a wavefront with which l2-norm is calculated
    :type wavefront: numpy.array
    :param rho: r coordinates of the plane,
    :type rho: numpy.array
    :param theta: calculated radial function
    :type theta: numpy.array
    :param normalize: should wavefront be normalized?
    :type normalize: bool
    :return: l2-norm of the difference between the two wavefronts
    :type: float

    """
    js_coefs_dict = dict(zip(js, coefs))
    sum_wf = construct_wavefront_from_js(js_coefs_dict, rho, theta, normalize)
    norm = np.linalg.norm(wavefront - sum_wf)
    logger.debug(f"L2-norm = {norm}")
    return norm
