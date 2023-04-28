from __future__ import print_function
from builtins import str
import os
import unittest
import shutil
import unittest
import yaml
from skytag.utKit import utKit
from fundamentals import tools
from os.path import expanduser
home = expanduser("~")


packageDirectory = utKit("").get_project_root()
settingsFile = packageDirectory + "/test_settings.yaml"
# settingsFile = home + \
#     "/git_repos/_misc_/settings/skytag/test_settings.yaml"

su = tools(
    arguments={"settingsFile": settingsFile},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName=None,
    defaultSettingsFile=False
)
arguments, settings, log, dbConn = su.setup()

# SETUP PATHS TO COMMON DIRECTORIES FOR TEST DATA
moduleDirectory = os.path.dirname(__file__)
pathToInputDir = moduleDirectory + "/input/"
pathToOutputDir = moduleDirectory + "/output/"

try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)


# xt-setup-unit-testing-files-and-folders
# xt-utkit-refresh-database

class test_prob_at_location(unittest.TestCase):

    def test_prob_only_at_location_function(self):

        from skytag.commonutils import prob_at_location
        prob = prob_at_location(
            log=log,
            ra=10.343234,
            dec=14.345532,
            mapPath=pathToOutputDir + "/bayestar.multiorder.fits"
        )
        print(prob)

    def test_prob_at_location_function(self):

        from skytag.commonutils import prob_at_location
        prob, deltas = prob_at_location(
            log=log,
            ra=10.343234,
            dec=14.345532,
            mjd=60063.212340,
            mapPath=pathToOutputDir + "/bayestar.multiorder.fits"
        )
        print(prob, deltas)

    def test_prob_at_location_function2(self):

        from skytag.commonutils import prob_at_location
        prob, deltas = prob_at_location(
            log=log,
            ra=[10.343234, 170.343532],
            dec=[14.345532, -40.532255],
            mjd=[60034.257381, 60063.257381],
            mapPath=pathToOutputDir + "/bayestar.multiorder.fits"
        )
        print(prob, deltas)

    def test_mixed_len_function_exception(self):

        from skytag.commonutils import prob_at_location
        try:
            from skytag.commonutils import prob_at_location
            this = prob_at_location(
                log=log,
                ra=[0.0, 170.],
                dec=[0.0, -40., -04.2],
                mapPath=pathToOutputDir + "/bayestar.multiorder.fits"
            )
            print(this)
            assert False
        except Exception as e:
            assert True
            print(str(e))

    def test_mixed_len_function_exception(self):

        from skytag.commonutils import prob_at_location
        try:
            from skytag.commonutils import prob_at_location
            this = prob_at_location(
                log=log,
                ra=[0.0, 170.],
                dec=[0.0, -40.],
                mjd=[60034.2],
                mapPath=pathToOutputDir + "/bayestar.multiorder.fits"
            )
            print(this)
            assert False
        except Exception as e:
            assert True
            print(str(e))

    def test_prob_at_location_function_exception(self):

        from skytag.commonutils import prob_at_location
        try:
            this = prob_at_location(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
