import numpy as np
from scipy.special import erf
from scipy.integrate import quad
from reciprocalspaceship.utils.structurefactors import compute_structurefactor_multiplicity


def acentric_posterior(Iobs, SigIobs, Sigma):
    """
    Compute the mean and std deviation of the truncated normal french wilson posterior.

    Parameters
    ----------
    Iobs : array (float)
        Observed merged refl intensities
    SigIobs : array (float)
        Observed merged refl std deviation
    Sigma : array (float)
        Average intensity in the resolution bin corresponding to Iobs, SigIobs
    """
    def Phi(x):
        return 0.5*(1 + erf(x/np.sqrt(2.)))

    def phi(x):
        return np.exp(-0.5*x**2)/np.sqrt(2*np.pi)

    eps = 0.

    a = 0.
    b = 1e300
    s = SigIobs
    u = (Iobs - s**2/Sigma)
    alpha = (a-u)/(s + eps)
    beta = (b-u)/(s + eps)
    Z = Phi(beta) - Phi(alpha) + eps
    mean = u + s * (phi(alpha) - phi(beta))/Z
    variance = s**2 * (1 + (alpha*phi(alpha) - beta*phi(beta))/Z - ((phi(alpha) - phi(beta))/Z)**2 )
    return mean, np.sqrt(variance)

def centric_posterior_quad(Iobs, SigIobs, Sigma):
    """
    Use scipy quadrature integration to estimate posterior intensities with a wilson prior.

    Parameters
    ----------
    Iobs : array (float)
        Observed merged refl intensities
    SigIobs : array (float)
        Observed merged refl std deviation
    Sigma : array (float)
        Average intensity in the resolution bin corresponding to Iobs, SigIobs
    """
    lower = 0.
    u = Iobs-SigIobs**2/2/Sigma
    upper = np.abs(Iobs) + 10.*SigIobs
    limit = 1000

    Z = np.zeros(len(u))
    for i in range(len(Z)):
        Z[i] = quad(
            lambda J: np.power(J, -0.5)*np.exp(-0.5*((J-u[i])/SigIobs[i])**2),
            lower, upper[i],
        )[0]

    mean = np.zeros(len(u))
    for i in range(len(Z)):
        mean[i] = quad(
            lambda J: J*np.power(J, -0.5)*np.exp(-0.5*((J-u[i])/SigIobs[i])**2),
            lower, upper[i],
        )[0]
    mean = mean/Z

    variance = np.zeros(len(u))
    for i in range(len(Z)):
        variance[i] = quad(
            lambda J: J*J*np.power(J, -0.5)*np.exp(-0.5*((J-u[i])/SigIobs[i])**2),
            lower, upper[i],
        )[0]
    variance = variance/Z - mean**2.

    return mean,np.sqrt(variance)


def centric_posterior_trapz(Iobs, SigIobs, Sigma, npoints=10000):
    """
    Use numpy trapezoid rule integration to estimate posterior intensities with a wilson prior.

    Parameters
    ----------
    Iobs : array (float)
        Observed merged refl intensities
    SigIobs : array (float)
        Observed merged refl std deviation
    Sigma : array (float)
        Average intensity in the resolution bin corresponding to Iobs, SigIobs
    """
    eps = 1e-3
    J = np.linspace(
        eps,
        np.abs(Iobs)+5*Sigma, 
        npoints+1
    )
    u = Iobs-SigIobs**2/2/Sigma
    P = np.power(J, -0.5)*np.exp(-0.5*((J-u)/SigIobs)**2)
    Z = np.trapz(P, J, axis=0)
    mean = np.trapz(J*P/Z, J, axis=0)
    variance = np.trapz(J*J*P/Z, J, axis=0) - mean**2
    return mean,np.sqrt(variance)


