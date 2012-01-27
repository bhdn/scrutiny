
from scrutiny.notice import Error, Warning

class ZeroLength(Error):
    label = 'zero-length'
    descr = ''

class PerlTempFile(Warning):
    label = 'perl-temp-file'
    descr = 'You have a perl temporary file in your package. Usually, this\nfile is beginning with a dot (.) and contain "perl" in its name.'

class NonGhostFile(Error):
    label = 'non-ghost-file'
    descr = 'File should be tagged %ghost.'

class VersionControlInternalFile(Error):
    label = 'version-control-internal-file'
    descr = 'You have included file(s) internally used by a version control system\nin the package. Move these files out of the package and rebuild it.'

class DanglingRelativeSymlink(Warning):
    label = 'dangling-relative-symlink'
    descr = 'The relative symbolic link points nowhere.'

class PostinWithoutLdconfig(Error):
    label = 'postin-without-ldconfig'
    descr = "This package contains a library and its %post doesn't call ldconfig."

class IncoherentLogrotateFile(Error):
    label = 'incoherent-logrotate-file'
    descr = 'Your logrotate file should be named /etc/logrotate.d/<package name>.'

class PostinWithWrongDepmod(Error):
    label = 'postin-with-wrong-depmod'
    descr = 'This package contains a kernel module but its %post calls depmod for the wrong kernel.'

class NotListedAsDocumentation(Error):
    label = 'not-listed-as-documentation'
    descr = 'The documentation files of this package are not listed with\nthe standard %doc tag.'

class NonExecutableScript(Error):
    label = 'non-executable-script'
    descr = 'This script is not executable.'

class PostunWithWrongDepmod(Error):
    label = 'postun-with-wrong-depmod'
    descr = 'This package contains a kernel module but its %postun calls depmod for the wrong kernel.'

class DirOrFileInVarLocal(Error):
    label = 'dir-or-file-in-var-local'
    descr = "A file in the package is located in /var/local. It's not permitted\nto put a file in this directory."

class ManifestInPerlModule(Warning):
    label = 'manifest-in-perl-module'
    descr = 'This perl module package contains a MANIFEST or a MANIFEST.SKIP file\nin the documentation directory.'

class PostunWithoutLdconfig(Error):
    label = 'postun-without-ldconfig'
    descr = "This package contains a library and its %postun doesn't call ldconfig."

class CrossCompileName(Error):
    label = 'cross-compile-name'
    descr = ''

class LengthySymlink(Warning):
    label = 'lengthy-symlink'
    descr = ''

class NonStandardGid(Error):
    label = 'non-standard-gid'
    descr = 'A file in this package is owned by a non standard group.\nStandard groups are:\n\n- root\t\t- bin\t\t- dip\n- daemon\t- sys\t\t- ftp\n- adm\t\t- tty\t\t- smb\n- disk\t\t- lp\t\t- cdrom\n- mem\t\t- kmem\t\t- pppusers\n- wheel\t\t- floppy\t- cdwriter\n- mail\t\t- news\t\t- audio\n- uucp\t\t- man\t\t- dos\n- games\t\t- gopher\t- nobody\n- users\t\t- console\t- utmp\n- lists\t\t- gdm\t\t- xfs\n- popusers\t- slipusers\t- slocate\n- x10\t\t- urpmi\t\t- apache\n- postgres\t- rpcuser\t- rpm'

class NoDependencyOn(Warning):
    label = 'no-dependency-on'

class HtaccessFile(Error):
    label = 'htaccess-file'
    descr = 'You have individual apache configuration .htaccess file(s) in your package. Replace them by a central configuration file in /etc/httpd/webapps.d.'

class DirOrFileInTmp(Error):
    label = 'dir-or-file-in-tmp'
    descr = "A file in the package is located in /tmp. It's not permitted\nto put a file in this directory."

class WrongFileEndOfLineEncoding(Warning):
    label = 'wrong-file-end-of-line-encoding'
    descr = 'This file has wrong end-of-line encoding, usually caused by creation on a\nnon-Unix system. It could harm its visualisation.'

class SymlinkContainsUpAndDownSegments(Error):
    label = 'symlink-contains-up-and-down-segments'

class NonReadable(Error):
    label = 'non-readable'
    descr = "The file can't be read by everybody. If this is normal (for security reason), send an\nemail to <flepied at mandriva.com> to add it to the list of exceptions in the next release."

class DirOrFileInUsrLocal(Error):
    label = 'dir-or-file-in-usr-local'
    descr = "A file in the package is located in /usr/local. It's not permitted\nto put a file in this directory."

