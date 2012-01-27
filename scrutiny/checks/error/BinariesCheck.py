#------------------------------------------------------------------------------
# File					: BinariesCheck.py
# Package  		     	: scrutiny
# Original Author		: Frederic Lepied
# Purpose				: check binary files in a binary rpm package.
#------------------------------------------------------------------------------

from scrutiny.notice import Error, Warning

from Filter import *
import AbstractCheck
import rpm
import re
import commands
import string
import sys
import Config
import Pkg
import stat

DEFAULT_SYSTEM_LIB_PATHS=('/lib', '/usr/lib', '/usr/X11R6/lib',
                          '/lib64', '/usr/lib64', '/usr/X11R6/lib64')

path_regex=re.compile('(.*/)([^/]+)')
numeric_dir_regex=re.compile('/usr(?:/share)/man/man./(.*)\.[0-9](?:\.gz|\.bz2)')
versioned_dir_regex=re.compile('[^.][0-9]')
binary_regex=re.compile('ELF|current ar archive')
usr_share=re.compile('^/usr/share/')
etc=re.compile('^/etc/')
not_stripped=re.compile('not stripped')
unstrippable=re.compile('\.o$|\.static$')
shared_object_regex=re.compile('shared object')
executable_regex=re.compile('executable')
libc_regex=re.compile('libc\.')
ldso_soname_regex=re.compile('^ld(-linux(-ia64|)|)\.so')
so_regex=re.compile('/lib(64)?/[^/]+\.so')
validso_regex=re.compile('^lib.+(\.so\.[\.0-9]+|-[\.0-9]+\.so)$')
sparc_regex=re.compile('SPARC32PLUS|SPARC V9|UltraSPARC')
system_lib_paths=Config.getOption('SystemLibPaths', DEFAULT_SYSTEM_LIB_PATHS)
usr_lib_regex=re.compile('^/usr/lib(64)?/')
bin_regex=re.compile('^(/usr(/X11R6)?)?/s?bin/')
soversion_regex=re.compile('.*?([0-9][.0-9]*)\\.so|.*\\.so\\.([0-9][.0-9]*).*')
reference_regex=re.compile('\.la$|^/usr/lib/pkgconfig/')
usr_lib_exception_regex=re.compile(Config.getOption('UsrLibBinaryException', '^/usr/lib/(perl|python|ruby|menu|pkgconfig|lib[^/]+\.(so|l?a)$|bonobo/servers/)'))
srcname_regex=re.compile('(.*?)-[0-9]')


class InvalidDirectoryReference(Error):
    label = 'invalid-directory-reference'
    descr = 'This file contains a reference to /tmp or /home.'

class NoBinary(Error):
    label = 'no-binary'
    descr = "The package should be of the noarch architecture because it doesn't contain any binary."

class ArchDependentFileInUsrShare(Error):
    label = 'arch-dependent-file-in-usr-share'
    descr = 'This package installs an ELF binary in the /usr/share\n hierarchy, which is reserved for architecture-independent files.'

class ShlibWithNonPicCode(Error):
    label = 'shlib-with-non-pic-code'
    descr = "The listed shared libraries contain object code that was compiled\nwithout -fPIC. All object code in shared libraries should be\nrecompiled separately from the static libraries with the -fPIC option.\n\nAnother common mistake that causes this problem is linking with \n``gcc -Wl,-shared'' instead of ``gcc -shared''."

class ExecutableInLibraryPackage(Error):
    label = 'executable-in-library-package'
    descr = 'The package mixes up libraries and executables. Mixing up these\nboth types of files makes upgrades quite impossible.'

class NonVersionedFileInLibraryPackage(Error):
    label = 'non-versioned-file-in-library-package'
    descr = 'The package contains files in non versioned directories. This makes\nimpossible to have multiple major versions of the libraries installed.\nOne solution can be to change the directories which contain the files\nto subdirs of /usr/lib/<name>-<version> or /usr/share/<name>-<version>.\nAnother solution can be to include a version number in the file names\nthemselves.'

class ProgramNotLinkedAgainstLibc(Error):
    label = 'program-not-linked-against-libc'
    descr = ''

class BinaryOrShlibDefinesRpath(Error):
    label = 'binary-or-shlib-defines-rpath'
    descr = "The binary or shared library defines the `RPATH'. Usually this is a\nbad thing because it hard codes the path to search libraries and so it\nmakes difficult to move libraries around.  Most likely you will find a\nMakefile with a line like: gcc test.o -o test -Wl,--rpath."

class ArchIndependentPackageContainsBinaryOrObject(Error):
    label = 'arch-independent-package-contains-binary-or-object'
    descr = 'The package contains a binary or object file but is tagged\nArchitecture: noarch.'

class InvalidSoname(Error):
    label = 'invalid-soname'
    descr = 'The soname of the library is neither of the form lib<libname>.so.<major> or lib<libname>-<major>.so.'

