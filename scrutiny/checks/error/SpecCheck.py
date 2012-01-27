
from scrutiny.notice import Error, Warning

class LibPackageWithoutMklibname(Error):
    label = 'lib-package-without-mklibname'
    descr = 'The package name must be built using %mklibname to allow lib64 and lib32\ncoexistence.'

class InvalidSpecName(Error):
    label = 'invalid-spec-name'
    descr = "Your spec file must finish with '.spec'. If it's not the case, rename your\nfile and rebuild your package."

class UseOfRpm_source_dir(Warning):
    label = 'use-of-RPM_SOURCE_DIR'
    descr = 'You use RPM_SOURCE_DIR or %{_sourcedir} in your spec file. If you have to\nuse a directory for building, use RPM_BUILD_ROOT instead.'

class PatchNotApplied(Warning):
    label = 'patch-not-applied'
    descr = "A patch is included in your package but was not applied. Refer to the patches\ndocumentation to see what's wrong."

class HardcodedLibraryPath(Error):
    label = 'hardcoded-library-path'
    descr = 'A library path is hardcoded to one of the following paths: /lib,\n/usr/lib. It should be replaced by something like /%{_lib} or %{_libdir}.'

class ObsoleteTag(Warning):
    label = 'obsolete-tag'
    descr = 'The following tags are obsolete: Copyright and Serial. They must\nbe replaced by License and Epoch respectively.'

class NoCleanSection(Warning):
    label = 'no-clean-section'
    descr = "The spec file doesn't contain a %clean section to remove the files installed\nby the %install section."

class NoBuildrootTag(Error):
    label = 'no-buildroot-tag'
    descr = "The BuildRoot tag isn't used in your spec. It must be used to\nallow build as non root."

class HardcodedPrefixTag(Warning):
    label = 'hardcoded-prefix-tag'
    descr = 'The Prefix tag is hardcoded in your spec file. It should be removed, so as to allow package relocation.'

class HardcodedPathInBuildrootTag(Warning):
    label = 'hardcoded-path-in-buildroot-tag'
    descr = 'A path is hardcoded in your Buildroot tag. It should be replaced\nby something like %{_tmppath}/%name-root.'

class IfarchAppliedPatch(Warning):
    label = 'ifarch-applied-patch'
    descr = 'A patch is applied inside an %ifarch block. Patches must be applied\non all architectures and may contain necessary configure and/or code\npatch to be effective only on a given arch.'

class HardcodedPackagerTag(Warning):
    label = 'hardcoded-packager-tag'
    descr = "The Packager tag is hardcoded in your spec file. It should be removed, so as to use rebuilder's own defaults."

class RedundantPrefixTag(Warning):
    label = 'redundant-prefix-tag'
    descr = 'The Prefix tag is uselessly defined as %{_prefix} in your spec file. It should be removed, as it is redundant with rpm defaults.'

class PrereqUse(Error):
    label = 'prereq-use'
    descr = 'The use of PreReq is deprecated. You should use Requires(pre), Requires(post),\nRequires(preun) or Requires(postun) according to your needs.'

class NoSpecFile(Error):
    label = 'no-spec-file'
    descr = 'No spec file was specified in your RPM building. Please specify a valid\nSPEC file to build a valid RPM package.'

class ConfigureWithoutLibdirSpec(Error):
    label = 'configure-without-libdir-spec'
    descr = 'A configure script is run without specifying the libdir. Configure\noptions must be augmented with something like libdir=%{_libdir}.'

#############################################################################
# File		: SpecCheck.py
# Package	: rpmlint
# Author	: Frederic Lepied
# Created on	: Thu Oct  7 17:06:14 1999
# Version	: $Id: SpecCheck.py,v 1.29 2005/08/10 06:10:39 flepied Exp $
# Purpose	: check the spec file of a source rpm.
#############################################################################

from Filter import *
import AbstractCheck
import re
import sys
import rpm
import string
import Config

# Don't check for hardcoded library paths in biarch packages
DEFAULT_BIARCH_PACKAGES='^(gcc|glibc)'

# Don't check for hardcoded library paths in packages which can have
# their noarch files in /usr/lib/<package>/*, or packages that can't
# be installed on biarch systems
DEFAULT_HARDCODED_LIB_PATH_EXCEPTIONS='/lib/(modules|cpp|perl5|rpm|hotplug)($|[\s/,])'

spec_regex=re.compile(".spec$")
patch_regex=re.compile("^\s*Patch(.*?)\s*:\s*([^\s]+)")
applied_patch_regex=re.compile("^\s*%patch.*-P\s*([^\s]*)|^\s*%patch([^\s]*)\s")
source_dir_regex=re.compile("^[^#]*(\$RPM_SOURCE_DIR|%{?_sourcedir}?)")
obsolete_tags_regex=re.compile("^(Copyright|Serial)\s*:\s*([^\s]+)")
buildroot_regex=re.compile('Buildroot\s*:\s*([^\s]+)', re.IGNORECASE)
prefix_regex=re.compile('^Prefix\s*:\s*([^\s]+)', re.IGNORECASE)
packager_regex=re.compile('^Packager\s*:\s*([^\s]+)', re.IGNORECASE)
tmp_regex=re.compile('^/')
clean_regex=re.compile('^%clean')
changelog_regex=re.compile('^%changelog')
configure_start_regex=re.compile('\./configure')
configure_libdir_spec_regex=re.compile('ln |\./configure[^#]*--libdir=([^\s]+)[^#]*')
lib_package_regex=re.compile('^%package.*\Wlib')
mklibname_regex=re.compile('%mklibname')
ifarch_regex=re.compile('%ifn?arch')
if_regex=re.compile('%if\s+')
endif_regex=re.compile('%endif')
biarch_package_regex=re.compile(DEFAULT_BIARCH_PACKAGES)
hardcoded_lib_path_exceptions_regex=re.compile(Config.getOption('HardcodedLibPathExceptions', DEFAULT_HARDCODED_LIB_PATH_EXCEPTIONS))
prereq_regex=re.compile('^PreReq:\s*(.+?)\s*$', re.IGNORECASE)

