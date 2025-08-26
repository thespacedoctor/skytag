#!/usr/bin/env python
# encoding: utf-8
"""
*Return the probability contour a given location in the sky resides within in a heaplix skymap*

:Author:
    David Young

:Date Created:
    April 28, 2023
"""
from fundamentals import tools
from builtins import object
import sys
import os
os.environ['TERM'] = 'vt100'


def prob_at_location(
        ra,
        dec,
        mapPath,
        mjd=False,
        log=False,
        distance=False,
        probdensity=False):
    """*Return the probability contour a given sky-location resides within in a heaplix skymap*

    **Key Arguments:**
        - ``ra`` -- right ascension in decimal degrees (float or list)
        - ``dec`` -- declination in decimal degrees (float or list)
        - ``mapPath`` -- path the the HealPix map
        - ``mjd`` -- MJD of transient event (e.g. discovery date). If supplied, a time-delta from the map event is returned (float or list)
        - ``log`` -- logger
        - ``distance`` -- return also a distance (if present). Default False
        - ``probdensity`` -- return also the probability density. Default False

    **Return:**
        - ``probs`` -- a list of probabilities the same length as the input RA and Dec lists. One probability per location.
        - ``timeDeltas`` -- a list of time-deltas (days) the same length as the input RA, Dec and MJD lists. One delta per input MJD giving the time since the map event. Only returned if MJD is supplied.
        - ``distance`` -- a list of location specific distances and distance-sigmas. A list of tuples. Only returned if `distance=True`.
        - ``probdensity`` -- a list of location specific probability densities. Only returned if `probdensity=True`.

    You can pass a single coordinate to return the probability contour that location lies within on the skymap:

    ```python
    from skytag.commonutils import prob_at_location
    prob = prob_at_location(
        ra=10.343234,
        dec=14.345532,
        mapPath="/path/to/bayestar.multiorder.fits"
    )
    ```

    Or a list of coordinates:

    ```python
    from skytag.commonutils import prob_at_location
    prob = prob_at_location(
        log=log,
        ra=[10.343234, 170.343532],
        dec=[14.345532, -40.532255],
        mapPath=pathToOutputDir + "/bayestar.multiorder.fits"
    )
    ```

    You can also pass in a list of MJDs to also return a list of time-deltas:

    ```
    from skytag.commonutils import prob_at_location
    prob, deltas = prob_at_location(
        log=log,
        ra=[10.343234, 170.343532],
        dec=[14.345532, -40.532255],
        mjd=[60034.257381, 60063.257381],
        mapPath=pathToOutputDir + "/bayestar.multiorder.fits"
    )
    ```

    Here probs = `[100.0, 74.55]` and deltas = `[-28.11018, 0.88982]`. Deltas are in days, with negative deltas occurring before the map event.

    You can also request distance estimates at the locations:

    ```
    from skytag.commonutils import prob_at_location
    prob, deltas, distance = prob_at_location(
        log=log,
        ra=[10.343234, 170.343532],
        dec=[14.345532, -40.532255],
        mjd=[60034.257381, 60063.257381],
        mapPath=pathToOutputDir + "/bayestar.multiorder.fits",
        distance=True
    )
    ```

    The distances are returned as a list of tuples (distance in MPC, distance sigma in MPC)

    You can also request probability density (per steradian) at the locations,

    ```
    from skytag.commonutils import prob_at_location
    prob, deltas, distance, probdensity = prob_at_location(
        log=log,
        ra=[10.343234, 170.343532],
        dec=[14.345532, -40.532255],
        mjd=[60034.257381, 60063.257381],
        mapPath=pathToOutputDir + "/bayestar.multiorder.fits",
        distance=True,
        probdensity=True
    )
    ```

    """

    if not log:
        from fundamentals.logs import emptyLogger
        log = emptyLogger()

    log.debug('starting the ``prob_at_location`` function')

    from astropy.table import Table
    import astropy_healpix as ah
    import numpy as np
    from astropy import units as u
    import pandas as pd


    

    # CONVERT HEALPIX MAP TO DATAFRAME
    skymap = Table.read(mapPath)
    if "DISTMEAN" in skymap.meta:
        rmax = skymap.meta["DISTMEAN"] + 7*skymap.meta["DISTSTD"]   
    else:
        rmax = 500
    mjdObs = skymap.meta["MJD-OBS"]
    skymap.sort('PROBDENSITY', reverse=True)
    tableData = skymap.to_pandas()

    # FIND LEVEL AND NSIDE PIXEL INDEX FOR EACH MULTI-RES PIXEL
    tableData['LEVEL'], tableData['IPIX'] = ah.uniq_to_level_ipix(tableData['UNIQ'])
    tableData['NSIDE'] = ah.level_to_nside(tableData['LEVEL'])
    # DETERMINE THE PIXEL AREA AND PROB OF EACH PIXEL
    tableData['AREA'] = ah.nside_to_pixel_area(tableData['NSIDE']).to_value(u.steradian)
    tableData['PROB'] = tableData['AREA'] * tableData["PROBDENSITY"]
    tableData['CUMPROB'] = np.cumsum(tableData['PROB'])

    # DETERMINE THE INDEX OF MULTI-RES PIX AT HIGHEST HEALPIX RESOLUTION
    max_level = 29
    max_nside = ah.level_to_nside(max_level)
    tableData['INDEX29'] = tableData['IPIX'] * (2**(max_level - tableData['LEVEL']))**2

    if not isinstance(ra, list) and not isinstance(ra, np.ndarray):
        ra = [ra]
    if not isinstance(dec, list) and not isinstance(dec, np.ndarray):
        dec = [dec]

    ra = np.array(ra) * u.deg
    dec = np.array(dec) * u.deg

    # TEST FOR EQUAL LEN
    if ra.shape != dec.shape:
        raise AttributeError("RA and Dec lists must be of equal length")

    # DETERMINE THE HIGH-RES PIXEL LOCATION FOR EACH RA AND DEC
    match_ipix = ah.lonlat_to_healpix(ra, dec, max_nside, order='nested')

    # RETURNS THE INDICES THAT WOULD SORT THIS ARRAY
    sorter = np.argsort(tableData['INDEX29'])
    # FIND INDICES WHERE ELEMENTS SHOULD BE INSERTED TO MAINTAIN ORDER -- CLOSET MATCH TO THE RIGHT
    matchedIndices = sorter[np.searchsorted(tableData['INDEX29'].values, match_ipix, side='right', sorter=sorter) - 1]

    # MERGE TABLES
    results = tableData.iloc[matchedIndices]

    resultCount = 1
    resultsToReturn = [np.around(results['CUMPROB'].values * 100., 2).tolist()]

    if mjd:
        resultCount += 1
        if not isinstance(mjd, list) and not isinstance(mjd, np.ndarray):
            mjd = [mjd]
        mjd = np.array(mjd)
        # TEST FOR EQUAL LEN
        if ra.shape != mjd.shape:
            raise AttributeError("MJD list must be of equal length to RA and Dec lists")
        mjdDelta = mjd - mjdObs
        resultsToReturn.append(np.around(mjdDelta, 5).tolist())

    if distance:
        resultCount += 1
        if 'DISTMU' in results.columns:
            dist = results['DISTMU'].values
            distsigma = results['DISTSIGMA'].values
            distnorm = results['DISTNORM'].values
            mean, std = ansatz_to_normal(distmu=dist, distsigma=distsigma, distnorm=distnorm, rmax=rmax, num=10000)
            distTuples = []
            distTuples[:] = [(d, s) for d, s in zip(np.round(mean, 2), np.round(std, 2))]
            resultsToReturn.append(distTuples)
        else:
            distTuples = []
            distTuples[:] = [(None, None) for p in resultsToReturn[0]]

            resultsToReturn.append(distTuples)

    if probdensity:
        resultCount += 1
        prob = np.around(results['PROBDENSITY'].values, 5).tolist()
        resultsToReturn.append(prob)

    log.debug('completed the ``prob_at_location`` function')
    if resultCount == 1:
        return resultsToReturn
    else:
        return resultsToReturn[0:resultCount]