class StaticallyLinkedBinary(Error):
    label = 'statically-linked-binary'
    descr = 'The package installs a statically linked binary or object file.\n\nUsually this is a bug. Otherwise, please contact\n<flepied at mandriva.com> about this so that this error gets included\nin the exception file for rpmlint. With that, rpmlint will ignore\nthis bug in the future.'

class NoLdconfigSymlink(Error):
    label = 'no-ldconfig-symlink'
    descr = 'The package should not only include the shared library itself, but\nalso the symbolic link which ldconfig would produce. (This is\nnecessary, so that the link gets removed by dpkg automatically when\nthe package gets removed.)  If the symlink is in the package, check\nthat the SONAME of the library matches the info in the shlibs\nfile.'

class OnlyNonBinaryInUsrLib(Error):
    label = 'only-non-binary-in-usr-lib'
    descr = 'There are only non binary files in /usr/lib so they should be in /usr/share.'

class BinaryInEtc(Error):
    label = 'binary-in-etc'
    descr = 'This package installs an ELF binary in /etc.  Both the\nFHS and the FSSTND forbid this.'

class LibraryNotLinkedAgainstLibc(Error):
    label = 'library-not-linked-against-libc'
    descr = ''

class InvalidLdconfigSymlink(Error):
    label = 'invalid-ldconfig-symlink'
    descr = 'The symbolic link references the wrong file. It should reference\nthe shared library.'

class IncoherentVersionInName(Error):
    label = 'incoherent-version-in-name'
    descr = 'The package name should contain the major version of the library.'

class SharedLibWithoutDependencyInformation(Error):
    label = 'shared-lib-without-dependency-information'
    descr = ''

class UnstrippedBinaryOrObject(Warning):
    label = 'unstripped-binary-or-object'
    descr = ''

class LaFileWithInvalidDirReference(Warning):
    label = 'la-file-with-invalid-dir-reference'
    descr = 'The .la file contains a reference to /tmp or /home.'

class NonSparc32Binary(Warning):
    label = 'non-sparc32-binary'
    descr = ''
class NoSoname(Warning):
    label = 'no-soname'
    descr = ''

class BinaryInfo:

    needed_regex=re.compile('^\s*NEEDED\s*(\S+)')
    rpath_regex=re.compile('^\s*RPATH\s*(\S+)')
    soname_regex=re.compile('^\s*SONAME\s*(\S+)')
    comment_regex=re.compile('^\s*\d+\s+\.comment\s+')
    dynsyms_regex=re.compile('^DYNAMIC SYMBOL TABLE:')
    unrecognized_regex=re.compile('^objdump: (.*?): File format not recognized$')
    pic_regex=re.compile('^\s+\d+\s+\.rela?\.(data|text)')
    non_pic_regex=re.compile('TEXTREL', re.MULTILINE)
    
    def __init__(self, path, file):
	self.needed=[]
	self.rpath=[]
	self.comment=0
	self.dynsyms=0
	self.soname=0
        self.non_pic=1
        
	res=commands.getoutput('objdump --headers --private-headers -T ' + path)
	if res:
	    for l in string.split(res, '\n'):
		needed=BinaryInfo.needed_regex.search(l)
		if needed:
		    self.needed.append(needed.group(1))
		else:
		    rpath=BinaryInfo.rpath_regex.search(l)
		    if rpath:
                        for p in string.split(rpath.group(1), ':'):
                            self.rpath.append(p)
		    elif BinaryInfo.comment_regex.search(l):
			self.comment=1
		    elif BinaryInfo.dynsyms_regex.search(l):
			self.dynsyms=1
                    elif BinaryInfo.pic_regex.search(l):
                        self.non_pic=0
		    else:
			r=BinaryInfo.unrecognized_regex.search(l)
			if r:
			    sys.stderr.write('file format not recognized for %s in %s\n' % (r.group(1), file))
			    #sys.exit(1)
		    r=BinaryInfo.soname_regex.search(l)
                    if r:
			self.soname=r.group(1)
            if self.non_pic:
                self.non_pic=BinaryInfo.non_pic_regex.search(res)

def dir_base(path):
    res=path_regex.search(path)
    if res:
        return res.group(1), res.group(2)
    else:
        return '', path
    
