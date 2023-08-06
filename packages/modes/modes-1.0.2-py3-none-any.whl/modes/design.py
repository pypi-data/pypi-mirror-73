import numpy as np


def directional_coupler_lc(wavelength_nm, n_eff_1, n_eff_2):
    """
    Calculates the coherence length (100% power transfer) of a
    directional coupler.

    Args:
        wavelength_nm (float): The wavelength in [nm] the
            directional coupler should operate at.
        n_eff_1 (float): n_eff of the fundamental (even)
            supermode of the directional coupler.
        n_eff_2 (float): n_eff of the first-order (odd)
            supermode of the directional coupler.

    Returns:
        float: The length [um] the directional coupler
        needs to be to achieve 100% power transfer.

    """
    wavelength_m = wavelength_nm * 1.0e-9
    dn_eff = (n_eff_1 - n_eff_2).real
    lc_m = wavelength_m / (2.0 * dn_eff)
    lc_um = lc_m * 1.0e6
    return lc_um


def grating_coupler_period(
    wavelength, n_eff, n_clad, incidence_angle_deg, diffration_order=1
):
    """
    Calculate the period needed for a grating coupler.

    Args:
        wavelength (float): The target wavelength for the
            grating coupler.
        n_eff (float): The effective index of the mode
            of a waveguide with the width of the grating
            coupler.
        n_clad (float): The refractive index of the cladding.
        incidence_angle_deg (float): The incidence angle
            the grating coupler should operate at [degrees].
        diffration_order (int): The grating order the coupler
            should work at.  Default is 1st order (1).

    Returns:
        float: The period needed for the grating coupler
        in the same units as the wavelength was given at.
    """
    k0 = 2.0 * np.pi / wavelength
    beta = n_eff.real * k0
    n_inc = n_clad

    grating_period = (2.0 * np.pi * diffration_order) / (
        beta - k0 * n_inc * np.sin(np.radians(incidence_angle_deg))
    )

    return grating_period


def loss(n, wavelength):
    kappa = n.imag
    alpha = (
        4.34 * 4 * np.pi * np.abs(kappa) / wavelength
    )  # 4.34 = 10*np.log10(np.e) -> [dB/m] = 4.34 [/m]
    return alpha  # [db/um] if working in [um]


def qpm_wavenumber(
    pmp_n, pmp_l, sig_n, sig_l, idl_n, idl_l, period_qpm, type="forward"
):
    pi2 = np.pi * 2

    k_pmp = pmp_n * pi2 / pmp_l
    k_sig = sig_n * pi2 / sig_l
    k_idl = idl_n * pi2 / idl_l
    k_qpm = pi2 / period_qpm

    if type == "forward":
        sgn_1 = 1
        sgn_2 = 1
    elif type == "forward_backward":
        sgn_1 = 1
        sgn_2 = -1
    elif type == "backward":
        sgn_1 = -1
        sgn_2 = -1

    k_mismatch = k_idl * sgn_1 + k_sig * sgn_2 + k_qpm - k_pmp
    return k_mismatch


def qpm_period(pmp_n, pmp_l, sig_n, sig_l, idl_n, idl_l, type="forward"):
    pi2 = np.pi * 2

    k_pmp = pmp_n * pi2 / pmp_l
    k_sig = sig_n * pi2 / sig_l
    k_idl = idl_n * pi2 / idl_l

    if type == "forward":
        sgn_1 = 1
        sgn_2 = 1
    elif type == "forward_backward":
        sgn_1 = 1
        sgn_2 = -1
    elif type == "backward":
        sgn_1 = -1
        sgn_2 = -1

    k_qpm = k_pmp - k_idl * sgn_1 - k_sig * sgn_2
    l_qpm = pi2 / k_qpm
    return l_qpm
