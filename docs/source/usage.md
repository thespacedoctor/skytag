

```bash 
Usage:
    skytag init
    skytag <ra> <dec> <mapPath>
    skytag <ra> <dec> <mjd> <mapPath>

Options:
    init                                   setup the skytag settings file for the first time
    <ra>                                   sky location right-ascension (decimal degrees or sexegesimal)
    <dec>                                  sky location declination (decimal degrees or sexegesimal)
    <mjd>                                  a transient event MJD. If supplied, a time delta from the map event is returned alongside probability.
    <mapPath>                              path to a HealPix skymap
    -h, --help                             show this help message
    -v, --version                          show version
    -s, --settings <pathToSettingsFile>    the settings file
```
