
from scrutiny.notice import Error, Warning

class FileInUsrMarkedAsConffile(Error):
    label = 'file-in-usr-marked-as-conffile'
    descr = 'A file in /usr is marked as being a configuration file.\nStore your conf files in /etc/ instead.'

class ScoreFileMustNotBeConffile(Error):
    label = 'score-file-must-not-be-conffile'
    descr = 'A file in /var/lib/games/ is a configuration file. Store your conf\nfiles in /etc instead.'

class AppDefaultsMustNotBeConffile(Error):
    label = 'app-defaults-must-not-be-conffile'
    descr = 'A file in /usr/X11R6/lib/X11/app-defaults/ is a configuration file.\nIf you need to store your conf file, put it in /etc.'

class NonEtcOrVarFileMarkedAsConffile(Warning):
    label = 'non-etc-or-var-file-marked-as-conffile'
    descr = 'A file not in /etc or /var is marked as being a configuration file.\nPlease put your conf files in /etc or /var.'

class ConffileWithoutNoreplaceFlag(Warning):
    label = 'conffile-without-noreplace-flag'
    descr = 'A configuration file is stored in your package without the noreplace flag.\nA way to resolve this is to put the following in your SPEC file:\n\n%config(noreplace) /etc/your_config_file_here\n'

#############################################################################
# File		: ConfigCheck.py
# Package	: rpmlint
# Author	: Frederic Lepied
# Created on	: Sun Oct  3 21:48:20 1999
# Version	: $Id: ConfigCheck.py,v 1.8 2001/11/14 16:34:02 flepied Exp $
# Purpose	: 
#############################################################################

from Filter import *
import AbstractCheck
import Config
import re

class ConfigCheck(AbstractCheck.AbstractCheck):
    games_regex=re.compile("^/var/lib/games")
    usr_regex=re.compile("^/usr/")
    etc_var_regex=re.compile("^/etc/|^/var/")
    appdefaults_regex=re.compile("^/usr/X11R6/lib/X11/app-defaults/")
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, "ConfigCheck")

    def check(self, pkg):
	# Check only binary package
	if pkg.isSource():
	    return
	
	config_files=pkg.configFiles()
        noreplace_files=pkg.noreplaceFiles()
        
	for c in config_files:
	    if ConfigCheck.appdefaults_regex.search(c):
		yield AppDefaultsMustNotBeConffile(pkg, c)
	    if ConfigCheck.games_regex.search(c):
		yield ScoreFileMustNotBeConffile(pkg, c)
	    if ConfigCheck.usr_regex.search(c):
		yield FileInUsrMarkedAsConffile(pkg, c)
	    elif not ConfigCheck.etc_var_regex.search(c):
		yield NonEtcOrVarFileMarkedAsConffile(pkg, c)

            if not c in noreplace_files:
                yield ConffileWithoutNoreplaceFlag(pkg, c)
                
# Create an object to enable the auto registration of the test
check=ConfigCheck()



def init(checkcontext):
	checkcontext.installCheck(ConfigCheck)

# ConfigCheck.py ends here