def ansatz_to_normal(distmu, distsigma, distnorm, rmin=0, rmax=500, num=1000):
    """
    Approximate an Ansatz (r^2-weighted Gaussian) distance distribution as a normal distribution.

    Parameters
    ----------
    distmu : float or array-like
        Mean of the underlying Gaussian (DISTMU).
    distsigma : float or array-like
        Stddev of the underlying Gaussian (DISTSIGMA).
    distnorm : float or array-like
        Normalization factor (DISTNORM).
    rmin : float
        Minimum distance (default: 0).
    rmax : float
        Maximum distance (default: 500).
    num : int
        Number of points in the distance grid.

    Returns
    -------
    mean : float or np.ndarray
        Mean of the Ansatz distribution.
    std : float or np.ndarray
        Stddev of the Ansatz distribution.
    """
    import numpy as np
    from scipy.stats import norm

    r = np.linspace(rmin, rmax, num)
    distmu = np.atleast_1d(distmu)
    distsigma = np.atleast_1d(distsigma)
    distnorm = np.atleast_1d(distnorm)

    means = []
    stds = []

    for mu, sigma, normfac in zip(distmu, distsigma, distnorm):
        pdf = r**2 * normfac * norm.pdf(r, mu, sigma)
        pdf /= np.trapezoid(pdf, r)
        mean = np.trapezoid(r * pdf, r)
        std = np.sqrt(np.trapezoid((r - mean)**2 * pdf, r))
        means.append(mean)
        stds.append(std)

    means = np.array(means)
    stds = np.array(stds)

    return means, stds
