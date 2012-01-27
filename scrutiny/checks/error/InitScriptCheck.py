
from scrutiny.notice import Error, Warning

class NoReloadEntry(Warning):
    label = 'no-reload-entry'
    descr = "In your init script (/etc/rc.d/init.d/your_file), you don't\nhave a 'reload' entry, which is necessary for a good functionality."

class InitScriptWithoutChkconfigPostin(Error):
    label = 'init-script-without-chkconfig-postin'
    descr = "The package contains an init script but doesn't contain a %post with\na call to chkconfig."

class InitScriptNonExecutable(Error):
    label = 'init-script-non-executable'
    descr = 'The init script should have at least the execution bit set for root \nin order to be run during the boot'

class InitScriptNameWithDot(Error):
    label = 'init-script-name-with-dot'
    descr = 'The init script name should not contains a dot in the name. \nit would not be taken in account by chkconfig'

class IncoherentInitScriptName(Warning):
    label = 'incoherent-init-script-name'
    descr = 'The init script name should be the same as the package name in lower case.'

class PostinWithoutChkconfig(Error):
    label = 'postin-without-chkconfig'
    descr = "The package contains an init script but doesn't call chkconfig in its %post."

class InitScriptWithoutChkconfigPreun(Error):
    label = 'init-script-without-chkconfig-preun'
    descr = "The package contains an init script but doesn't contain a %preun with\na call to chkconfig."

class IncoherentSubsys(Error):
    label = 'incoherent-subsys'
    descr = "The filename of your lock file in /var/lock/subsys/ is incoherent\nwith your actual init script name. For example, if your script name\nis httpd, you have to put a 'httpd' file in your subsys directory."

class SubsysNotUsed(Error):
    label = 'subsys-not-used'
    descr = 'While your program is running, you have to put a lock file in\n/var/lock/subsys/. To see an example, look at this directory on your\nmachine.'

class NoDefaultRunlevel(Warning):
    label = 'no-default-runlevel'
    descr = "The default runlevel isn't specified in the init script."

class PreunWithoutChkconfig(Error):
    label = 'preun-without-chkconfig'
    descr = "The package contains an init script but doesn't call chkconfig in its %preun."

class NoChkconfigLine(Error):
    label = 'no-chkconfig-line'
    descr = "The init script doesn't contain a chkconfig line to specify the runlevels at which\nto start and stop it."

class NoStatusEntry(Error):
    label = 'no-status-entry'
    descr = "In your init script (/etc/rc.d/init.d/your_file), you don't\nhave a 'status' entry, which is necessary for a good functionality."

#---------------------------------------------------------------
# Project         : Mandriva Linux
# Module          : rpmlint
# File            : InitScriptCheck.py
# Version         : $Id: InitScriptCheck.py,v 1.15 2005/08/10 01:51:34 flepied Exp $
# Author          : Frederic Lepied
# Created On      : Fri Aug 25 09:26:37 2000
# Purpose         : check init scripts (files in /etc/rc.d/init.d)
#---------------------------------------------------------------

from Filter import *
import AbstractCheck
import re
import rpm
import Pkg
import string
import Config

rc_regex=re.compile('^/etc(/rc.d)?/init.d/')
chkconfig_content_regex=re.compile('# +chkconfig: +([-0-9]+) +[-0-9]+ +[-0-9]+', re.MULTILINE)
subsys_regex=re.compile('/var/lock/subsys/([^/"\'\n ]+)', re.MULTILINE)
chkconfig_regex=re.compile('^[^#]*(chkconfig|add-service|del-service)', re.MULTILINE)
status_regex=re.compile('^[^#]*status', re.MULTILINE)
reload_regex=re.compile('^[^#]*reload', re.MULTILINE)
basename_regex=re.compile('([^/]+)$')
dot_in_name_regex=re.compile('.*\..*')

class InitScriptCheck(AbstractCheck.AbstractCheck):

    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, 'InitScriptCheck')
    
    def check(self, pkg):
	# Check only binary package
	if pkg.isSource():
	    return

        list=[]
        for f in pkg.files().keys():
            if rc_regex.search(f):
                basename=basename_regex.search(f).group(1)
                list.append(basename)
		if pkg.files()[f][0] & 0500 != 0500:
		    yield InitScriptNonExecutable(pkg,f)
	    
		if dot_in_name_regex.match(basename):
			yield InitScriptNameWithDot(pkg, f)
                # check chkconfig call in %post and %preun
                postin=pkg[rpm.RPMTAG_POSTIN] or pkg[rpm.RPMTAG_POSTINPROG]
                if not postin:
                    yield InitScriptWithoutChkconfigPostin(pkg, f)
                else:
                    if not chkconfig_regex.search(postin):
                        yield PostinWithoutChkconfig(pkg, f)                    
                    
                preun=pkg[rpm.RPMTAG_PREUN] or pkg[rpm.RPMTAG_PREUNPROG]
                if not preun:
                    yield InitScriptWithoutChkconfigPreun(pkg, f)
                else:
                    if not chkconfig_regex.search(preun):
                        yield PreunWithoutChkconfig(pkg, f)

                # check common error in file content
                fd=open(pkg.dirName() + '/' + f, 'r')
                content=fd.read(-1)
                fd.close()
                
                if not status_regex.search(content):
                    yield NoStatusEntry(pkg, f)
                    
                if not reload_regex.search(content):
                    yield NoReloadEntry(pkg, f)
                    
                res=chkconfig_content_regex.search(content)
                if not res:
                    yield NoChkconfigLine(pkg, f)
                else:
                    if res.group(1) == '-':
                        yield NoDefaultRunlevel(pkg)
                        
                res=subsys_regex.search(content)
                if not res:
                    yield SubsysNotUsed(pkg, f)
                else:
                    name=res.group(1)
                    if name != basename:
                        error=1
                        if name[0] == '$':
                            value=Pkg.substitute_shell_vars(name, content)
                            if value == basename:
                                error=0
                        if error:
                            yield IncoherentSubsys(pkg, f, name)

        if len(list) == 1 and string.lower(pkg[rpm.RPMTAG_NAME]) != list[0]:
            yield IncoherentInitScriptName(pkg, list[0])
	    
                
# Create an object to enable the auto registration of the test
check=InitScriptCheck()


def init(checkcontext):
	checkcontext.installCheck(InitScriptCheck)
		
# InitScriptCheck.py ends here
