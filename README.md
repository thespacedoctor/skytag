# skytag

[![](https://zenodo.org/badge/DOI/10.5281/zenodo.7977905.svg)](https://zenodo.org/doi/10.5281/zenodo.7977905) 

<!-- INFO BADGES -->  

[![](https://img.shields.io/pypi/pyversions/skytag)](https://pypi.org/project/skytag/)
[![](https://img.shields.io/pypi/v/skytag)](https://pypi.org/project/skytag/)
[![](https://img.shields.io/conda/vn/conda-forge/skytag)](https://anaconda.org/conda-forge/skytag)
[![](https://pepy.tech/badge/skytag)](https://pepy.tech/project/skytag)
[![](https://img.shields.io/github/license/thespacedoctor/skytag)](https://github.com/thespacedoctor/skytag)

<!-- STATUS BADGES -->  

[![](https://soxs-eso-data.org/ci/buildStatus/icon?job=skytag%2Fmain&subject=build%20main)](https://soxs-eso-data.org/ci/blue/organizations/jenkins/skytag/activity?branch=main)
[![](https://soxs-eso-data.org/ci/buildStatus/icon?job=skytag%2Fdevelop&subject=build%20dev)](https://soxs-eso-data.org/ci/blue/organizations/jenkins/skytag/activity?branch=develop)
[![](https://cdn.jsdelivr.net/gh/thespacedoctor/skytag@main/coverage.svg)](https://raw.githack.com/thespacedoctor/skytag/main/htmlcov/index.html)
[![](https://readthedocs.org/projects/skytag/badge/?version=main)](https://skytag.readthedocs.io/en/main/)
[![](https://img.shields.io/github/issues/thespacedoctor/skytag/type:%20bug?label=bug%20issues)](https://github.com/thespacedoctor/skytag/issues?q=is%3Aissue+is%3Aopen+label%3A%22type%3A+bug%22+) 

*Annotate transient sources or galaxies with the percentage credibility region they reside within on a given HealPix sky map.*

Documentation for skytag is hosted by [Read the Docs](https://skytag.readthedocs.io/en/main/) ([development version](https://skytag.readthedocs.io/en/develop/) and [main version](https://skytag.readthedocs.io/en/main/)). The code lives on [github](https://github.com/thespacedoctor/skytag). Please report any issues you find [here](https://github.com/thespacedoctor/skytag/issues). If you want to contribute, [pull requests](https://github.com/thespacedoctor/skytag/pulls) are welcomed! 
true

## Features

- A command-line tool to report the credibility region a sky-location is found within on a HealPix skymap.  
- Providing a MJD will also return the time since the map event.  
- A python interface to provide the same functionality reported above, but can handle large lists of sky-locations or transient events.
- works well in conjunction with [gocart](https://github.com/thespacedoctor/gocart).

## Installation

The easiest way to install skytag is to use `conda`:

``` bash
conda create -n skytag python=3.11 pip skytag -c conda-forge
conda activate skytag
```

To upgrade to the latest version of skytag use the command:

``` bash
conda upgrade skytag -c conda-forge
```

It is also possible to install via pip if required:

``` bash
pip install skytag
```

To check installation was successful run `skytag -v`. This should return the version number of the install.

## Command-Line 

Here is the command-line usage:

```bash 
Usage:
    skytag <ra> <dec> <mapPath>
    skytag <ra> <dec> <mjd> <mapPath>
```

If you need an example skymap, [download one from here](https://github.com/thespacedoctor/skytag/raw/main/skytag/commonutils/tests/input/bayestar.multiorder.fits).

For example, to find the probability of the location RA=170.343532, Dec=-40.532255 then run:

```bash 
skytag 170.343532 -40.532255 bayestar.multiorder.fits
```

This returns:

> This location is found in the 74.55 credibility region of the map.

If you also supply an MJD:

```bash 
skytag 170.343532 -40.532255 60065.2232 bayestar.multiorder.fits
```

We get:

> This transient is found in the 74.55 credibility region, and occurred 2.85564 days after the map event.

Finally, we can request the localised event distance for this specific sky-position be returned:

```bash 
skytag -d 170.343532 -40.532255 bayestar.multiorder.fits
```

> This transient is found in the 74.55% credibility region. At this sky-position the map event is localised to a distance of 75.03 (±19.72) Mpc.

## Python API

To use skytag in your own Python code, [see here](_autosummary/skytag.commonutils.prob_at_location.html#skytag.commonutils.prob_at_location).

## gocart

skyTag works very well in conjunction with [gocart](https://github.com/thespacedoctor/gocart), a tool to consume GCN Kafka alert streams and convert HealPix skymaps.

## How to cite skytag

If you use `skytag` in your work, please cite using the following BibTeX entry: 

```bibtex
@software{Young_skytag,
    author = {Young, David R.},
    doi = {10.5281/zenodo.7977905},
    license = {GPL-3.0-only},
    title = {{skytag. Annotate transient sources or galaxies with the percentage credibility region they reside within on a given HealPix sky map.}},
    url = {https://zenodo.org/doi/10.5281/zenodo.7977905}
}
```

