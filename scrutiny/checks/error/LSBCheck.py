
from scrutiny.notice import Error, Warning

class NonLsbCompliantRelease(Error):
    label = 'non-lsb-compliant-release'
    descr = 'Your version number contains an illegal character. Use only\nlowercase letters and/or numbers.'

class NonLsbCompliantVersion(Error):
    label = 'non-lsb-compliant-version'
    descr = 'Your version number contains an illegal character. Use only\nlowercase letters and/or numbers.'

class NonLsbCompliantPackageName(Error):
    label = 'non-lsb-compliant-package-name'
    descr = 'Your package name contains an illegal character. Use only\nalphanumeric symbols in your package name.'

#---------------------------------------------------------------
# Project         : Mandriva Linux
# Module          : rpmlint
# File            : LSBCheck.py
# Version         : $Id: LSBCheck.py,v 1.9 2005/04/15 20:01:46 flepied Exp $
# Author          : Frederic Lepied
# Created On      : Tue Jan 30 14:44:37 2001
# Purpose         : LSB non compliance checks
#---------------------------------------------------------------

from Filter import *
import AbstractCheck
import rpm
import re

version_regex=re.compile('^[a-zA-Z0-9.+]+$')
name_regex=re.compile('^[a-z0-9.+-]+$')

class LSBCheck(AbstractCheck.AbstractCheck):
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, "LSBCheck")

    def check(self, pkg):

	name=pkg[rpm.RPMTAG_NAME]
	if name and not name_regex.search(name):
	    yield NonLsbCompliantPackageName(pkg, name)

	version=pkg[rpm.RPMTAG_VERSION]
	if version and not version_regex.search(version):
	    yield NonLsbCompliantVersion(pkg, version)

        release=pkg[rpm.RPMTAG_RELEASE]
	if release and not version_regex.search(release):
	    yield NonLsbCompliantRelease(pkg, release)

# Create an object to enable the auto registration of the test
check=LSBCheck()


def init(checkcontext):
	checkcontext.installCheck(LSBCheck)
# LSBCheck.py ends here
