
from scrutiny.notice import Error, Warning

class OneLineCommandInPost(Warning):
    label = 'one-line-command-in-post'
    descr = 'You should use %post -p <command> instead of using:\n\n%post\n<command>\n\nIt will avoid the fork of a shell interpreter to execute your command as\nwell as allows rpm to automatically mark the dependency on your command.'

class PerlSyntaxErrorIn(Error):
    label = 'perl-syntax-error-in'
    descr = ''

class OneLineCommandInPostun(Warning):
    label = 'one-line-command-in-postun'
    descr = 'You should use %postun -p <command> instead of using:\n\n%postun\n<command>\n\nIt will avoid the fork of a shell interpreter to execute your command as\nwell as allows rpm to automatically mark the dependency on your command.'

class SpuriousBracketInPreun(Warning):
    label = 'spurious-bracket-in-preun'
    descr = 'The %preun scriptlet contains an if [] construction without a space before the\n].'

class NoPrereqOn(Error):
    label = 'no-prereq-on'
    descr = ''

class BogusVariableUseIn(Warning):
    label = 'bogus-variable-use-in'
    descr = ''

class PercentIn(Warning):
    label = 'percent-in'
    descr = ''

class SpuriousBracketInPre(Warning):
    label = 'spurious-bracket-in-pre'
    descr = 'The %pre scriptlet contains an if [] construction without a space before the\n].'

class PostinWithoutGhostFileCreation(Warning):
    label = 'postin-without-ghost-file-creation'
    descr = 'A file tagged as ghost is not created during %prein nor during %postin.'

class UseOfHomeIn(Error):
    label = 'use-of-home-in'
    descr = ''

class OneLineCommandInPre(Warning):
    label = 'one-line-command-in-pre'
    descr = 'You should use %pre -p <command> instead of using:\n\n%pre\n<command>\n\nIt will avoid the fork of a shell interpreter to execute your command as\nwell as allows rpm to automatically mark the dependency on your command.'

class InvalidShellIn(Error):
    label = 'invalid-shell-in'
    descr = ''

class UseTmpIn(Error):
    label = 'use-tmp-in'
    descr = ''

class ShellSyntaxErrorIn(Error):
    label = 'shell-syntax-error-in'
    descr = ''

class SpuriousBracketInPostun(Warning):
    label = 'spurious-bracket-in-postun'
    descr = 'The %postun scriptlet contains an if [] construction without a space before the\n].'

class SpuriousBracketIn(Warning):
    label = 'spurious-bracket-in'
    descr = ''

class NonEmptyIn(Error):
    label = 'non-empty-in'
    descr = ''

class OneLineCommandIn(Warning):
    label = 'one-line-command-in'
    descr = ''

class SpuriousBracketInPost(Warning):
    label = 'spurious-bracket-in-post'
    descr = 'The %post scriptlet contains an if [] construction without a space before the\n].'

class GhostFilesWithoutPostin(Warning):
    label = 'ghost-files-without-postin'
    descr = ''

class EmptyTag(Warning):
    label = 'empty-tag'
    descr = ''

class UpdateMenusWithoutMenuFileIn(Error):
    label = 'update-menus-without-menu-file-in'
    descr = ''

class OneLineCommandInPreun(Warning):
    label = 'one-line-command-in-preun'
    descr = 'You should use %preun -p <command> instead of using:\n\n%preun\n<command>\n\nIt will avoid the fork of a shell interpreter to execute your command as\nwell as allows rpm to automatically mark the dependency on your command.'

class DangerousCommandIn(Warning):
    label = 'dangerous-command-in'
    descr = ''

#############################################################################
# Project         : Mandriva Linux
# Module          : rpmlint
# File            : PostCheck.py
# Version         : $Id: PostCheck.py,v 1.36 2005/06/17 09:27:04 flepied Exp $
# Author          : Frederic Lepied
# Created On      : Wed Jul  5 13:30:17 2000
# Purpose         : Check post/pre scripts
#############################################################################

from Filter import *
import AbstractCheck
import rpm
import re
import os
import commands
import string
import types

DEFAULT_VALID_SHELLS=('/bin/sh',
                      '/bin/bash',
                      '/sbin/sash',
                      '/usr/bin/perl',
                      '/sbin/ldconfig',
                      )

DEFAULT_EMPTY_SHELLS=('/sbin/ldconfig',
                     )

extract_dir=Config.getOption('ExtractDir', '/tmp')
valid_shells=Config.getOption('ValidShells', DEFAULT_VALID_SHELLS)
empty_shells=Config.getOption('ValidEmptyShells', DEFAULT_EMPTY_SHELLS)

braces_regex=re.compile('^[^#]*%', re.MULTILINE)
double_braces_regex=re.compile('%%', re.MULTILINE)
bracket_regex=re.compile('^[^#]*if.*[^ :\]]\]', re.MULTILINE)
home_regex=re.compile('[^a-zA-Z]+~/|\$HOME', re.MULTILINE)
dangerous_command_regex=re.compile("(^|\s|;|/s?bin/|\|)(cp|mv|ln|tar|rpm|chmod|chown|rm|cpio|install|perl|userdel|groupdel)\s", re.MULTILINE)
single_command_regex=re.compile("^[ \n]*([^ \n]+)[ \n]*$")
update_menu_regex=re.compile('update-menus', re.MULTILINE)
tmp_regex=re.compile('\s(/var)?/tmp', re.MULTILINE)
menu_regex=re.compile('^/usr/lib/menu/|^/etc/menu-methods/')
bogus_var_regex=re.compile('(\${?RPM_BUILD_(ROOT|DIR)}?)')

