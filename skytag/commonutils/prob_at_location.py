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
        log=False):
    """*Return the probability contour a given sky-location resides within in a heaplix skymap*

    **Key Arguments:**
        - ``ra`` -- right ascension in decimal degrees (float or list)
        - ``dec`` -- declination in decimal degrees (float or list)
        - ``mapPath`` -- path the the HealPix map
        - ``mjd`` -- MJD of transient event (e.g. discovery date). If supplied, a time-delta from the map event is returned (float or list)
        - ``log`` -- logger

    **Return:**
        - ``probs`` -- a list of probabilities the same length as the input RA and Dec lists. One probability per location.
        - ``timeDeltas`` -- a list of time-deltas (days) the same length as the input RA, Dec and MJD lists. One delta per input MJD giving the time since the map event. Only returned if MJD is supplied.

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

    Finally, you can also pass in a list of MJDs to also return a list of time-deltas:

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

    if mjd:
        if not isinstance(mjd, list) and not isinstance(mjd, np.ndarray):
            mjd = [mjd]
        mjd = np.array(mjd)
        # TEST FOR EQUAL LEN
        if ra.shape != mjd.shape:
            raise AttributeError("MJD list must be of equal length to RA and Dec lists")
        mjdDelta = mjd - mjdObs
        log.debug('completed the ``prob_at_location`` function')
        return np.around(results['CUMPROB'].values * 100., 2).tolist(), np.around(mjdDelta, 5).tolist()

    log.debug('completed the ``prob_at_location`` function')
    return np.around(results['CUMPROB'].values * 100., 2).tolist()
