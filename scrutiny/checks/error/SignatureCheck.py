
from scrutiny.notice import Error, Warning

class NoSignature(Error):
    label = 'no-signature'
    descr = 'You have to include your pgp or gpg signature in your package.\nFor more information on signatures, please refer to www.gnupg.org.'

class UnknownKey(Error):
    label = 'unknown-key'
    descr = 'The package was signed, but with an unknown key.\nSee the rpm --import option for more information.'

#############################################################################
# File		: SignatureCheck.py
# Package	: rpmlint
# Author	: Frederic Lepied
# Created on	: Thu Oct  7 17:06:14 1999
# Version	: $Id: SignatureCheck.py,v 1.8 2003/04/23 13:32:46 flepied Exp $
# Purpose	: check the presence of a PGP signature.
#############################################################################

from Filter import *
import AbstractCheck
import re
import sys

class SignatureCheck(AbstractCheck.AbstractCheck):
    pgp_regex=re.compile("pgp|gpg", re.IGNORECASE)
    unknown_key_regex=re.compile("\(MISSING KEYS:\s+([^\)]+)\)")
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, "SignatureCheck")

    def check(self, pkg):
	res=pkg.checkSignature()
	if not res or res[0] != 0:
            if res and res[1]:
                kres=SignatureCheck.unknown_key_regex.search(res[1])
            else:
                kres=None
            if kres:
                yield UnknownKey(pkg, kres.group(1))
            else:
                sys.stderr.write("error checking signature of " + pkg.filename + "\n")
	else:
	    if not SignatureCheck.pgp_regex.search(res[1]):
		yield NoSignature(pkg)
	
# Create an object to enable the auto registration of the test
check=SignatureCheck()

def init(context):
	context.installCheck(SignatureCheck)

# SignatureCheck.py ends here