def french_wilson(ds, intensity_key='Iobs', sigma_key='SigIobs', bins=50, inplace=False, fast=False):
    """
    Do french wilson scaling, return structure factors

    Parameters
    ----------
    ds : DataSet
    intensity_key : string (optional)
        Defaults to 'Iobs'
    sigma_key : string (optional)
        Defaults to 'SigIobs'
    bins : int or array
        Either an integer number of n bins. Or an array of bin edges with shape==(n, 2)
    fast : bool
        If true, use trapezoid rule integration which is faster but less accurate
    """
    if not inplace:
        ds = ds.copy()
    if 'dHKL' not in ds:
        ds.compute_dHKL(inplace=True)
    if 'CENTRIC' not in ds:
        ds.label_centrics(inplace=True)

    if fast:
        centric_posterior = centric_posterior_trapz
    else:
        centric_posterior = centric_posterior_quad

    d = ds.compute_dHKL().dHKL.to_numpy()**-2.
    if isinstance(bins, int):
        binedges = np.percentile(d, np.linspace(0, 100, bins+1))
        binedges = np.vstack((binedges[:-1], binedges[1:]))

    I, Sig = ds[intensity_key].to_numpy(), ds[sigma_key].to_numpy()

    idx = (d[:,None] > binedges[0]) & (d[:,None] < binedges[1])
    SigmaMean = (I[:,None]*idx).sum(0)/idx.sum(0)
    dmean = (d[:,None]*idx).sum(0)/idx.sum(0)

    #I prefer to do this with a kernel smoother to linear interp. 
    h = (d.max() - d.min())/len(dmean) #Bandwidth is roughly the spacing of estimates
    W = np.exp(-0.5*((d[:,None] - dmean)/h)**2)
    W = W/W.sum(1)[:,None]
    Sigma = W@SigmaMean

    multiplicity = compute_structurefactor_multiplicity(ds.get_hkls(), ds.spacegroup)
    Sigma = Sigma * multiplicity

    ds['FW' + intensity_key] = 0.
    ds['FW' + sigma_key] = 0.

    #We will get posterior centric intensities from integration
    mean, std = centric_posterior(
	ds.loc[ds.CENTRIC, intensity_key].to_numpy(),
	ds.loc[ds.CENTRIC, sigma_key].to_numpy(),
	Sigma[ds.CENTRIC]
    )

    ds.loc[ds.CENTRIC, 'FW' + intensity_key] = mean
    ds.loc[ds.CENTRIC, 'FW' + sigma_key] = std
    
    #We will get posterior acentric intensities from integration
    mean, std = acentric_posterior(
	ds.loc[~ds.CENTRIC, intensity_key].to_numpy(),
	ds.loc[~ds.CENTRIC, sigma_key].to_numpy(),
	Sigma[~ds.CENTRIC]
    )
    ds.loc[~ds.CENTRIC, 'FW' + intensity_key] = mean
    ds.loc[~ds.CENTRIC, 'FW' + sigma_key] = std

    return ds

    

import reciprocalspaceship as rs
from matplotlib import pyplot as plt
from IPython import embed

inFN =  "/home/kmdalton/xtal/ratchet_analysis/postrefinement/dhfr/reference_data/DHFR_SSRL_refine_56_final.mtz"
ds = rs.read_mtz(inFN).dropna()
ds = french_wilson(ds, 'I-obs', 'SIGI-obs', fast=True)

Iobs = np.array([
    -3.0,
    -2.0,
    -1.0,
     0.0,
     1.0,
     2.0,
     3.0,
     4.0,
     5.0,
     6.0,
    10.0,
    20.0,
    50.0,
])


SigIobs = np.ones(len(Iobs))
Sigma = 20.*np.ones(len(Iobs))
mean,stddev = acentric_posterior(Iobs, SigIobs, Sigma)

print("(a) Acentric Series")
for i,j,k in zip(Iobs, mean, stddev):
    print(f"{i:10.3f}{j:10.3f}{k:10.3f}")


SigIobs = np.ones(len(Iobs))
Sigma = 20.*np.ones(len(Iobs))
mean,stddev = centric_posterior_quad(Iobs, SigIobs, Sigma)

print("(b) Centric Series (Quadrature)")
for i,j,k in zip(Iobs, mean, stddev):
    print(f"{i:10.3f}{j:10.3f}{k:10.3f}")

SigIobs = np.ones(len(Iobs))
Sigma = 20.*np.ones(len(Iobs))
mean,stddev = centric_posterior_trapz(Iobs, SigIobs, Sigma)

print("(b) Centric Series (Trapezoid Rule)")
for i,j,k in zip(Iobs, mean, stddev):
    print(f"{i:10.3f}{j:10.3f}{k:10.3f}")

embed(colors='neutral')