class SetuidBinary(Error):
    label = 'setuid-binary'
    descr = 'The file is setuid. Usually this is a bug. Otherwise, please contact\n<flepied at mandriva.com> about this so that this error gets included\nin the exception file for rpmlint. With that, rpmlint will ignore\nthis bug in the future.'

class OutsideLibdirFiles(Error):
    label = 'outside-libdir-files'
    descr = 'This library package must not contain non library files to allow 64\nand 32 bits versions of the package to coexist.'

class DirOrFileInOpt(Error):
    label = 'dir-or-file-in-opt'
    descr = "A file in the package is located in /opt. It's not permitted\nto put a file in this directory."

class DirOrFileInHome(Error):
    label = 'dir-or-file-in-home'
    descr = "A file in the package is located in /home. It's not permitted\nto put a file in this directory."

class WrongScriptInterpreter(Error):
    label = 'wrong-script-interpreter'
    descr = 'This script uses an incorrect interpreter.'

class ModuleWithoutDepmodPostun(Error):
    label = 'module-without-depmod-postun'
    descr = 'This package contains a kernel module but provides no call to depmod in %postun.'

class InfoFilesWithoutInstallInfoPostun(Error):
    label = 'info-files-without-install-info-postun'
    descr = 'This package contains info files and provides no %postun with a call to install-info.'

class SiteperlInPerlModule(Warning):
    label = 'siteperl-in-perl-module'
    descr = 'This perl module package installs files under the subdirectory site_perl,\nwhile they must appear under vendor_perl.'

class StandardDirOwnedByPackage(Error):
    label = 'standard-dir-owned-by-package'
    descr = 'This package owns a directory that is part of the standard hierarchy and this\ncan lead to default directory rights, owner or group be changed to something\nnon standard.'

class SubdirInBin(Error):
    label = 'subdir-in-bin'
    descr = "The package contains a subdirectory in /usr/bin. It's not permitted to\ncreate a subdir there. Create it in /usr/lib/ instead."

class KernelModulesNotInKernelPackages(Error):
    label = 'kernel-modules-not-in-kernel-packages'
    descr = ''

class InfoDirFile(Error):
    label = 'info-dir-file'
    descr = "You have /usr/info/dir or /usr/share/info/dir in your package. It's not allowed.\nPlease remove it and rebuild your package."

class CompressedSymlinkWithWrongExt(Error):
    label = 'compressed-symlink-with-wrong-ext'
    descr = "The symlink points to a compressed file but doesn't use the same extension."

class PostunWithoutInstallInfo(Warning):
    label = 'postun-without-install-info'
    descr = "This package contains info files and its %postun doesn't call install-info."

class ExecutableMarkedAsConfigFile(Error):
    label = 'executable-marked-as-config-file'
    descr = 'Executables must not be marked as config files because it will\nprevent upgrades to work correctly. If you need to be able to\ncustomize an executable, make it read a config file in /etc/sysconfig\nfor example.'

class NonStandardExecutablePerm(Error):
    label = 'non-standard-executable-perm'
    descr = 'A standard executable should have permission set to 0755. If you get this message,\nthat means that you have a wrong executable permission in your package.'

class LibraryWithoutLdconfigPostun(Error):
    label = 'library-without-ldconfig-postun'
    descr = 'This package contains a library and provides no %postun with a call to ldconfig.'

class ModuleWithoutDepmodPostin(Error):
    label = 'module-without-depmod-postin'
    descr = 'This package contains a kernel module but provides no call to depmod in %post.'

class NonStandardUid(Error):
    label = 'non-standard-uid'
    descr = 'A file in this package is owned by a non standard owner.\nStandard owners are:\n\n- root\t\t- bin\n- daemon\t- adm\n- lp\t\t- sync\n- shutdown\t- halt\n- mail\t\t- news\n- uucp\t\t- operator\n- games\t\t- gopher\n- ftp\t\t- nobody\n- nobody\t- lists\n- gdm\t\t- xfs\n- apache\t- postgres\n- rpcuser\t- rpm'

class SymlinkShouldBeAbsolute(Warning):
    label = 'symlink-should-be-absolute'

class DevelFileInNonDevelPackage(Warning):
    label = 'devel-file-in-non-devel-package'
    descr = 'A development file (usually source code) is located in a non-devel\npackage. If you want to include source code in your package, be sure to\ncreate a development package.'