# Only check for /lib, /usr/lib, /usr/X11R6/lib
# TODO: better handling of X libraries and modules.
hardcoded_library_paths='(/lib|/usr/lib|/usr/X11R6/lib/(?!([^/]+/)+)[^/]*\\.([oa]|la|so[0-9.]*))'
hardcoded_library_path_regex=re.compile('^[^#]*((^|\s+|\.\./\.\.|\${?RPM_BUILD_ROOT}?|%{?buildroot}?|%{?_prefix}?)' + hardcoded_library_paths + '(?=[\s;/])([^\s,;]*))')

def file2string(file):
    fd=open(file, "r")
    content=fd.readlines()
    fd.close()
    return content
    
class SpecCheck(AbstractCheck.AbstractCheck):
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, "SpecCheck")

    def check(self, pkg):
        if not pkg.isSource():
            return

        # lookup spec file
        files=pkg.files()
	spec_file=None
	for f in files.keys():
	    if spec_regex.search(f):
                spec_file=pkg.dirName() + "/" + f
                break
        if not spec_file:
            yield NoSpecFile(pkg)
        else:
            if f != pkg[rpm.RPMTAG_NAME] + ".spec":
                yield InvalidSpecName(pkg, f)
                
            # check content of spec file
            spec=file2string(spec_file)
            patches={}
            applied_patches=[]
            applied_patches_ifarch=[]
            source_dir=None
            buildroot=0
            clean=0
            changelog=0
            configure=0
            configure_cmdline=""
            mklibname=0
            lib=0
            if_depth=0
            ifarch_depth=-1
            
            # gather info from spec lines
            for line in spec:

                # I assume that the changelog section is at the end of the spec
                # to avoid wrong warnings
                res=changelog_regex.search(line)
                if res:
                    changelog=1
                    break

                res=ifarch_regex.search(line)
                if res:
                    if_depth = if_depth + 1
                    ifarch_depth = if_depth
                res=if_regex.search(line)
                if res:
                    if_depth = if_depth + 1
                res=endif_regex.search(line)
                if res:
                    if ifarch_depth == if_depth:
                        ifarch_depth = -1
                    if_depth = if_depth - 1
                
                res=patch_regex.search(line)
                if res:
                    patches[res.group(1)]=res.group(2)
                else:
                    res=applied_patch_regex.search(line)
                    if res:
                        applied_patches.append(res.group(1) or res.group(2))
                        if ifarch_depth > 0:
                            applied_patches_ifarch.append(res.group(1))
                    elif not source_dir:
                        res=source_dir_regex.search(line)
                        if res:
                            source_dir=1
                            yield UseOfRpm_source_dir(pkg)
                            
                res=obsolete_tags_regex.search(line)
                if res:
                    yield ObsoleteTag(pkg, res.group(1))
				
                if configure:
                    if configure_cmdline[-1] == "\\":
                        configure_cmdline=configure_cmdline[:-1] + string.strip(line)
                    else:
                        configure=0
                        res=configure_libdir_spec_regex.search(configure_cmdline)
                        if not res:
                            yield ConfigureWithoutLibdirSpec(pkg)
                        elif res.group(1):
                            res=re.match(hardcoded_library_paths, res.group(1))
                            if res:
                                yield HardcodedLibraryPath(pkg, res.group(1), "in configure options")
                
                res=configure_start_regex.search(line)
                if not changelog and res:
                    configure=1
                    configure_cmdline=string.strip(line)
                
                res=hardcoded_library_path_regex.search(line)
                if not changelog and res and not (biarch_package_regex.match(pkg[rpm.RPMTAG_NAME]) or hardcoded_lib_path_exceptions_regex.search(string.lstrip(res.group(1)))):
                    yield HardcodedLibraryPath(pkg, "in", string.lstrip(res.group(1)))
                
                res=buildroot_regex.search(line)
                if res:
                    buildroot=1
                    if tmp_regex.search(res.group(1)):
                        yield HardcodedPathInBuildrootTag(pkg, res.group(1))

		res=packager_regex.search(line)
                if res:
                        yield HardcodedPackagerTag(pkg, res.group(1))
		res=prefix_regex.search(line)
                if res:
                    if res.group(1) == '%{_prefix}':
                        yield RedundantPrefixTag(pkg)
		    else:
                        yield HardcodedPrefixTag(pkg, res.group(1))

                if not clean and clean_regex.search(line):
                    clean=1

                if mklibname_regex.search(line):
                    mklibname=1

                if lib_package_regex.search(line):
                    lib=1

                res=prereq_regex.search(line)
                if res:
                    yield PrereqUse(pkg, res.group(1))
                    
            if not buildroot:
                yield NoBuildrootTag(pkg)

            if not clean:
                yield printError(pkg, 'no-%clean-section')

            if lib and not mklibname:
                yield LibPackageWithoutMklibname(pkg)
                
            # process gathered info
            for p in patches.keys():
                if p in applied_patches_ifarch:
                    yield IfarchAppliedPatch(pkg, "Patch" + p + ":", patches[p])
                if p not in applied_patches:
                    if p == "" and "0" in applied_patches:
                        continue
                    if p == "0" and "" in applied_patches:
                        continue
                    yield PatchNotApplied(pkg, "Patch" + p + ":", patches[p])

# Create an object to enable the auto registration of the test
check=SpecCheck()


def init(context):
	context.installCheck(SpecCheck)

# SpecCheck.py ends here
