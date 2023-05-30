

```bash 
    
    Documentation for skytag can be found here: http://skytag.readthedocs.org
    
    Usage:
        skytag init
        skytag [-d] <ra> <dec> <mapPath>
        skytag [-d] <ra> <dec> <mjd> <mapPath>
    
    Options:
        init                                   setup the skytag settings file for the first time
        <ra>                                   sky location right-ascension (decimal degrees or sexegesimal)
        <dec>                                  sky location declination (decimal degrees or sexegesimal)
        <mjd>                                  a transient event MJD. If supplied, a time delta from the map event is returned alongside probability.
        <mapPath>                              path to a HealPix skymap
        -d, --distance                         also return a distance (and error) at the sky location
        -h, --help                             show this help message
        -v, --version                          show version
        -s, --settings <pathToSettingsFile>    the settings file
    

```
