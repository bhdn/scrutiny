#------------------------------------------------------------------------------
# File				: DistributionCheck.py
# Package       	: scrutiny
# Original Author	: Frederic Lepied
# Purpose			: check the Distribution specificities in a binary rpm package.
#------------------------------------------------------------------------------

from scrutiny.notice import Warning

from Filter import *
import AbstractCheck
import rpm
import re
import Config

man_regex=re.compile("/man./")
info_regex=re.compile("(/usr/share|/usr)/info/")
info_dir_regex=re.compile("/info/dir$")
bz2_regex=re.compile(".bz2$")
gz_regex=re.compile(".gz$")
vendor=Config.getOption("Vendor", "Mandriva")
distribution=Config.getOption("Distribution", "Mandriva Linux")
use_bzip2=Config.getOption("UseBzip2", 1)

class ManpageNotGzipped(Warning):
    label = 'manpage-not-gzipped'
    descr = 'Manual Pages are not under the .gz extension/format. Please\nrun gzip <man page file> to gzip it and after, build the package.'

class InfopageNotGzipped(Warning):
    label = 'infopage-not-gzipped'
    descr = 'An info page is not under the .gz extension/format. Please\nrun gzip <info page file> to gzip it and after, build the package.'

class InvalidVendor(Warning):
    label = 'invalid-vendor'
    descr = 'In the Mandriva Linux distribution, the vendor should be "Mandriva".'

class ManpageNotBzipped(Warning):
    label = 'manpage-not-bzipped'
    descr = 'Manual Pages are not under the .bz2 extension/format. Please\nrun bzip2 <man page file> to bzip it in the %install section and\nafter, build the package. You can also use the spec-helper package\nthat automatizes this task.'

class InfopageNotBzipped(Warning):
    label = 'infopage-not-bzipped'
    descr = 'An info page is not under the .bz2 extension/format. Please\nrun bzip2 <info page file> to bzip it and after, build the package.\nYou can also use the spec-helper package that automatizes this task.'

class InvalidDistribution(Warning):
    label = 'invalid-distribution'
    descr = 'The distribution value should be "Mandriva Linux".'

class DistributionCheck(AbstractCheck.AbstractCheck):

    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, "DistributionCheck")

    def check(self, pkg):
	# Check only binary package
	if pkg.isSource():
	    return
	
	if pkg[rpm.RPMTAG_VENDOR] != vendor:
	    yield InvalidVendor(pkg, pkg[rpm.RPMTAG_VENDOR])

	if pkg[rpm.RPMTAG_DISTRIBUTION] != distribution:
	    yield InvalidDistribution(pkg, pkg[rpm.RPMTAG_DISTRIBUTION])

	# Check the listing of files
	list=pkg[rpm.RPMTAG_FILENAMES]
	
	if list:
	    for f in list:
		if man_regex.search(f):
		    if use_bzip2:
			if not bz2_regex.search(f):
			    yield ManpageNotBzipped(pkg, f)
		    elif not gz_regex.search(f):
			yield ManpageNotGzipped(pkg, f)
		if info_regex.search(f) and not info_dir_regex.search(f):
		    if use_bzip2:
			if not bz2_regex.search(f):
			    yield InfopageNotBzipped(pkg, f)
		    elif not gz_regex.search(f):
			    yield InfopageNotGzipped(pkg, f)

# Create an object to enable the auto registration of the test
check=DistributionCheck()



def init(context):
	context.installCheck(DistributionCheck)
    
# DistributionCheck.py ends here
