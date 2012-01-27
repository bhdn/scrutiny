#------------------------------------------------------------------------------
# File            : MenuCheck.py
# Package       	: scrutiny
# Original Author	: Frederic Lepied
# Purpose       	: Check old style menus
#------------------------------------------------------------------------------

from scrutiny.notice import Error, Warning

from Filter import *
import AbstractCheck
import rpm
import re
import commands
import string
import sys
import stat
import Pkg

DEFAULT_VALID_SECTIONS=(
    'Office/Accessories',
    'Office/Address Books',
    'Office/Communications/Fax',
    'Office/Communications/PDA',
    'Office/Communications/Phone',
    'Office/Communications/Other',
    'Office/Drawing',
    'Office/Graphs',
    'Office/Presentations',
    'Office/Publishing',
    'Office/Spreadsheets',
    'Office/Tasks Management',
    'Office/Time Management',
    'Office/Wordprocessors',
    'Office/Other',
    'Internet/Chat',
    'Internet/File Transfer',
    'Internet/Instant Messaging',
    'Internet/Mail',
    'Internet/News',
    'Internet/Remote Access',
    'Internet/Video Conference',
    'Internet/Web Browsers',
    'Internet/Web Editors',
    'Internet/Other',
    'Multimedia/Graphics',
    'Multimedia/Sound',
    'Multimedia/Video',
    'Multimedia/Other',
    'System/Archiving/Backup',
    'System/Archiving/CD Burning',
    'System/Archiving/Compression',
    'System/Archiving/Other',
    'System/Configuration/Boot and Init',
    'System/Configuration/GNOME',
    'System/Configuration/Hardware',
    'System/Configuration/KDE',
    'System/Configuration/Networking',
    'System/Configuration/Packaging',
    'System/Configuration/Printing',
    'System/Configuration/Users',
    'System/Configuration/Other',
    'System/File Tools',
    'System/Monitoring',
    'System/Session/Windowmanagers',
    'System/Terminals',
    'System/Text Tools',
    'System/Other',
    'More Applications/Accessibility',
    'More Applications/Communications',
    'More Applications/Databases',
    'More Applications/Development/Code Generators',
    'More Applications/Development/Development Environments',
    'More Applications/Development/Interpreters',
    'More Applications/Development/Tools',
    'More Applications/Development/Other',
    'More Applications/Documentation',
    'More Applications/Editors',
    'More Applications/Education/Economy',
    'More Applications/Education/Geography',
    'More Applications/Education/History',
    'More Applications/Education/Languages',
    'More Applications/Education/Literature',
    'More Applications/Education/Sciences',
    'More Applications/Education/Sports',
    'More Applications/Education/Other',
    'More Applications/Emulators',
    'More Applications/Finances',
    'More Applications/Games/Adventure',
    'More Applications/Games/Arcade',
    'More Applications/Games/Boards',
    'More Applications/Games/Cards',
    'More Applications/Games/Puzzles',
    'More Applications/Games/Sports',
    'More Applications/Games/Strategy',
    'More Applications/Games/Toys',
    'More Applications/Games/Other',
    'More Applications/Sciences/Artificial Intelligence',
    'More Applications/Sciences/Astronomy',
    'More Applications/Sciences/Biology',
    'More Applications/Sciences/Chemistry',
    'More Applications/Sciences/Computer Science',
    'More Applications/Sciences/Data visualization',
    'More Applications/Sciences/Electricity',
    'More Applications/Sciences/Geosciences',
    'More Applications/Sciences/Image Processing',
    'More Applications/Sciences/Mathematics',
    'More Applications/Sciences/Numerical Analysis',
    'More Applications/Sciences/Parallel Computing',
    'More Applications/Sciences/Physics',
    'More Applications/Sciences/Robotics',
    'More Applications/Sciences/Other',
    'More Applications/Other',
    )

DEFAULT_EXTRA_MENU_NEEDS = (
    'gnome',
    'icewm',
    'kde',
    'wmaker',
    )

DEFAULT_ICON_PATH = (('/usr/share/icons/', 'normal'),
                     ('/usr/share/icons/mini/', 'mini'),
                     ('/usr/share/icons/large/', 'large'))


