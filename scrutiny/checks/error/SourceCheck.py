
from scrutiny.notice import Error, Warning

class SourceOrPatchNotBzipped(Warning):
    label = 'source-or-patch-not-bzipped'
    descr = "A source package or file in your package is not bzipped (doesn't\nhave the .bz2 extension. To bzip it, use bzip2."

class MultipleSpecfiles(Error):
    label = 'multiple-specfiles'
    descr = 'Your package contain multiple spec files. To build a\ncorrect package, you need to have only one spec file containing\nall your RPM information.'

class SourceOrPatchNotGzipped(Warning):
    label = 'source-or-patch-not-gzipped'
    descr = "A source package or file in your package is not gzipped (doesn't\nhave the .gz extension. To gzip it, use the gzip command."

class StrangePermission(Warning):
    label = 'strange-permission'
    descr = 'A file that you listed to include in your package is under strange\npermissions. Usually, a file is under a 0644 permission.'

#############################################################################
# File		: SourceCheck.py
# Package	: rpmlint
# Author	: Frederic Lepied
# Created on	: Wed Oct 27 21:17:03 1999
# Version	: $Id: SourceCheck.py,v 1.10 2003/03/25 12:12:31 flepied Exp $
# Purpose	: verify source package correctness.
#############################################################################

from Filter import *
import AbstractCheck
import re
import Config

DEFAULT_VALID_SRC_PERMS=(0644, 0755)

spec_regex=re.compile('.spec$')
bz2_regex=re.compile('.bz2$')
gz_regex=re.compile('gz$')
source_regex=re.compile('\\.(tar|patch|tgz|diff)$')
use_bzip2=Config.getOption('UseBzip2', 1)
valid_src_perms=Config.getOption("ValidSrcPerms", DEFAULT_VALID_SRC_PERMS)

class SourceCheck(AbstractCheck.AbstractCheck):

    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, 'SourceCheck')

    def check(self, pkg):
	# Check only source package
	if not pkg.isSource():
	    return

	# process file list
	files=pkg.files()
	spec_file=None
	for f in files.keys():
	    if spec_regex.search(f):
		if spec_file:
		    yield MultipleSpecfiles(pkg, spec_file, f)
		else:
		    spec_file=f
	    elif source_regex.search(f):
		if use_bzip2:
		    if not bz2_regex.search(f):
			yield SourceOrPatchNotBzipped(pkg, f)
		else:
		    if not gz_regex.search(f):
			yield SourceOrPatchNotGzipped(pkg, f)
	    perm=files[f][0] & 07777
	    if perm not in valid_src_perms:
		yield StrangePermission(pkg, f, oct(perm))	    
		
check=SourceCheck()



def init(context):
	context.installCheck(SourceCheck)
# SourceCheck.py ends here
