# skytag

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

*Annotate transient sources or galaxies with the percentage credibility region they reside within on a given HealPix sky map.*.

Documentation for skytag is hosted by [Read the Docs](https://skytag.readthedocs.io/en/main/) ([development version](https://skytag.readthedocs.io/en/develop/) and [main version](https://skytag.readthedocs.io/en/main/)). The code lives on [github](https://github.com/thespacedoctor/skytag). Please report any issues you find [here](https://github.com/thespacedoctor/skytag/issues). If you want to contribute, [pull requests](https://github.com/thespacedoctor/skytag/pulls) are welcomed! 
true


## Features

* 



## Installation

The easiest way to install skytag is to use `conda`:

``` bash
conda create -n skytag python=3.9 pip skytag -c conda-forge
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

Or you can clone the [github repo](https://github.com/thespacedoctor/skytag) and install from a local version of the code:

``` bash
git clone git@github.com:thespacedoctor/skytag.git
cd skytag
python setup.py install
```

To check installation was successful run `skytag -v`. This should return the version number of the install.

## Initialising skytag

Before using skytag you need to use the `init` command to generate a user settings file. Running the following creates a [yaml](https://learnxinyminutes.com/docs/yaml/) settings file in your home folder under `~/.config/skytag/skytag.yaml`:

```bash
skytag init
```

The file is initially populated with skytag's default settings which can be adjusted to your preference.

If at any point the user settings file becomes corrupted or you just want to start afresh, simply trash the `skytag.yaml` file and rerun `skytag init`.

You are now ready to start using skytag.