class SymlinkShouldBeRelative(Warning):
    label = 'symlink-should-be-relative'

class NonRootGroupLogFile(Error):
    label = 'non-root-group-log-file'
    descr = 'If you need non root log file, just create a subdir in /var/log and put your files inside.'

class ScriptWithoutShellbang(Error):
    label = 'script-without-shellbang'
    descr = 'This script does not begins with a shellbang. It will prevent its execution.'

class NoDocumentation(Warning):
    label = 'no-documentation'
    descr = 'The package contains no documentation (README, doc, etc).\nYou have to include documentation files.'

class WrongScriptEndOfLineEncoding(Error):
    label = 'wrong-script-end-of-line-encoding'
    descr = 'This script has wrong end-of-line encoding, usually caused by creation on a\nnon-Unix system. It will prevent its execution.'

class SetgidBinary(Error):
    label = 'setgid-binary'
    descr = 'The file is setgid. Usually this is a bug. Otherwise, please contact\n<flepied at mandriva.com> about this so that this error gets included\nin the exception file for rpmlint. With that, rpmlint will ignore\nthis bug in the future.'

class InfoFilesWithoutInstallInfoPostin(Error):
    label = 'info-files-without-install-info-postin'
    descr = 'This package contains info files and provides no %post with a call to install-info.'

class SymlinkHasTooManyUpSegments(Error):
    label = 'symlink-has-too-many-up-segments'

class LibraryWithoutLdconfigPostin(Error):
    label = 'library-without-ldconfig-postin'
    descr = 'This package contains a library and provides no %post with a call to ldconfig.'

class MispelledMacro(Warning):
    label = 'mispelled-macro'
    descr = 'This package contains a file which match %{.*}, this is often the sign\nof a mispelled macro. Please check your spec file.'

class PostinWithoutInstallInfo(Error):
    label = 'postin-without-install-info'
    descr = "This package contains info files and its %post doesn't call install-info."

class LogFilesWithoutLogrotate(Warning):
    label = 'log-files-without-logrotate'
    descr = 'This package use files in /var/log/ without adding a entry for \nlogrotate.'

class SetuidGidBinary(Error):
    label = 'setuid-gid-binary'
    descr = 'The file is setuid and setgid. Usually this is a bug. Otherwise, please contact\n<flepied at mandriva.com> about this so that this error gets included\nin the exception file for rpmlint. With that, rpmlint will ignore\nthis bug in the future.'

class NonExecutableInBin(Warning):
    label = 'non-executable-in-bin'
    descr = 'A file is being installed in /usr/bin, but is not an executable. Be sure\nthat the file is an executable or that it has executable permissions.'

class NonConffileInEtc(Warning):
    label = 'non-conffile-in-etc'
    descr = 'A non-executable file in your package is being installed in /etc, but is not\na configuration file. All non-executable files in /etc should be configuration\nfiles. Mark the file as %config in the spec file.'

class DirOrFileInMnt(Error):
    label = 'dir-or-file-in-mnt'
    descr = "A file in the package is located in /mnt. It's not permitted\nto put a file in this directory."

class HiddenFileOrDir(Warning):
    label = 'hidden-file-or-dir'
    descr = 'The file or directory is hidden. You should see if this is normal, \nand delete it if needed.'

class NonRootUserLogFile(Error):
    label = 'non-root-user-log-file'
    descr = 'If you need non root log file, just create a subdir in /var/log and put your files inside.'

class DanglingSymlink(Warning):
    label = 'dangling-symlink'
    descr = 'The symbolic link points nowhere.'

class NonStandardDirPerm(Error):
    label = 'non-standard-dir-perm'
    descr = 'A standard directory should have permission set to 0755. If you get this message,\nthat means that you have a wrong directory permission in your package.'

class BackupFileInPackage(Error):
    label = 'backup-file-in-package'
    descr = 'You have a backup file in your package. The files are usually\nbeginning with ~ (vi) or #file# (emacs). Please remove it and rebuild\nyour package.'

#############################################################################
# File		: FilesCheck.py
# Package	: rpmlint
# Author	: Frederic Lepied
# Created on	: Mon Oct  4 19:32:49 1999
# Version	: $Id: FilesCheck.py,v 1.88 2005/08/10 01:46:30 flepied Exp $
# Purpose	: test various aspects on files: locations, owner, groups,
#		permission, setuid, setgid...
#############################################################################

from Filter import *
import AbstractCheck
import rpm
import re
import stat
import string
import os
import Config

