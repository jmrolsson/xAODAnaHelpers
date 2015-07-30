#!/usr/bin/python
#
# *******************************************************************************
# script to checkout specific ASG packages for a given release,
# and apply svn patches if needed
#
# Authors:
#  M.Milesi(mrco.milesi@cern.ch), G.Stark(g.stark@cern.ch)
#
# Usage (from the directory where ASG release has been set up):
#  python () (./xAODAnaHelpers/scripts/)checkoutASGtags.py RELEASE_NUMBER [X.Y.Z]
# *******************************************************************************

import os, subprocess
import argparse

rc_env = os.environ.copy()

parser = argparse.ArgumentParser(description='Checkout packages and apply patches!', usage='%(prog)s version')
parser.add_argument('version', help='the ASG release you have set up')
args = parser.parse_args()

print "Using ASG version {0}".format(args.version)


##check that you're in the right directory?

dict_pkg = {
            '2.3.18': ["atlasoff/Reconstruction/Jet/JetUncertainties/tags/JetUncertainties-00-09-28",
                       "atlasoff/Reconstruction/Jet/JetResolution/tags/JetResolution-03-00-36",
                       "atlasoff/Reconstruction/Jet/JetCalibTools/tags/JetCalibTools-00-04-46",
                       "atlasoff/Trigger/TrigAnalysis/TrigEgammaMatchingTool/tags/TrigEgammaMatchingTool-00-00-05",
		                   "atlasoff/PhysicsAnalysis/AnalysisCommon/IsolationSelection/tags/IsolationSelection-00-00-10"],
            '2.3.19': ["atlasoff/Trigger/TrigAnalysis/TrigEgammaMatchingTool/tags/TrigEgammaMatchingTool-00-00-05",
		                   "atlasoff/PhysicsAnalysis/AnalysisCommon/IsolationSelection/tags/IsolationSelection-00-00-10",
                       "atlasoff/Reconstruction/Jet/JetUncertainties/tags/JetUncertainties-00-09-29"],
            '2.3.21': []
           }

try:
  packages_to_checkout = dict_pkg[args.version]
except KeyError:
  print "Warning: that version isn't supported! This may not be a problem if you're using a new ASG release."
  import sys
  sys.exit(0)

if len(packages_to_checkout) == 0:
  print "No packages needed for version ", args.version
else:
  for pkg in packages_to_checkout:
    print "Checking out package: {0}".format(pkg)
    subprocess.Popen(['cd $ROOTCOREBIN/.. && pwd && rc checkout_pkg {0}'.format(pkg) ], env=rc_env, shell=True).wait()

###  Apply Local Patches ###
packages_to_patch = []
print "Applying svn patches..."
for pkg in packages_to_patch:
  if pkg in packages_to_checkout:
    print "  patching {0}".format(pkg)
    subprocess.Popen(['cd $ROOTCOREBIN/../{0} && pwd && patch -p0 -i $ROOTCOREBIN/../xAODAnaHelpers/data/{0}_Base.{1}.diff && cd - && pwd'.format(pkg, args.version)], env=rc_env, shell=True ).wait()
  else:
    print "  no patches to be applied!"

#### Update Run II GRLs ####
print "Updating GRL..."
physicsGRL = "http://atlasdqm.web.cern.ch/atlasdqm/grlgen/All_Good/data15_13TeV.periodAllYear_DetStatus-v63-pro18-01_DQDefects-00-01-02_PHYS_StandardGRL_All_Good.xml"
atlasReadyGRL = "http://atlasdqm.web.cern.ch/atlasdqm/grlgen/Atlas_Ready/data15_13TeV.periodAllYear_HEAD_DQDefects-00-01-02_PHYS_StandardGRL_Atlas_Ready.xml"
try:
  subprocess.call(["wget","-q",physicsGRL,"-O", "xAODAnaHelpers/data/"+physicsGRL.split('/')[-1]])
  subprocess.call(["wget","-q",atlasReadyGRL,"-O","xAODAnaHelpers/data/"+atlasReadyGRL.split('/')[-1]])
except OSError as e:
  print "Error, wget is not available.  Will not download grl.  You can find the latest version at", physicsGRL