menu_file_regex=re.compile('^/usr/lib/menu/([^/]+)$')
old_menu_file_regex=re.compile('^/usr/share/(gnome/apps|applnk)/([^/]+)$')
package_regex=re.compile('\?package\((.*)\):')
needs_regex=re.compile('needs=(\"([^\"]+)\"|([^ \t\"]+))')
section_regex=re.compile('section=(\"([^\"]+)\"|([^ \t\"]+))')
title_regex=re.compile('[\"\s]title=(\"([^\"]+)\"|([^ \t\"]+))')
longtitle_regex=re.compile('longtitle=(\"([^\"]+)\"|([^ \t\"]+))')
command_regex=re.compile('command=(?:\"([^\"]+)\"|([^ \t\"]+))')
kdesu_command_regex=re.compile('[/usr/bin/]?kdesu -c \"?([^ \t\"]+)\"?')
kdesu_bin_regex=re.compile('[/usr/bin/]?kdesu')
icon_regex=re.compile('icon=\"?([^\" ]+)')
valid_sections=Config.getOption('ValidMenuSections', DEFAULT_VALID_SECTIONS)
update_menus_regex=re.compile('^[^#]*update-menus',re.MULTILINE)
standard_needs=Config.getOption('ExtraMenuNeeds', DEFAULT_EXTRA_MENU_NEEDS)
icon_paths=Config.getOption('IconPath', DEFAULT_ICON_PATH)
xpm_ext_regex=re.compile('/usr/share/icons/(mini/|large/).*\.xpm$')
icon_ext_regex=re.compile(Config.getOption('IconFilename', '.*\.png$'))
capital_regex=re.compile('[0-9A-Z]')
version_regex=re.compile('([0-9.][0-9.]+)($|\s)')
launchers=Config.getOption('MenuLaunchers', Config.DEFAULT_LAUNCHERS)
bad_title_regex=re.compile('/')

# compile regexps
for l in launchers:
    l[0]=re.compile(l[0])
 
class PostunWithoutUpdateMenus(Error):
    label = 'postun-without-update-menus'
    descr = "A menu file exists in the package but the %postun doesn't call update-menus."

class NonReadableMenuFile(Error):
    label = 'non-readable-menu-file'
    descr = "The menu file isn't readable. Check the permissions."

class NoTitleInMenu(Error):
    label = 'no-title-in-menu'
    descr = "The title field isn't present in the menu entry."

class MenuWithoutPostun(Error):
    label = 'menu-without-postun'
    descr = 'A menu file exists in the package but no %postun is present to call\nupdate-menus.'

class UseOfLauncherInMenuButNoRequiresOn(Error):
    label = 'use-of-launcher-in-menu-but-no-requires-on'
    descr = 'The menu command uses a launcher but there is no require on the package\nthat contains it.'

class InvalidMenuSection(Error):
    label = 'invalid-menu-section'
    descr = "The section field of the menu entry isn't standard."

class OldMenuEntry(Error):
    label = 'old-menu-entry'

class InvalidTitle(Error):
    label = 'invalid-title'
    descr = 'The menu title contains invalid characters like /.'

class ExecutableMenuFile(Error):
    label = 'executable-menu-file'
    descr = ''

class MenuWithoutPostin(Error):
    label = 'menu-without-postin'
    descr = 'A menu file exists in the package but no %post is present to call\nupdate-menus.'

class PostinWithoutUpdateMenus(Error):
    label = 'postin-without-update-menus'
    descr = "A menu file exists in the package but the %post doesn't call update-menus."

class NonFileInMenuDir(Error):
    label = 'non-file-in-menu-dir'
    descr = '/usr/lib/menu must not contain something else than normal files.'

class IconNotInPackage(Error):
    label = 'icon-not-in-package'
    descr = 'Package must supply all sizes (normal, mini and large) for icons.'

class NoLongtitleInMenu(Error):
    label = 'no-longtitle-in-menu'
    descr = "The longtitle field isn't present in the menu entry."


class UnableToParseMenuEntry(Warning):
    label = 'unable-to-parse-menu-entry'
    descr = ''

class MenuCommandNotInPackage(Warning):
    label = 'menu-command-not-in-package'
    descr = "The command used in the menu isn't contained in the package."

class InvalidMenuIconType(Warning):
    label = 'invalid-menu-icon-type'
    descr = ''

class VersionInMenuTitle(Warning):
    label = 'version-in-menu-title'
    descr = 'A version is contained in the title field of the menu entry. This is bad because\nit will be prone to error when the version of the package changes.'