# must be kept in sync with the filesystem package
STANDARD_DIRS=(
    '/bin',
    '/boot',
    '/etc',
    '/etc/X11',
    '/etc/opt',
    '/etc/skel',
    '/etc/xinetd.d',
    '/home',
    '/lib',
    '/lib64',
    '/lib/modules',
    '/mnt',
    '/mnt/cdrom',
    '/mnt/disk',
    '/mnt/floppy',
    '/opt',
    '/proc',
    '/root',
    '/sbin',
    '/tmp',
    '/usr',
    '/usr/X11R6',
    '/usr/X11R6/bin',
    '/usr/X11R6/doc',
    '/usr/X11R6/include',
    '/usr/X11R6/lib',
    '/usr/X11R6/lib64',
    '/usr/X11R6/man',
    '/usr/X11R6/man/man1',
    '/usr/X11R6/man/man2',
    '/usr/X11R6/man/man3',
    '/usr/X11R6/man/man4',
    '/usr/X11R6/man/man5',
    '/usr/X11R6/man/man6',
    '/usr/X11R6/man/man7',
    '/usr/X11R6/man/man8',
    '/usr/X11R6/man/man9',
    '/usr/X11R6/man/mann',
    '/usr/bin',
    '/usr/bin/X11',
    '/usr/etc',
    '/usr/games',
    '/usr/include',
    '/usr/lib',
    '/usr/lib64',
    '/usr/lib/X11',
    '/usr/lib/games',
    '/usr/lib/gcc-lib',
    '/usr/lib/menu',
    '/usr/lib64/gcc-lib',
    '/usr/local',
    '/usr/local/bin',
    '/usr/local/doc',
    '/usr/local/etc',
    '/usr/local/games',
    '/usr/local/info',
    '/usr/local/lib',
    '/usr/local/lib64',
    '/usr/local/man',
    '/usr/local/man/man1',
    '/usr/local/man/man2',
    '/usr/local/man/man3',
    '/usr/local/man/man4',
    '/usr/local/man/man5',
    '/usr/local/man/man6',
    '/usr/local/man/man7',
    '/usr/local/man/man8',
    '/usr/local/man/man9',
    '/usr/local/man/mann',
    '/usr/local/sbin',
    '/usr/local/src',
    '/usr/sbin',
    '/usr/share',
    '/usr/share/dict',
    '/usr/share/icons',
    '/usr/share/doc',
    '/usr/share/info',
    '/usr/share/man',
    '/usr/share/man/man1',
    '/usr/share/man/man2',
    '/usr/share/man/man3',
    '/usr/share/man/man4',
    '/usr/share/man/man5',
    '/usr/share/man/man6',
    '/usr/share/man/man7',
    '/usr/share/man/man8',
    '/usr/share/man/man9',
    '/usr/share/man/mann',
    '/usr/share/misc',
    '/usr/src',
    '/usr/tmp',
    '/var',
    '/var/cache',
    '/var/db',
    '/var/lib',
    '/var/lib/games',
    '/var/lib/misc',
    '/var/lib/rpm',
    '/var/local',
    '/var/lock',
    '/var/lock/subsys',
    '/var/log',
    '/var/mail',
    '/var/nis',
    '/var/opt',
    '/var/preserve',
    '/var/run',
    '/var/spool',
    '/var/spool/mail',
    '/var/tmp',
    '/etc/profile.d'
    )

DEFAULT_GAMES_GROUPS='Games'

DEFAULT_DANGLING_EXCEPTIONS = (['consolehelper$', 'usermode-consoleonly'],
                               )

