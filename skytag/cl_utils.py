#!/usr/bin/env python
# encoding: utf-8
"""
Documentation for skytag can be found here: http://skytag.readthedocs.org

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
"""
from subprocess import Popen, PIPE, STDOUT
from fundamentals import tools, times
from docopt import docopt
import pickle
import glob
import readline
import sys
import os
os.environ['TERM'] = 'vt100'


def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when `cl_utils.py` is run as a single script from the cl, or when installed as a cl command*
    """
    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="WARNING",
        options_first=True,
        projectName="skytag",
        defaultSettingsFile=True
    )
    arguments, settings, log, dbConn = su.setup()

    # tab completion for raw_input
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tab_complete)

    # UNPACK REMAINING CL ARGUMENTS USING `EXEC` TO SETUP THE VARIABLE NAMES
    # AUTOMATICALLY
    a = {}
    for arg, val in list(arguments.items()):
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        a[varname] = val
        if arg == "--dbConn":
            dbConn = val
            a["dbConn"] = val
        log.debug('%s = %s' % (varname, val,))

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cl_utils.py AT %s' %
        (startTime,))

    if a["init"]:
        from os.path import expanduser
        home = expanduser("~")
        filepath = home + "/.config/skytag/skytag.yaml"
        try:
            cmd = """open %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        try:
            cmd = """start %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        return

    if a["mjd"]:
        from skytag.commonutils import prob_at_location
        prob, deltas = prob_at_location(
            log=log,
            ra=float(a["ra"]),
            dec=float(a["dec"]),
            mjd=float(a["mjd"]),
            mapPath=a["mapPath"]
        )

        if deltas[0] < 0.:
            preposition = "before"
        else:
            preposition = "after"

        print(f"This transient is found in the {prob[0]}% credibility region, and occurred {deltas[0]} days {preposition} the map event.")

    else:
        # CALL FUNCTIONS/OBJECTS
        from skytag.commonutils import prob_at_location
        prob = prob_at_location(
            log=log,
            ra=float(a["ra"]),
            dec=float(a["dec"]),
            mapPath=a["mapPath"]
        )[0]

        print(f"This location is found in the {prob}% credibility region of the map.")

    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return


if __name__ == '__main__':
    main()
