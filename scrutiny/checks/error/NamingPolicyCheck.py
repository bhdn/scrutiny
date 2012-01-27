
from scrutiny.notice import Error, Warning

class Perl5NamingPolicyNotApplied(Warning):
    label = 'perl5-naming-policy-not-applied'
    descr = "This package doesn't respect the naming policy.\nThe name sould begin with perl-.\nIt should only be used for separate packages modules."

class FortuneNamingPolicyNotApplied(Warning):
    label = 'fortune-naming-policy-not-applied'
    descr = "This package doesn't respect the naming policy.\nThe name sould begin with fortune-.\nIt should only be used for separate packages modules."

class NamingPolicyNotApplied(Warning):
    label = 'naming-policy-not-applied'
    descr = ''

class OcamlNamingPolicyNotApplied(Warning):
    label = 'ocaml-naming-policy-not-applied'
    descr = "This package doesn't respect the naming policy.\nThe name sould begin with ocaml-.\nIt should only be used for separate packages modules."

class Apache2NamingPolicyNotApplied(Warning):
    label = 'apache2-naming-policy-not-applied'
    descr = "This package doesn't respect the naming policy.\nThe name sould begin with apache2-mod_.\nIt should only be used for separate packages modules."

class XmmsNamingPolicyNotApplied(Warning):
    label = 'xmms-naming-policy-not-applied'
    descr = "This package doesn't respect the naming policy.\nThe name sould begin with xmms-.\nIt should only be used for separate packages modules."

class PythonNamingPolicyNotApplied(Warning):
    label = 'python-naming-policy-not-applied'
    descr = "This package doesn't respect the naming policy.\nThe name sould begin with python-.\nIt should only be used for separate packages modules."

class PhpNamingPolicyNotApplied(Warning):
    label = 'php-naming-policy-not-applied'
    descr = "This package doesn't respect the naming policy.\nThe name sould begin with php-.\nIt should only be used for separate packages modules."

class RubyNamingPolicyNotApplied(Warning):
    label = 'ruby-naming-policy-not-applied'
    descr = "This package doesn't respect the naming policy.\nThe name sould begin with ruby-.\nIt should only be used for separate packages modules."

#---------------------------------------------------------------
# Project         : Mandriva Linux
# Module          : rpmlint
# File            : NamingPolicyCheck.py
# Version         : $Id: NamingPolicyCheck.py,v 1.7 2005/04/15 20:01:46 flepied Exp $
# Author          : Michael Scherer
# Created On      : Mon May 19 11:25:37 2003
# Purpose         : Check package names according to their content.
#---------------------------------------------------------------

from Filter import *
import AbstractCheck
import rpm
import re
import Config

# could be added.
#
# zope 
# abiword2
# alsaplayer-plugin-input
# emacs
# gstreamer
# nautilus
# vlc-plugin
# XFree
# xine 

executable_re=re.compile('^(/usr)?/(s?bin|games)/\S+')
simple_naming_policy_re=re.compile('\^[a-zA-Z1-9-_]*$');

class NamingPolicyCheck(AbstractCheck.AbstractCheck):
    checks_=[]
    
    def __init__(self):
        AbstractCheck.AbstractCheck.__init__(self, "NamingPolicyCheck")
        
    def add_check(pkg_name,name_re,file_re,exception):
        c={}
        c['pkg_name']=pkg_name
        c['name_re']=re.compile(name_re)
        c['file_re']=re.compile(file_re)
	c['exception']=exception
        NamingPolicyCheck.checks_.append(c)
        if Config.info:
            if simple_naming_policy_re.search(name_re):
                details="The name sould begin with " + name_re[1:]
            else:
                details="The name should match this regular expression " + name_re
				
            addDetails(pkg_name + '-naming-policy-not-applied',
                       "This package doesn't respect the naming policy.\n" 
                       + details + ".\nIt should only be used for separate packages modules.")
    add_check = staticmethod(add_check)
            
    def check(self, pkg):
        if pkg.isSource():
            return
        list=pkg[rpm.RPMTAG_FILENAMES]
        if not list:
            return
        try:
	    # check for binaries first
	    executables=0
	    for f in list:
		if executable_re.search(f):
		    executables=1
		    break

            # check for files then
            for c in self.checks_:
		exception=0
		if c['exception'] and executables:
		    exception=1

                for f in list:
		    if c['file_re'].search(f) and not c['name_re'].search(pkg[rpm.RPMTAG_NAME]) and not exception:
                        raise 'naming-policy-not-applied'
        except 'naming-policy-not-applied':	
            yield NamingPolicyNotApplied(pkg, f, c['pkg_name'])

check=NamingPolicyCheck

#
# these are the check currently impleted.
#  
# first argument is the name of the check, yield printed by the warning.
#   ex : xmms.
#
# secund argument is the regular expression of the naming policy.
#   ex: xmms plugin should be named xmms-name_of_plugin.
#
# third is the path of the file that should contains a package to be related to the naming scheme.
#   ex: xmms plugin are put under /usr/lib/xmms/
#
# fourth is a boolean for excepting packages with any executable in path of the naming scheme
#   ex: a perl package with files both in /usr/bin and in /usr/lib/perl5 can be either a module with exemple script, of a perl programs with some personal modules
#
# the module is far from being perfect since you need to check this file for the naming file.
#
# the module is far from being perfect since you need to check this file for the naming file.
# if somone as a elegant solution, I will be happy to implement and test it.


check.add_check('xmms', '^xmms-', '^/usr/lib/xmms/', 0)
check.add_check('python', '^python-', '^/usr/lib/python[1-9](-[1-9])?', 1)
check.add_check('perl5', '^perl-', '^/usr/lib/perl5/vendor_perl', 1)
check.add_check('apache2', '^apache2-mod_', '^/usr/lib/apache2-', 0)
check.add_check('fortune', '^fortune-', '^/usr/share/games/fortunes/', 0)
check.add_check('php', '^php-', '/usr/lib/php/extensions/', 1)
check.add_check('ruby', '^ruby-', '/usr/lib/ruby/[1-9](-[1-9])?/', 1)
check.add_check('ocaml', '^ocaml-', '/usr/lib/ocaml/', 1)

# these exception should be added 
# apache2 => apache2-devel
#            apache2-modules
# ruby => apache2-mod_ruby
#         ruby


# NamingPolicyCheck.py ends here
def init(context):
	context.installCheck(NamingPolicyCheck)