class StrangeNeeds(Warning):
    label = 'strange-needs'
    descr = ''

class NormalIconNotInPackage(Warning):
    label = 'normal-icon-not-in-package'
    descr = "The normal icon isn't present in the package."

class MenuTitleNotCapitalized(Warning):
    label = 'menu-title-not-capitalized'
    descr = "The title field of the menu entry doesn't start with a capital letter."

class LargeIconNotInPackage(Warning):
    label = 'large-icon-not-in-package'
    descr = "The large icon isn't present in the package."

class MissingMenuCommand(Warning):
    label = 'missing-menu-command'
    descr = "The menu file doesn't contain a command."

class NoIconInMenu(Warning):
    label = 'no-icon-in-menu'
    descr = "The menu entry doesn't contain an icon field."

class HardcodedPathInMenuIcon(Warning):
    label = 'hardcoded-path-in-menu-icon'
    descr = 'The path of the icon is hardcoded in the menu entry. This prevent multiple sizes\nof the icon to be found.'

class VersionInMenuLongtitle(Warning):
    label = 'version-in-menu-longtitle'
    descr = 'A version is contained in the longtitle field of the menu entry. This is bad because\nit will be prone to error when the version of the package changes.'

class NonCoherentMenuFilename(Warning):
    label = 'non-coherent-menu-filename'
    descr = 'The menu file name should be /usr/lib/menu/<package>.'

class IncoherentPackageValueInMenu(Warning):
    label = 'incoherent-package-value-in-menu'
    descr = "The package field of the menu entry isn't the same as the package name."

class MiniIconNotInPackage(Warning):
    label = 'mini-icon-not-in-package'
    descr = "The mini icon isn't present in the package."

class NonTransparentXpm(Warning):
    label = 'non-transparent-xpm'
    descr = 'xpm icon should be transparent to used in menus.'

class UnableToParseMenuSection(Warning):
    label = 'unable-to-parse-menu-section'
    descr = "rpmlint wasn't able to parse the menu section. Please report."

class MenuLongtitleNotCapitalized(Warning):
    label = 'menu-longtitle-not-capitalized'
    descr = "The longtitle field of the menu doesn't start with a capital letter."

class UnableToParseMenuNeeds(Warning):
    label = 'unable-to-parse-menu-needs'
    descr = ''

   