prereq_assoc = (
#    ['chkconfig', ('chkconfig', '/sbin/chkconfig')],
    ['chkfontpath', ('chkfontpath', '/usr/sbin/chkfontpath')],
    ['rpm-helper', ('rpm-helper',)],
    )

for p in prereq_assoc:
    p[0] = re.compile('^[^#]+' + p[0], re.MULTILINE)
    
def incorrect_shell_script(shellscript):
    tmpfile = '%s/.bash-script.%d' % (extract_dir, os.getpid())
    if not shellscript:
        return 0
    file=open(tmpfile, 'w')
    file.write(shellscript)
    file.close()
    ret=commands.getstatusoutput('/bin/bash -n %s' % tmpfile)
    os.remove(tmpfile)
    return ret[0]

def incorrect_perl_script(perlscript):
    tmpfile = '%s/.perl-script.%d' % (extract_dir, os.getpid())
    if not perlscript:
        return 0
    file=open(tmpfile, 'w')
    file.write(perlscript)
    file.close()
    ret=commands.getstatusoutput('/usr/bin/perl -wc %s' % tmpfile)
    os.remove(tmpfile)
    return ret[0]

class PostCheck(AbstractCheck.AbstractCheck):
    
    def __init__(self):
        AbstractCheck.AbstractCheck.__init__(self, 'PostCheck')

    def check(self, pkg):
	# Check only binary package
	if pkg.isSource():
	    return

        menu_error=0
        prereq=map(lambda x: x[0], pkg.prereq())
        files=pkg.files().keys()
        
        for tag in ((rpm.RPMTAG_PREIN, rpm.RPMTAG_PREINPROG, '%pre'),
                    (rpm.RPMTAG_POSTIN, rpm.RPMTAG_POSTINPROG, '%post'),
                    (rpm.RPMTAG_PREUN, rpm.RPMTAG_PREUNPROG, '%preun'),
                    (rpm.RPMTAG_POSTUN, rpm.RPMTAG_POSTUNPROG, '%postun'),
                    (rpm.RPMTAG_TRIGGERSCRIPTS, rpm.RPMTAG_TRIGGERSCRIPTPROG, '%trigger'),
                    ):
            script = pkg[tag[0]]
            prog = pkg[tag[1]]

            if type(script) != types.ListType:
                self.check_aux(pkg, files, prog, script, tag, prereq)
            else:
                for idx in range(0, len(prog)):
                    self.check_aux(pkg, files, prog[idx], script[idx], tag, prereq)
                     
        ghost_files=pkg.ghostFiles()
        if ghost_files:
            postin=pkg[rpm.RPMTAG_POSTIN]
            prein=pkg[rpm.RPMTAG_PREIN]
            if not postin and not prein:
                yield GhostFilesWithoutPostin(pkg)
            else:
                for f in ghost_files:
                    if (not postin or string.find(postin, f) == -1) and \
                       (not prein or string.find(prein, f) == -1):
                        yield PostinWithoutGhostFileCreation(pkg, f)

    def check_aux(self, pkg, files, prog, script, tag, prereq):
        if script:
            if prog:
                if not prog in valid_shells:
                    yield InvalidShellIn(pkg, tag[2], prog)
                if prog in empty_shells:
                    yield NonEmptyIn(pkg, tag[2], prog)
            if prog == '/bin/sh' or prog == '/bin/bash' or prog == '/usr/bin/perl':
                if braces_regex.search(script) and not double_braces_regex.search(script):
                    yield PercentIn(pkg,  tag[2])
                if bracket_regex.search(script):
                    yield SpuriousBracketIn(pkg, tag[2])
                res=dangerous_command_regex.search(script)
                if res:
                    yield DangerousCommandIn(pkg, tag[2], res.group(2))
                if update_menu_regex.search(script):
                    menu_error=1
                    for f in files:
                        if menu_regex.search(f):
                            menu_error=0
                            break
                    if menu_error:
                        yield UpdateMenusWithoutMenuFileIn(pkg, tag[2])
                if tmp_regex.search(script):
                    yield UseTmpIn(pkg, tag[2])
                for c in prereq_assoc:
                    if c[0].search(script):
                        found=0
                        for p in c[1]:
                            if p in prereq or p in files:
                                found=1
                                break
                        if not found:
                            yield NoPrereqOn(pkg, c[1][0])
                            
            if prog == '/bin/sh' or prog == '/bin/bash':
                if incorrect_shell_script(script):
                    yield ShellSyntaxErrorIn(pkg, tag[2])
                if home_regex.search(script):
                    yield UseOfHomeIn(pkg, tag[2])
                res=bogus_var_regex.search(script)
                if res:
                    yield BogusVariableUseIn(pkg, tag[2], res.group(1))

            if prog == '/usr/bin/perl':
                if incorrect_perl_script(script):
                    yield PerlSyntaxErrorIn(pkg, tag[2])
                    
            res=single_command_regex.search(script)
            if res:
                yield OneLineCommandIn(pkg, tag[2], res.group(1))
        else:
            if prog not in empty_shells and prog in valid_shells:
                yield EmptyTag(pkg, tag[2])

# Create an object to enable the auto registration of the test
check=PostCheck()

def init(check):
	check.installCheck(PostCheck)

# PostCheck.py ends here