class BinariesCheck(AbstractCheck.AbstractCheck):
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, 'BinariesCheck')

    def check(self, pkg):
	# Check only binary package
	if pkg.isSource():
	    return
	
        info=pkg.getFilesInfo()
	arch=pkg[rpm.RPMTAG_ARCH]
        files=pkg.files()
        exec_files=[]
        has_lib=[]
        version=None
        binary=0
        binary_in_usr_lib=0
        has_usr_lib_file=0

        res=srcname_regex.search(pkg[rpm.RPMTAG_SOURCERPM])
        if res:
            multi_pkg=(pkg.name != res.group(1))
        else:
            multi_pkg=0

        for f in files.keys():
            if usr_lib_regex.search(f) and not usr_lib_exception_regex.search(f) and not stat.S_ISDIR(files[f][0]):
                has_usr_lib_file=f
                break
            
	for i in info:
	    is_binary=binary_regex.search(i[1])
            
	    if is_binary:
                binary=binary+1
                if has_usr_lib_file and not binary_in_usr_lib and usr_lib_regex.search(i[0]):
                    binary_in_usr_lib=1
                    
		if arch == 'noarch':
		    yield ArchIndependentPackageContainsBinaryOrObject(pkg, i[0])
		else:
		    # in /usr/share ?
		    if usr_share.search(i[0]):
			yield ArchDependentFileInUsrShare(pkg, i[0])
		    # in /etc ?
		    if etc.search(i[0]):
			yield BinaryInEtc(pkg, i[0])

                    if arch == 'sparc' and sparc_regex.search(i[1]):
                        yield NonSparc32Binary(pkg, i[0])

		    # stripped ?
		    if not unstrippable.search(i[0]):
			if not_stripped.search(i[1]):
			    yield UnstrippedBinaryOrObject(pkg, i[0])

			# inspect binary file
			bin_info=BinaryInfo(pkg.dirName()+i[0], i[0])

                        # so name in library
                        if so_regex.search(i[0]):
                            has_lib.append(i[0])
                            if not bin_info.soname:
                                yield NoSoname(pkg, i[0])
                            else:
                                if not validso_regex.search(bin_info.soname):
                                    yield InvalidSoname(pkg, i[0], bin_info.soname)
                                else:
                                    (dir, base) = dir_base(i[0])
                                    try:
                                        symlink = dir + bin_info.soname
                                        (perm, owner, group, link, size, md5, mtime, rdev) = files[symlink]
                                        if link != i[0] and link != base and link != '':
                                            yield InvalidLdconfigSymlink(pkg, i[0], link)
                                    except KeyError:
                                        yield NoLdconfigSymlink(pkg, i[0])
                                res=soversion_regex.search(bin_info.soname)
                                if res:
                                    soversion=res.group(1) or res.group(2)
                                    if version == None:
                                        version = soversion
                                    elif version != soversion:
                                        version = -1
                                    
                            if bin_info.non_pic:
                                yield ShlibWithNonPicCode(pkg, i[0])
			# rpath ?
			if bin_info.rpath:
                            for p in bin_info.rpath:
                                if p in system_lib_paths or \
                                   not usr_lib_regex.search(p):
                                    yield BinaryOrShlibDefinesRpath(pkg, i[0], bin_info.rpath)
                                    break

			# statically linked ?
                        is_exec=executable_regex.search(i[1])
			if shared_object_regex.search(i[1]) or \
			   is_exec:

                            if is_exec and bin_regex.search(i[0]):
                                exec_files.append(i[0])
                                
			    if not bin_info.needed and \
                               not (bin_info.soname and \
                                    ldso_soname_regex.search(bin_info.soname)):
				if shared_object_regex.search(i[1]):
				    yield SharedLibWithoutDependencyInformation(pkg, i[0])
				else:
				    yield StaticallyLinkedBinary(pkg, i[0])
			    else:
				# linked against libc ?
				if not libc_regex.search(i[0]) and \
				   ( not bin_info.soname or \
				     ( not libc_regex.search(bin_info.soname) and \
				       not ldso_soname_regex.search(bin_info.soname))):
				    found_libc=0
				    for lib in bin_info.needed:
					if libc_regex.search(lib):
					    found_libc=1
					    break
				    if not found_libc:
					if shared_object_regex.search(i[1]):
					    yield LibraryNotLinkedAgainstLibc(pkg, i[0])
					else:
					    yield ProgramNotLinkedAgainstLibc(pkg, i[0])
            else:
                if reference_regex.search(i[0]):
                    if Pkg.grep('tmp|home', pkg.dirname + '/' + i[0]):
                        yield InvalidDirectoryReference(pkg, i[0])

        if has_lib != []:
            if exec_files != []:
                for f in exec_files:
                    yield ExecutableInLibraryPackage(pkg, f)
            for f in files.keys():
                res=numeric_dir_regex.search(f)
                fn=res and res.group(1) or f
                if not f in exec_files and not so_regex.search(f) and not versioned_dir_regex.search(fn):
                    yield NonVersionedFileInLibraryPackage(pkg, f)
            if version and version != -1 and string.find(pkg.name, version) == -1:
                yield IncoherentVersionInName(pkg, version)

        if arch != 'noarch' and not multi_pkg:
            if binary == 0:
                yield NoBinary(pkg)

        if has_usr_lib_file and not binary_in_usr_lib:
            yield OnlyNonBinaryInUsrLib(pkg)
        
# Create an object to enable the auto registration of the test
check=BinariesCheck()


def init(context):
	context.installCheck(BinariesCheck)