class MenuCheck(AbstractCheck.AbstractCheck):
    
    def __init__(self):
        AbstractCheck.AbstractCheck.__init__(self, 'MenuCheck')

    def check(self, pkg):
	# Check only binary package
	if pkg.isSource():
	    return

        files=pkg.files()
        pkgname=pkg[rpm.RPMTAG_NAME]
        menus=[]
        dirname=pkg.dirName()
        
        for f in files.keys():
            # Check menu files
            res=menu_file_regex.search(f)
            if res:
                basename=res.group(1)
                mode=files[f][0]
                if not stat.S_ISREG(mode):
                    yield NonFileInMenuDir(pkg, f)
                else:
                    if basename != pkgname:
                        yield NonCoherentMenuFilename(pkg, f)
                    if mode & 0444 != 0444:
                        yield NonReadableMenuFile(pkg, f)
                    if mode & 0111 != 0:
                        yield ExecutableMenuFile(pkg, f)
                    menus.append(f)
            else:
                # Check old menus from KDE and GNOME
                res=old_menu_file_regex.search(f)
                if res:
                    mode=files[f][0]
                    if stat.S_ISREG(mode):
                        yield OldMenuEntry(pkg, f)
                else:
                    # Check non transparent xpm files
                    res=xpm_ext_regex.search(f)
                    if res:
                        mode=files[f][0]
                        if stat.S_ISREG(mode) and not Pkg.grep('None",', dirname + '/' + f):
                            yield NonTransparentXpm(pkg, f)
        if len(menus) > 0:
            dir=pkg.dirName()
            if menus != []:
                postin=pkg[rpm.RPMTAG_POSTIN] or pkg[rpm.RPMTAG_POSTINPROG]
                if not postin:
                    yield MenuWithoutPostin(pkg)
                else:
                    if not update_menus_regex.search(postin):
                        yield PostinWithoutUpdateMenus(pkg)                    
                    
                postun=pkg[rpm.RPMTAG_POSTUN] or pkg[rpm.RPMTAG_POSTUNPROG]
                if not postun:
                    yield MenuWithoutPostun(pkg)
                else:
                    if not update_menus_regex.search(postun):
                        yield PostunWithoutUpdateMenus(pkg)

            for f in menus:
                # remove comments and handle cpp continuation lines
                str='/lib/cpp %s%s 2>/dev/null| grep ^\?' % (dir, f)
                cmd=commands.getoutput(str)
                for line in string.split(cmd, '\n'):
                    res=package_regex.search(line)
                    if res:
                        package=res.group(1)
                        if package != pkgname:
                            yield IncoherentPackageValueInMenu(pkg, package, f)
                    else:
                        yield UnableToParseMenuEntry(pkg, line)

                    command=1
                    res=command_regex.search(line)
                    if res:
                        command_line=string.split(res.group(1) or res.group(2))
                        command=command_line[0]
                        for launcher in launchers:
                            if launcher[0].search(command):
                                found=0
                                if launcher[1]:
                                    if (files.has_key('/bin/' + command_line[0]) or
                                        files.has_key('/usr/bin/' + command_line[0]) or
                                        files.has_key('/usr/X11R6/bin/' + command_line[0])):
                                        found=1
                                    else:
                                        for l in launcher[1]:
                                            if l in pkg.req_names():
                                                found=1
                                                break
                                    if not found:
                                        yield UseOfLauncherInMenuButNoRequiresOn(pkg, launcher[1][0])
                                command=command_line[1]
                                break
                        try:
                            if command[0] == '/':
                                files[command]
                            else:
                                if not (files.has_key('/bin/' + command) or
                                        files.has_key('/usr/bin/' + command) or
                                        files.has_key('/usr/X11R6/bin/' + command)):
                                    raise KeyError, command
                        except KeyError:
                            yield MenuCommandNotInPackage(pkg, command)
                    else:
                        yield MissingMenuCommand(pkg)
                        command=0

                    res=longtitle_regex.search(line)
                    if res:
                        grp=res.groups()
                        title=grp[1] or grp[2]
                        if not capital_regex.search(title[0]):
                            yield MenuLongtitleNotCapitalized(pkg, title)
                        res=version_regex.search(title)
                        if res:
                            yield VersionInMenuLongtitle(pkg, title)
                    else:
                        yield NoLongtitleInMenu(pkg, f)
                        title=None
                        
                    res=title_regex.search(line)
                    if res:
                        grp=res.groups()
                        title=grp[1] or grp[2]
                        if not capital_regex.search(title[0]):
                            yield MenuTitleNotCapitalized(pkg, title)
                        res=version_regex.search(title)
                        if res:
                            yield VersionInMenuTitle(pkg, title)
                        if bad_title_regex.search(title):
                            yield InvalidTitle(pkg, title)
                    else:
                        yield NoTitleInMenu(pkg, f)
                        title=None
                        
                    res=needs_regex.search(line)
                    if res:
                        grp=res.groups()
                        needs=string.lower(grp[1] or grp[2])
                        if needs in ('x11', 'text' ,'wm'):
                            res=section_regex.search(line)
                            if res:
                                grp=res.groups()
                                section=grp[1] or grp[2]
                                # don't warn entries for sections
                                if command:
                                    if section not in valid_sections:
                                        yield InvalidMenuSection(pkg, section, f)
                            else:
                                yield UnableToParseMenuSection(pkg, line)
                        elif needs not in standard_needs:
                            yield StrangeNeeds(pkg, needs, f)
                    else:
                        yield UnableToParseMenuNeeds(pkg, line)

                    res=icon_regex.search(line)
                    if res:
                        icon=res.group(1)
                        if not icon_ext_regex.search(icon):
                            yield InvalidMenuIconType(pkg, icon)
                        if icon[0] == '/' and needs == 'x11':
                            yield HardcodedPathInMenuIcon(pkg, icon)
                        else:
                            for path in icon_paths:
                                try:
                                    files[path[0] + icon]
                                except KeyError:
                                    yield IconNotInPackage(pkg, icon, path[1], f)
                    else:
                        yield NoIconInMenu(pkg, title)
                        
# Create an object to enable the auto registration of the test
check=MenuCheck()



def init(checkcontext):
	checkcontext.installCheck(MenuCheck)
		


# MenuCheck.py ends here