tmp_regex=re.compile('^/tmp/|^(/var|/usr)/tmp/')
mnt_regex=re.compile('^/mnt/')
opt_regex=re.compile('^/opt/')
home_regex=re.compile('^/home/')
etc_regex=re.compile('^/etc/')
usr_local_regex=re.compile('^/usr/local/')
var_local_regex=re.compile('^/var/local/')
sub_bin_regex=re.compile('^(/usr)?/s?bin/\S+/')
backup_regex=re.compile('~$|\#[^/]+\#$')
compr_regex=re.compile('\.(gz|z|Z|zip|bz2)$')
absolute_regex=re.compile('^/([^/]+)')
absolute2_regex=re.compile('^/?([^/]+)')
points_regex=re.compile('^../(.*)')
doc_regex=re.compile('^/usr/(doc|man|info)|^/usr/share/(doc|man|info)')
bin_regex=re.compile('^(/usr)?/s?bin/')
includefile_regex=re.compile('\.(c|h|a|cmi)$')
buildconfigfile_regex=re.compile('(\.pc|-config)$')
sofile_regex=re.compile('/lib(64)?/[^/]+\.so$')
devel_regex=re.compile('-(devel|source)$')
lib_regex=re.compile('lib(64)?/lib[^/]*\.so\..*')
ldconfig_regex=re.compile('^[^#]*ldconfig', re.MULTILINE)
depmod_regex=re.compile('^[^#]*depmod', re.MULTILINE)
info_regex=re.compile('^/usr/share/info')
install_info_regex=re.compile('^[^#]*install-info', re.MULTILINE)
perl_temp_file=re.compile('.*perl.*(\.bs|/\.packlist|/perllocal\.pod)$')
scm_regex=re.compile('/CVS/[^/]+$|/.cvsignore$|/\.svn/|/(\.arch-ids|{arch})/')
htaccess_regex=re.compile('\.htaccess$')
games_path_regex=re.compile('/usr/(lib/)?/games')
games_group_regex=re.compile(Config.getOption('RpmGamesGroups', DEFAULT_GAMES_GROUPS))
source_regex=re.compile('(.c|.cc|.cpp|.ui)$')
dangling_exceptions=Config.getOption('DanglingSymlinkExceptions', DEFAULT_DANGLING_EXCEPTIONS)
logrotate_regex=re.compile('^/etc/logrotate.d/(.*)')
module_rpms_ok=Config.getOption('KernelModuleRPMsOK', 1)
kernel_modules_regex=re.compile('^/lib/modules/(2.[23456].[0-9]+[^/]*?)/')
kernel_package_regex=re.compile('^kernel(22)?(-)?(smp|enterprise|bigmem|secure|BOOT|i686-up-4GB|p3-smp-64GB)?')
normal_zero_length_regex=re.compile('^/etc/security/console.apps/|/.nosearch$|/__init__.py$')
perl_regex=re.compile('^/usr/lib/perl5/(?:vendor_perl/)?([0-9]+\.[0-9]+)\.([0-9]+)/')
python_regex=re.compile('^/usr/lib/python([.0-9]+)/')
cross_compile_regex=re.compile(Config.getOption('CrossCompilation', '-mandriva-linux-[^/]+$'))
perl_version_trick=Config.getOption('PerlVersionTrick', 1)
log_regex=re.compile('^/var/log/[^/]+$')
lib_path_regex=re.compile('^(/usr(/X11R6)?)?/lib(64)?')
lib_package_regex=re.compile('^(lib|.+-libs)')
hidden_file_regex=re.compile('/\.[^/]*$')
mispelled_macro_regex=re.compile('%{.*}')
siteperl_perl_regex=re.compile('/site_perl/')
manifest_perl_regex=re.compile('^/usr/share/doc/perl-.*/MANIFEST(\.SKIP)?$');
shellbang_regex=re.compile('^#!\s*(\S*)')
interpreter_regex=re.compile('^/(usr/)?s?bin/[^/]+$')
script_regex=re.compile('^/((usr/)?s?bin|etc/(rc.d/init.d|profile.d|X11/xinit.d|cron.(hourly|daily|monthly|weekly)))/')

for idx in range(0, len(dangling_exceptions)):
    dangling_exceptions[idx][0]=re.compile(dangling_exceptions[idx][0])

# loosely inspired from Python Cookbook
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/173220
text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
_null_trans = string.maketrans("", "")

def istextfile(f):
    s=open(f).read(512)

    if "\0" in s:
        return 0
    
    if not s:  # Empty files are considered text
        return 1

    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    if len(t)/len(s) > 0.30:
        return 0
    return 1

