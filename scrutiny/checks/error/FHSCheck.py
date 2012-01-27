
from scrutiny.notice import Error, Warning

class FsstndDirInVar(Warning):
    label = 'FSSTND-dir-in-var'
    descr = 'Your package is creating an illegal folder in /var. THE FSSTND (illegal) ones are:\n\t-adm\t\t-catman\n\t-local\t\t-named\n\t-nis\t\t-preserve\n'

class NonStandardDirInVar(Warning):
    label = 'non-standard-dir-in-var'
    descr = 'Your package is creating a non-standard sub directory in /var. The standard directories are:\n\t-account\t-lib\n\t-cache\t\t-crash\n\t-games\t\t-lock\n\t-log\t\t-opt\n\t-run\t\t-spool\n\t-state\t\t-tmp\n\t-yp\t\t-www\n\t-ftp\n'

class NonStandardDirInUsr(Warning):
    label = 'non-standard-dir-in-usr'
    descr = 'Your package is creating a non-standard sub directory in /usr. The standard directories are:\n\t-X11R6\t\t-X386\n\t-bin\t\t-games\n\t-include\t-lib\n\t-local\t\t-sbin\n\t-share\t\t-src\n\t-spool\t\t-tmp\n\t-lib64\n'

#############################################################################
# File		: FHSCheck.py
# Package	: rpmlint
# Author	: Frederic Lepied
# Created on	: Fri Oct 15 17:40:32 1999
# Version	: $Id: FHSCheck.py,v 1.8 2002/07/23 08:23:06 gbeauchesne Exp $
# Purpose	: check FHS conformity
#############################################################################

from Filter import *
import AbstractCheck
import Config
import re

class FHSCheck(AbstractCheck.AbstractCheck):
    usr_regex=re.compile("^/usr/([^/]+)/")
    usr_subdir_regex=re.compile("^(X11R6|X386|bin|games|include|lib|lib64|local|sbin|share|src|spool|tmp)$")
    var_regex=re.compile("^/var/([^/]+)/")
    var_fsstnd_regex=re.compile("^(adm|catman|local|named|nis|preserve)$")
    var_subdir_regex=re.compile("^(account|lib|cache|crash|games|lock|log|opt|run|spool|state|tmp|yp|www|ftp)$")
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, "FHSCheck")

    def check(self, pkg):
	# Check only binary package
	if pkg.isSource():
	    return
	
	files=pkg.files()
	var_list=[]
	usr_list=[]
	
	for f in files.keys():
	    s=FHSCheck.usr_regex.search(f)
	    if s:
		dir=s.group(1)
		if not FHSCheck.usr_subdir_regex.search(dir):
		    if not dir in usr_list:
			yield NonStandardDirInUsr(pkg, dir)
			usr_list.append(dir)
	    else:
		s=FHSCheck.var_regex.search(f)
		if s:
		    dir=s.group(1)
		    if FHSCheck.var_fsstnd_regex.search(dir):
			if not dir in var_list:
			    yield FsstndDirInVar(pkg, f)
			    var_list.append(dir)
		    elif not FHSCheck.var_subdir_regex.search(dir):
			if not dir in var_list:
			    yield NonStandardDirInVar(pkg, dir)
			    var_list.append(dir)
			    
# Create an object to enable the auto registration of the test
check=FHSCheck()



def init(checkcontext):
	checkcontext.installCheck(FHSCheck)
		    
# FHSCheck.py ends here