class FilesCheck(AbstractCheck.AbstractCheck):

    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, 'FilesCheck')

    def check(self, pkg):
	# Check only binary package
	if pkg.isSource():
	    return

        # Check if the package is a development package
	devel_pkg=devel_regex.search(pkg.name)

	files=pkg.files()
	config_files=pkg.configFiles()
	ghost_files=pkg.ghostFiles()
	doc_files=pkg.docFiles()
        req_names=pkg.req_names()
        lib_package=lib_package_regex.search(pkg.name)
        is_kernel_package=kernel_package_regex.search(pkg.name)
        
        # report these errors only once
        perl_dep_error=0
        python_dep_error=0
        lib_file=0
        non_lib_file=0
        log_file=0
        logrotate_file=0
        
        if doc_files == [] and not (pkg.name[:3] == 'lib' and string.find(pkg.name, '-devel')):
	    yield NoDocumentation(pkg)
	    
	for f in files.keys():
	    enreg=files[f]
	    mode=enreg[0]
	    user=enreg[1]
	    group=enreg[2]
            size=enreg[4]
            
	    if mispelled_macro_regex.search(f):
		yield MispelledMacro(pkg, f)
	    if not user in Config.STANDARD_USERS:
		yield NonStandardUid(pkg, f, user)
	    if not group in Config.STANDARD_GROUPS:
		yield NonStandardGid(pkg, f, group)

            if not module_rpms_ok and kernel_modules_regex.search(f) and not is_kernel_package:
                yield KernelModulesNotInKernelPackages(pkg, f)
                
            if tmp_regex.search(f):
		yield DirOrFileInTmp(pkg, f)
	    elif mnt_regex.search(f):
		yield DirOrFileInMnt(pkg, f)
	    elif opt_regex.search(f):
		yield DirOrFileInOpt(pkg, f)
	    elif usr_local_regex.search(f):
		yield DirOrFileInUsrLocal(pkg, f)
	    elif var_local_regex.search(f):
		yield DirOrFileInVarLocal(pkg, f)
	    elif sub_bin_regex.search(f):
		yield SubdirInBin(pkg, f)
	    elif backup_regex.search(f):
		yield BackupFileInPackage(pkg, f)
            elif home_regex.search(f):
		yield DirOrFileInHome(pkg, f)
            elif scm_regex.search(f):
		yield VersionControlInternalFile(pkg, f)
            elif htaccess_regex.search(f):
		yield HtaccessFile(pkg, f)
	    elif hidden_file_regex.search(f):	
		yield HiddenFileOrDir(pkg, f)
	    elif manifest_perl_regex.search(f):
		yield ManifestInPerlModule(pkg, f)
	    elif siteperl_perl_regex.search(f):
		yield SiteperlInPerlModule(pkg, f)
            elif f == '/usr/info/dir' or f == '/usr/share/info/dir':
                yield InfoDirFile(pkg, f)

            res=logrotate_regex.search(f)
            logrotate_file=res or logrotate_file
            if res and res.group(1) != pkg.name:
                yield IncoherentLogrotateFile(pkg, f)
	    link=enreg[3]
	    if link != '':
		ext=compr_regex.search(link)
		if ext:
		    if not re.compile('\.' + ext.group(1) + '$').search(f):
			yield CompressedSymlinkWithWrongExt(pkg, f, link)

	    perm=mode & 07777

	    # bit s check
	    if stat.S_ISGID & mode or stat.S_ISUID & mode:
		# check only normal files
		if stat.S_ISREG(mode):
		    user=enreg[1]
		    group=enreg[2]
		    setuid=None
		    setgid=None
		    if stat.S_ISUID & mode:
			setuid=user
		    if stat.S_ISGID & mode:
			setgid=group
		    if setuid and setgid:
			yield SetuidGidBinary(pkg, f, setuid, setgid, oct(perm))
		    elif setuid:
			yield SetuidBinary(pkg, f, setuid, oct(perm))
		    elif setgid:
                        if not (group == 'games' and
                                (games_path_regex.search(f) or games_group_regex.search(pkg[rpm.RPMTAG_GROUP]))):
                            yield SetgidBinary(pkg, f, setgid, oct(perm))
		    elif mode & 0777 != 0755:
			yield NonStandardExecutablePerm(pkg, f, oct(perm))

            if log_regex.search(f):
                   log_file=f

            # normal file check
            if stat.S_ISREG(mode):

                if not devel_pkg:
                    if lib_path_regex.search(f):
                        lib_file=1
                    elif f not in doc_files:
                        non_lib_file=f

                if log_regex.search(f):
                    if user != 'root':
                        yield NonRootUserLogFile(pkg, f, user)
                    if group != 'root':
                        yield NonRootGroupLogFile(pkg, f, group)
                    if not f in ghost_files:
                        yield NonGhostFile(pkg, f)
                        
                if doc_regex.search(f) and not f in doc_files:
                    yield NotListedAsDocumentation(pkg, f)
                #elif cross_compile_regex.search(f):
                #    yield CrossCompileName(pkg, f)

                # check ldconfig call in %post and %postun
                if lib_regex.search(f):
                    postin=pkg[rpm.RPMTAG_POSTIN] or pkg[rpm.RPMTAG_POSTINPROG]
                    if not postin:
                        yield LibraryWithoutLdconfigPostin(pkg, f)
                    else:
                        if not ldconfig_regex.search(postin):
                            yield PostinWithoutLdconfig(pkg, f)                    
                        
                    postun=pkg[rpm.RPMTAG_POSTUN] or pkg[rpm.RPMTAG_POSTUNPROG]
                    if not postun:
                        yield LibraryWithoutLdconfigPostun(pkg, f)
                    else:
                        if not ldconfig_regex.search(postun):
                            yield PostunWithoutLdconfig(pkg, f)
                
                # check depmod call in %post and %postun
                res=not is_kernel_package and kernel_modules_regex.search(f)
                if res:
                    kernel_version=res.group(1)
                    kernel_version_regex=re.compile('depmod -a.*-F /boot/System.map-' + kernel_version + '.*' + kernel_version, re.MULTILINE | re.DOTALL)
                    postin=pkg[rpm.RPMTAG_POSTIN] or pkg[rpm.RPMTAG_POSTINPROG]
                    if not postin or not depmod_regex.search(postin):
                        yield ModuleWithoutDepmodPostin(pkg, f)
                    # check that we run depmod on the right kernel
                    else:
                        if not kernel_version_regex.search(postin):
                            yield PostinWithWrongDepmod(pkg, f)

                    postun=pkg[rpm.RPMTAG_POSTUN] or pkg[rpm.RPMTAG_POSTUNPROG]
                    if not postun or not depmod_regex.search(postun):
                        yield ModuleWithoutDepmodPostun(pkg, f)
                    # check that we run depmod on the right kernel
                    else:
                        if not kernel_version_regex.search(postun):
                            yield PostunWithWrongDepmod(pkg, f)
                
                # check install-info call in %post and %postun
                if info_regex.search(f):
                    postin=pkg[rpm.RPMTAG_POSTIN]
                    if not postin:
                        yield InfoFilesWithoutInstallInfoPostin(pkg, f)
                    else:
                        if not install_info_regex.search(postin):
                            yield PostinWithoutInstallInfo(pkg, f)                    
                        
                    postun=pkg[rpm.RPMTAG_POSTUN]
                    preun=pkg[rpm.RPMTAG_PREUN]
                    if not postun and not preun:
                        yield InfoFilesWithoutInstallInfoPostun(pkg, f)
                    else:
                        if (not postun or not install_info_regex.search(postun)) and \
                           (not preun or not install_info_regex.search(preun)):
                            yield PostinWithoutInstallInfo(pkg, f)
    
               
                # check perl temp file
                if perl_temp_file.search(f):
                    yield PerlTempFile(pkg, f)

                if bin_regex.search(f) and mode & 0111 == 0:
                    yield NonExecutableInBin(pkg, f, oct(perm))
                if not devel_pkg and (includefile_regex.search(f) or buildconfigfile_regex.search(f)) and not f in doc_files:
                    yield DevelFileInNonDevelPackage(pkg, f)
                if mode & 0444 != 0444 and perm & 07000 == 0 and f[0:len('/var/log')] != '/var/log':
                    yield NonReadable(pkg, f, oct(perm))
                if size == 0 and not normal_zero_length_regex.search(f) and f not in ghost_files:
                    yield ZeroLength(pkg, f)

                if not perl_dep_error:
                    res=perl_regex.search(f)
                    if res:
                        if perl_version_trick:
                            vers = res.group(1) + '.' + res.group(2)
                        else:
                            vers = res.group(1) + res.group(2)
                        if not (pkg.check_versioned_dep('perl-base', vers) or
                                pkg.check_versioned_dep('perl', vers)):
                            yield NoDependencyOn(pkg, 'perl-base', vers)
                            perl_dep_error=1

                if not python_dep_error:
                    res=python_regex.search(f)
                    if res:
                        if not (pkg.check_versioned_dep('python-base', res.group(1)) or
                                pkg.check_versioned_dep('python', res.group(1))):
                            yield NoDependencyOn(pkg, 'python-base', res.group(1))
                            python_dep_error=1
                
                # normal executable check
		if mode & stat.S_IXUSR and perm != 0755:
		    yield NonStandardExecutablePerm(pkg, f, oct(perm))
		    
                if mode & 0111 != 0:
                    if f in config_files:
                        yield ExecutableMarkedAsConfigFile(pkg, f)
                elif etc_regex.search(f):
                    if not f in config_files and not f in ghost_files:
                        yield NonConffileInEtc(pkg, f)
                    
	    # normal dir check
            elif stat.S_ISDIR(mode):
                if perm != 0755:
                    yield NonStandardDirPerm(pkg, f, oct(perm))
                if pkg[rpm.RPMTAG_NAME] != 'filesystem':
                    if f in STANDARD_DIRS:
                        yield StandardDirOwnedByPackage(pkg, f)
		if hidden_file_regex.search(f):	
			yield HiddenFileOrDir(pkg, f)
 	

	    # symbolic link check
	    elif stat.S_ISLNK(mode):
		r=absolute_regex.search(link)
                is_so=sofile_regex.search(f)
                if not devel_pkg and is_so:
                    yield DevelFileInNonDevelPackage(pkg, f)
		# absolute link
		if r:
                    if (not is_so) and link not in files.keys():
                        is_exception=0
                        for e in dangling_exceptions:
                            if e[0].search(link):
                                is_exception=e[1]
                                break
                        if is_exception:
                            if is_exception not in req_names:
                                yield NoDependencyOn(pkg, is_exception)
                        else:
                            yield DanglingSymlink(pkg, f, link)
		    linktop=r.group(1)
		    r=absolute_regex.search(f)
		    if r:
			filetop=r.group(1)
			if filetop == linktop:
			    # absolute links within one toplevel directory are _not_ ok!
			    yield SymlinkShouldBeRelative(pkg, f, link)
		# relative link
		else:
                    if not is_so:
                        file = '%s%s/%s' % (pkg.dirName(), os.path.dirname(f), link)
                        file = os.path.normpath(file)
                        pkgfile = '%s/%s' % (os.path.dirname(f), link)
                        pkgfile = os.path.normpath(pkgfile)
                        if not (files.has_key(pkgfile) or os.path.exists(file)):
                            is_exception=0
                            for e in dangling_exceptions:
                                if e[0].search(link):
                                    is_exception=e[1]
                                    break
                            if is_exception:
                                if not is_exception in map(lambda x: x[0], pkg.requires() + pkg.prereq()):
                                    yield NoDependencyOn(pkg, is_exception)
                            else:
                                yield DanglingRelativeSymlink(pkg, f, link)
		    pathcomponents=string.split(f, '/')[1:]
		    r=points_regex.search(link)
		    lastpop=None
		    mylink=None
		    
		    while r:
			mylink=r.group(1)
			if len(pathcomponents) == 0:
			    yield SymlinkHasTooManyUpSegments(pkg, f, link)
			    break
			else:
			    lastpop=pathcomponents[0]
			    pathcomponents=pathcomponents[1:]
			    r=points_regex.search(mylink)

		    if mylink and lastpop:
			r=absolute2_regex.search(mylink)
			linktop=r.group(1)
			
			# does the link go up and then down into the same directory?
			#if linktop == lastpop:
			#    yield LengthySymlink(pkg, f, link)
		    
			if len(pathcomponents) == 0:
			    # we've reached the root directory
			    if linktop != lastpop:
				# relative link into other toplevel directory
				yield SymlinkShouldBeAbsolute(pkg, f, link)
			# check additional segments for mistakes like `foo/../bar/'
			for linksegment in string.split(mylink, '/'):
			    if linksegment == '..':
				yield SymlinkContainsUpAndDownSegments(pkg, f, link)

	    # check text file
	    if stat.S_ISREG(mode):
		path=pkg.dirName() + '/' + f
		if os.access(path, os.R_OK) and istextfile(path):
		    line=open(path).readline();

		    res=shellbang_regex.search(line)
		    if res or mode & 0111 != 0 or script_regex.search(f):
			if res:
			    if not interpreter_regex.search(res.group(1)):
				yield WrongScriptInterpreter(pkg, f, '"' + res.group(1) + '"')
			else:
			    yield ScriptWithoutShellbang(pkg, f)
		    
			if mode & 0111 == 0:
			    yield NonExecutableScript(pkg, f, oct(perm))
			if line.endswith('\r\n'):
			    yield WrongScriptEndOfLineEncoding(pkg, f)

		    elif doc_regex.search(f):
			if line.endswith('\r\n'):
			    yield WrongFileEndOfLineEncoding(pkg, f)

        if log_file and not logrotate_file:
            yield LogFilesWithoutLogrotate(pkg, log_file)

        if lib_package and lib_file and non_lib_file:
            yield OutsideLibdirFiles(pkg, non_lib_file)
            
# Create an object to enable the auto registration of the test
check=FilesCheck()



def init(checkcontext):
	checkcontext.installCheck(FilesCheck)
		

# FilesCheck.py ends here
