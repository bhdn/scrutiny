#------------------------------------------------------------------------------
# File				: TagsCheck.py
# Package       	: scrutiny
# Original Author	: Frederic Lepied
# Purpose			: Check a package to see if some rpm tags are present
#------------------------------------------------------------------------------

from scrutiny.notice import Error, Warning

from Filter import *
import AbstractCheck
import rpm
import string
import re
import Config

DEFAULT_VALID_GROUPS=(
    'Accessibility',
    'Archiving/Backup',
    'Archiving/Cd burning',
    'Archiving/Compression',
    'Archiving/Other',
    'Books/Computer books',
    'Books/Faqs',
    'Books/Howtos',
    'Books/Literature',
    'Books/Other',
    'Communications',
    'Databases',
    'Development/C',
    'Development/C++',
    'Development/Databases',
    'Development/GNOME and GTK+',
    'Development/Java',
    'Development/KDE and Qt',
    'Development/Kernel',
    'Development/Other',
    'Development/Perl',
    'Development/Python',
    'Editors',
    'Education',
    'Emulators',
    'File tools',
    'Games/Adventure',
    'Games/Arcade',
    'Games/Boards',
    'Games/Cards',
    'Games/Other',
    'Games/Puzzles',
    'Games/Sports',
    'Games/Strategy',
    'Graphical desktop/Enlightenment',
    'Graphical desktop/FVWM based',
    'Graphical desktop/GNOME',
    'Graphical desktop/Icewm',
    'Graphical desktop/KDE',
    'Graphical desktop/Other',
    'Graphical desktop/Sawfish',
    'Graphical desktop/WindowMaker',
    'Graphical desktop/Xfce',
    'Graphics',
    'Monitoring',
    'Networking/Chat',
    'Networking/File transfer',
    'Networking/IRC',
    'Networking/Instant messaging',
    'Networking/Mail',
    'Networking/News',
    'Networking/Other',
    'Networking/Remote access',
    'Networking/WWW',
    'Office',
    'Publishing',
    'Sciences/Astronomy',
    'Sciences/Biology',
    'Sciences/Chemistry',
    'Sciences/Computer science',
    'Sciences/Geosciences',
    'Sciences/Mathematics',
    'Sciences/Other',
    'Sciences/Physics',
    'Shells',
    'Sound',
    'System/Base',
    'System/Configuration/Boot and Init',
    'System/Configuration/Hardware',
    'System/Configuration/Networking',
    'System/Configuration/Other',
    'System/Configuration/Packaging',
    'System/Configuration/Printing',
    'System/Fonts/Console',
    'System/Fonts/True type',
    'System/Fonts/Type1',
    'System/Fonts/X11 bitmap',
    'System/Internationalization',
    'System/Kernel and hardware',
    'System/Libraries',
    'System/Servers',
    'System/X11',
    'Terminals',
    'Text tools',
    'Toys',
    'Video',
    )

# liste grabbed from www.opensource.org/licenses

DEFAULT_VALID_LICENSES = (
    'GPL',
    'LGPL',
    'GFDL',
    'OPL',
    'Artistic',
    'BSD',
    'MIT',
    'QPL',
    'MPL',
    'IBM Public License',
    'Apache License',
    'PHP License',
    'Public Domain',
    'Modified CNRI Open Source License',
    'zlib License',
    'CVW License',
    'Ricoh Source Code Public License',
    'Python license',
    'Vovida Software License',
    'Sun Internet Standards Source License',
    'Intel Open Source License',
    'Jabber Open Source License',
    'Nokia Open Source License',
    'Sleepycat License',
    'Nethack General Public License',
    'Common Public License',
    'Apple Public Source License',
    'X.Net License',
    'Sun Public License',
    'Eiffel Forum License',
    'W3C License',
    'Zope Public License',
    'Lucent Public License',
    'Design Science License',
    'LaTeX Project Public License',
    'CECILL',
    # non open source licences:
    'Proprietary',
    'Freeware',
    'Shareware',
    'Charityware'
    )

DEFAULT_PACKAGER = '@mandriva.com|@mandriva.org|http://www.mandrivaexpert.com'

BAD_WORDS = {
    'alot': 'a lot',
    'accesnt': 'accent',
    'accelleration': 'acceleration',
    'accessable': 'accessible',
    'accomodate': 'accommodate',
    'acess': 'access',
    'acording': 'according',
    'additionaly': 'additionally',
    'adress': 'address',
    'adresses': 'addresses',
    'adviced': 'advised',
    'albumns': 'albums',
    'alegorical': 'allegorical',
    'algorith': 'algorithm',
    'allpication': 'application',
    'altough': 'although',
    'alows': 'allows',
    'amoung': 'among',
    'amout': 'amount',
    'analysator': 'analyzer',
    'ang': 'and',
    'appropiate': 'appropriate',
    'arraival': 'arrival',
    'artifical': 'artificial',
    'artillary': 'artillery',
    'attemps': 'attempts',
    'automatize': 'automate',
    'automatized': 'automated',
    'automatizes': 'automates',
    'auxilliary': 'auxiliary',
    'availavility': 'availability',
    'availble': 'available',
    'avaliable': 'available',
    'availiable': 'available',
    'backgroud': 'background',
    'baloons': 'balloons',
    'becomming': 'becoming',
    'becuase': 'because',
    'cariage': 'carriage',
    'challanges': 'challenges',
    'changable': 'changeable',
    'charachters': 'characters',
    'charcter': 'character',
    'choosen': 'chosen',
    'colorfull': 'colorful',
    'comand': 'command',
    'commerical': 'commercial',
    'comminucation': 'communication',
    'commoditiy': 'commodity',
    'compability': 'compatibility',
    'compatability': 'compatibility',
    'compatable': 'compatible',
    'compatibiliy': 'compatibility',
    'compatibilty': 'compatibility',
    'compleatly': 'completely',
    'complient': 'compliant',
    'compres': 'compress',
    'containes': 'contains',
    'containts': 'contains',
    'contence': 'contents',
    'continous': 'continuous',
    'contraints': 'constraints',
    'convertor': 'converter',
    'convinient': 'convenient',
    'cryptocraphic': 'cryptographic',
    'deamon': 'daemon',
    'debians': 'Debian\'s',
    'decompres': 'decompress',
    'definate': 'definite',
    'definately': 'definitely',
    'dependancies': 'dependencies',
    'dependancy': 'dependency',
    'dependant': 'dependent',
    'developement': 'development',
    'developped': 'developed',
    'deveolpment': 'development',
    'devided': 'divided',
    'dictionnary': 'dictionary',
    'diplay': 'display',
    'disapeared': 'disappeared',
    'dissapears': 'disappears',
    'documentaion': 'documentation',
    'docuentation': 'documentation',
    'documantation': 'documentation',
    'dont': 'don\'t',
    'easilly': 'easily',
    'ecspecially': 'especially',
    'edditable': 'editable',
    'editting': 'editing',
    'eletronic': 'electronic',
    'enchanced': 'enhanced',
    'encorporating': 'incorporating',
    'enlightnment': 'enlightenment',
    'enterily': 'entirely',
    'enviroiment': 'environment',
    'environement': 'environment',
    'excellant': 'excellent',
    'exlcude': 'exclude',
    'exprimental': 'experimental',
    'extention': 'extension',
    'failuer': 'failure',
    'familar': 'familiar',
    'fatser': 'faster',
    'fetaures': 'features',
    'forse': 'force',
    'fortan': 'fortran',
    'framwork': 'framework',
    'fuction': 'function',
    'fuctions': 'functions',
    'functionnality': 'functionality',
    'functonality': 'functionality',
    'functionaly': 'functionally',
    'futhermore': 'furthermore',
    'generiously': 'generously',
    'grahical': 'graphical',
    'grahpical': 'graphical',
    'grapic': 'graphic',
    'guage': 'gauge',
    'halfs': 'halves',
    'heirarchically': 'hierarchically',
    'helpfull': 'helpful',
    'hierachy': 'hierarchy',
    'hierarchie': 'hierarchy',
    'howver': 'however',
    'implemantation': 'implementation',
    'incomming': 'incoming',
    'incompatabilities': 'incompatibilities',
    'indended': 'intended',
    'indendation': 'indentation',
    'independant': 'independent',
    'informatiom': 'information',
    'initalize': 'initialize',
    'inofficial': 'unofficial',
    'integreated': 'integrated',
    'integrety': 'integrity',
    'integrey': 'integrity',
    'intendet': 'intended',
    'interchangable': 'interchangeable',
    'intermittant': 'intermittent',
    'jave': 'java',
    'langage': 'language',
    'langauage': 'language',
    'langugage': 'language',
    'lauch': 'launch',
    'lesstiff': 'lesstif',
    'libaries': 'libraries',
    'licenceing': 'licencing',
    'loggin': 'login',
    'logile': 'logfile',
    'loggging': 'logging',
    'maintainance': 'maintenance',
    'maintainence': 'maintenance',
    'makeing': 'making',
    'managable': 'manageable',
    'manoeuvering': 'maneuvering',
    'ment': 'meant',
    'modulues': 'modules',
    'monochromo': 'monochrome',
    'multidimensionnal': 'multidimensional',
    'navagating': 'navigating',
    'nead': 'need',
    'neccesary': 'necessary',
    'neccessary': 'necessary',
    'necesary': 'necessary',
    'nescessary': 'necessary',
    'noticable': 'noticeable',
    'optionnal': 'optional',
    'orientied': 'oriented',
    'pacakge': 'package',
    'pachage': 'package',
    'packacge': 'package',
    'packege': 'package',
    'packge': 'package',
    'pakage': 'package',
    'particularily': 'particularly',
    'persistant': 'persistent',
    'plattform': 'platform',
    'ploting': 'plotting',
    'posible': 'possible',
    'powerfull': 'powerful',
    'prefered': 'preferred',
    'prefferably': 'preferably',
    'prepaired': 'prepared',
    'princliple': 'principle',
    'priorty': 'priority',
    'proccesors': 'processors',
    'proces': 'process',
    'processsing': 'processing',
    'processessing': 'processing',
    'progams': 'programs',
    'programers': 'programmers',
    'programm': 'program',
    'programms': 'programs',
    'promps': 'prompts',
    'pronnounced': 'pronounced',
    'prononciation': 'pronunciation',
    'pronouce': 'pronounce',
    'protcol': 'protocol',
    'protocoll': 'protocol',
    'recieve': 'receive',
    'recieved': 'received',
    'redircet': 'redirect',
    'regulamentations': 'regulations',
    'remoote': 'remote',
    'repectively': 'respectively',
    'replacments': 'replacements',
    'requiere': 'require',
    'runnning': 'running',
    'safly': 'safely',
    'savable': 'saveable',
    'searchs': 'searches',
    'separatly': 'separately',
    'seperate': 'separate',
    'seperately': 'separately',
    'seperatly': 'separately',
    'serveral': 'several',
    'setts': 'sets',
    'similiar': 'similar',
    'simliar': 'similar',
    'speach': 'speech',
    'standart': 'standard',
    'staically': 'statically',
    'staticly': 'statically',
    'succesful': 'successful',
    'succesfully': 'successfully',
    'suplied': 'supplied',
    'suport': 'support',
    'suppport': 'support',
    'supportin': 'supporting',
    'synchonized': 'synchronized',
    'syncronize': 'synchronize',
    'syncronizing': 'synchronizing',
    'syncronus': 'synchronous',
    'syste': 'system',
    'sythesis': 'synthesis',
    'taht': 'that',
    'throught': 'through',
    'useable': 'usable',
    'usefull': 'useful',
    'usera': 'users',
    'usetnet': 'Usenet',
    'utilites': 'utilities',
    'utillities': 'utilities',
    'utilties': 'utilities',
    'utiltity': 'utility',
    'utitlty': 'utility',
    'variantions': 'variations',
    'varient': 'variant',
    'verson': 'version',
    'vicefersa': 'vice-versa',
    'yur': 'your',
    'wheter': 'whether',
    'wierd': 'weird',
    'xwindows': 'X'
    }
DEFAULT_FORBIDDEN_WORDS_REGEX='mandrake'
DEFAULT_VALID_BUILDHOST='\.mandriva\.com$|\.mandriva\.org$'
DEFAULT_INVALID_REQUIRES=('^is$', '^not$', '^owned$', '^by$', '^any$', '^package$', '^libsafe\.so\.')
DEFAULT_INVALID_URL='mandrake'

distribution=Config.getOption("Distribution", "Mandriva Linux")
VALID_GROUPS=Config.getOption('ValidGroups', DEFAULT_VALID_GROUPS)
VALID_LICENSES=Config.getOption('ValidLicenses', DEFAULT_VALID_LICENSES)
INVALID_REQUIRES=map(lambda x: re.compile(x), Config.getOption('InvalidRequires', DEFAULT_INVALID_REQUIRES))
packager_regex=re.compile(Config.getOption('Packager', DEFAULT_PACKAGER))
basename_regex=re.compile('/?([^/]+)$')
changelog_version_regex=re.compile('[^>]([^ >]+)\s*$')
release_ext=Config.getOption('ReleaseExtension', 'mdk')
extension_regex=release_ext and re.compile(release_ext + '$')
use_version_in_changelog=Config.getOption('UseVersionInChangelog', 1)
devel_regex=re.compile('(.*)-devel')
devel_number_regex=re.compile('(.*?)([0-9.]+)(_[0-9.]+)?-devel')
lib_devel_number_regex=re.compile('^lib(.*?)([0-9.]+)(_[0-9.]+)?-devel')
capital_regex=re.compile('[0-9A-Z]')
url_regex=re.compile('^(ftp|http|https)://')
invalid_url_regex=re.compile(Config.getOption('InvalidURL', DEFAULT_INVALID_URL), re.IGNORECASE)
so_regex=re.compile('\.so$')
lib_regex=re.compile('^lib.*?(\.so.*)?$')
leading_space_regex=re.compile('^\s+')
invalid_version_regex=re.compile('([0-9](?:rc|alpha|beta|pre).*)', re.IGNORECASE)
forbidden_words_regex=re.compile('(' + Config.getOption('ForbiddenWords', DEFAULT_FORBIDDEN_WORDS_REGEX) + ')', re.IGNORECASE)
valid_buildhost_regex=re.compile(Config.getOption('ValidBuildHost', DEFAULT_VALID_BUILDHOST))
epoch_regex=re.compile('^[0-9]+:')
use_epoch=Config.getOption('UseEpoch', 0)
requires_in_usr_local_regex=re.compile('^/usr/local/bin')


class NoGroupTag(Error):
    label = 'no-group-tag'
    descr = 'There is no Group tag in your package. You have to specify a valid group\nin your spec file using the Group tag.'

class NoDescriptionTag(Error):
    label = 'no-description-tag'
    descr = "There is no %description tag in your spec file. To insert it, just insert a '%tag' in\nyour spec file and rebuild it."

class NoSummaryTag(Error):
    label = 'no-summary-tag'
    descr = "There is no Summary tag in your package. You have to describe your package\nusing this tag. To insert it, just insert a tag 'Summary'."

class InvalidDependency(Error):
    label = 'invalid-dependency'
    descr = 'An invalid dependency has been detected. It usually means that the build of the\npackage was buggy.'

class InvalidVersion(Error):
    label = 'invalid-version'
    descr = 'The version string must not contain the pre, alpha, beta or rc suffixes because\nwhen the final version will be out, you will have to use an Epoch tag to make\nyou package upgradable. Instead put it in the release tag like 0.alpha8.1mdk.'

class NoReleaseTag(Error):
    label = 'no-release-tag'
    descr = 'There is no Release tag in your package. You have to specify a release using the\nRelease tag.'

class RequiresOnRelease(Error):
    label = 'requires-on-release'
    descr = ''

class DescriptionLineTooLong(Error):
    label = 'description-line-too-long'
    descr = 'Your description lines must no exceed 80 characters. If a line is exceeding this number,\ncut it to fit in two lines.'

class NoLicense(Error):
    label = 'no-license'
    descr = "There is no License tag in your spec file. You have to specify one license for your\nprogram (ie GPL). To insert this tag, just insert a 'License' in your file."

class ObsoleteNotProvided(Error):
    label = 'obsolete-not-provided'
    descr = 'The obsoleted package must also be provided to allow a clean upgrade\nand not to break dependencies.'

class NoVersionTag(Error):
    label = 'no-version-tag'
    descr = 'There is no Version tag in your package. You have to specify a version using the\nVersion tag.'

class SummaryTooLong(Error):
    label = 'summary-too-long'
    descr = 'The "Summary:" must not exceed 80 characters.'

class NoPackagerTag(Error):
    label = 'no-packager-tag'
    descr = 'There is no Packager tag in your package. You have to specify a packager using\nthe Packager tag. Ex: Packager: Christian Belisle <cbelisle@mandriva.com>.'


class UselessExplicitProvides(Error):
    label = 'useless-explicit-provides'
    descr = 'This package provides 2 times the same capacity. It should only provide it once.'

class NoEpochTag(Error):
    label = 'no-epoch-tag'
    descr = 'There is no Epoch tag in your package. You have to specify an epoch using the\nEpoch tag.'

class DevelDependency(Error):
    label = 'devel-dependency'
    descr = "Your package has a dependency on a devel package whereas it's not a devel package."

class NoBuildhostTag(Error):
    label = 'no-buildhost-tag'
    descr = ''

class InvalidBuildRequires(Error):
    label = 'invalid-build-requires'
    descr = 'Your source package contains a dependency not compliant with the lib64 naming.\nThis BuildRequires dependency will not be resolved on lib64 platforms (i.e. amd64).'

class ObsoleteOnName(Error):
    label = 'obsolete-on-name'
    descr = 'A package should not obsolete itself, as it can cause weird errors in tools.'

class NoChangelognameTag(Error):
    label = 'no-changelogname-tag'
    descr = "There is no %changelog tag in your spec file. To insert it, just insert a '%changelog' in\nyour spec file and rebuild it."

class SummaryOnMultipleLines(Error):
    label = 'summary-on-multiple-lines'
    descr = 'Your summary must fit on one line. Please make it shorter and rebuilt your package.'

class NoNameTag(Error):
    label = 'no-name-tag'
    descr = 'There is no Name tag in your package. You have to specify a name using the Name tag.'

class ExplicitLibDependency(Error):
    label = 'explicit-lib-dependency'
    descr = 'You must let rpm find the library dependencies by itself. Do not put unneeded\nexplicit Requires: tags.'

class SummaryHasLeadingSpaces(Error):
    label = 'summary-has-leading-spaces'
    descr = 'Summary begins with spaces and that will waste space when displayed.'

class SummaryEndedWithDot(Warning):
    label = 'summary-ended-with-dot'
    descr = 'Summary ends with a dot.'

class InvalidPackager(Warning):
    label = 'invalid-packager'
    descr = 'The packager email must finish with @mandriva.com or must be @mandriva.org.\nPlease change it and rebuild your package.'

class DescriptionUseInvalidWord(Warning):
    label = 'description-use-invalid-word'
    descr = ''

class SummaryUseInvalidWord(Warning):
    label = 'summary-use-invalid-word'
    descr = ''

class NoMajorInName(Warning):
    label = 'no-major-in-name'
    descr = "The major number of the library isn't contained in the package name.\n"

class PackageProvidesItself(Warning):
    label = 'package-provides-itself'
    descr = ''

class IncoherentVersionInChangelog(Warning):
    label = 'incoherent-version-in-changelog'
    descr = 'Your last entry in %changelog contains a version that is not coherent with the current\nversion of your package.'

class UnreasonableEpoch(Warning):
    label = 'unreasonable-epoch'
    descr = 'The value of your Epoch tag is unreasonably large (> 99).'

class SpellingErrorIn(Warning):
    label = 'spelling-error-in'
    descr = ''

class NotStandardReleaseExtension(Warning):
    label = 'not-standard-release-extension'
    descr = 'Your release number must finish with mdk and must be valid.'

class NoEpochInDependency(Warning):
    label = 'no-epoch-in-dependency'
    descr = 'Your package contains a versioned dependency without an Epoch.'

class NoProvides(Warning):
    label = 'no-provides'
    descr = "Your library package doesn't provide the -devel name without the major version\nincluded."

class InvalidBuildhost(Warning):
    label = 'invalid-buildhost'
    descr = ''

class NoDependencyOn(Warning):
    label = 'no-dependency-on'

class NoVersionInLastChangelog(Warning):
    label = 'no-version-in-last-changelog'
    descr = "The last changelog entry doesn't contain a version. Please insert the coherent version and\nrebuild your package."

class NoEpochInProvides(Warning):
    label = 'no-epoch-in-provides'
    descr = 'Your package contains a versioned Provides entry without an Epoch.'

class NonCoherentFilename(Warning):
    label = 'non-coherent-filename'
    descr = 'The file which contains the package should be named <NAME>-<VERSION>-<RELEASE>.<ARCH>.rpm.'

class NoUrlTag(Warning):
    label = 'no-url-tag'
    descr = ''

class SpellingErrorInDescription(Warning):
    label = 'spelling-error-in-description'
    descr = 'You made a misspelling in the Description. Please double-check.'

class InvalidLicense(Warning):
    label = 'invalid-license'
    descr = "The license you specified is invalid. The valid licenses are:\n\n-GPL\t\t\t\t\t-LGPL\n-Artistic\t\t\t\t-BSD\n-MIT\t\t\t\t\t-QPL\n-MPL\t\t\t\t\t-IBM Public License\n-Apache License\t\t\t\t-PHP License\n-Public Domain\t\t\t\t-Modified CNRI Open Source License\n-zlib License\t\t\t\t-CVW License\n-Ricoh Source Code Public License\t-Python license\n-Vovida Software License\t\t-Sun Internet Standards Source License\n-Intel Open Source License\t\t-Jabber Open Source License\n\nif the license is near an existing one, you can use '<license> style'."

class InvalidUrl(Warning):
    label = 'invalid-url'
    descr = 'Your URL is not valid. It must begin with http, https or ftp and must not\ncontain anymore the word mandrake.'

class IncoherentVersionDependencyOn(Warning):
    label = 'incoherent-version-dependency-on'

class SpellingErrorInSummary(Warning):
    label = 'spelling-error-in-summary'
    descr = 'You made a misspelling in the Summary. Please double-check.'

class NoVersionDependencyOn(Warning):
    label = 'no-version-dependency-on'
class NonStandardGroup(Warning):
    label = 'non-standard-group'
    descr = 'The group specified in your spec file is not valid. To find a valid group,\nplease refer to the Mandriva Linux RPM documentation.'

class NoEpochInConflicts(Warning):
    label = 'no-epoch-in-conflicts'
    descr = 'Your package contains a versioned Conflicts entry without an Epoch.'

class SummaryNotCapitalized(Warning):
    label = 'summary-not-capitalized'
    descr = "Summary doesn't begin with a capital letter."

class NoEpochInObsoletes(Warning):
    label = 'no-epoch-in-obsoletes'
    descr = 'Your package contains a versioned Obsoletes entry without an Epoch.'

def spell_check(pkg, str, tagname):
    for seq in string.split(str, ' '):
        for word in re.split('[^a-z]+', string.lower(seq)):
            if len(word) > 0:
                try:
                    if word[0] == '\'':
                        word=word[1:]
                    if word[-1] == '\'':
                        word=word[:-1]                
                    correct=BAD_WORDS[word]
                    yield SpellingErrorIn(pkg, tagname, word, correct)
                except KeyError:
                    pass

class TagsCheck(AbstractCheck.AbstractCheck):
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, 'TagsCheck')

    def check(self, pkg):

        packager=pkg[rpm.RPMTAG_PACKAGER]
        if not packager:
	    yield NoPackagerTag(pkg)
        elif not packager_regex.search(packager):
            yield InvalidPackager(pkg, packager)
            
	version=pkg[rpm.RPMTAG_VERSION]
	if not version:
	    yield NoVersionTag(pkg)
        else:
            res=invalid_version_regex.search(version)
            if res:
                yield InvalidVersion(pkg, version)
                
        release=pkg[rpm.RPMTAG_RELEASE]
	if not release:
	    yield NoReleaseTag(pkg)
        elif release_ext and not extension_regex.search(release):
            yield NotStandardReleaseExtension(pkg, release)

        epoch=pkg[rpm.RPMTAG_EPOCH]
        if epoch is None:
            if use_epoch:
                yield NoEpochTag(pkg)
        else:
            if epoch > 99:
                yield UnreasonableEpoch(pkg, epoch)

        if use_epoch:
            for o in pkg.obsoletes():
                if o[1] and not epoch_regex.search(o[1]):
                    yield NoEpochInObsoletes(pkg, o[0] + ' ' + o[1])
            for c in pkg.conflicts():
                if c[1] and not epoch_regex.search(c[1]):
                    yield NoEpochInConflicts(pkg, c[0] + ' ' + c[1])
            for p in pkg.provides():
                if p[1] and not epoch_regex.search(p[1]):
                    yield NoEpochInProvides(pkg, p[0] + ' ' + p[1])

	name=pkg[rpm.RPMTAG_NAME]
        deps=pkg.requires() + pkg.prereq()
        devel_depend=0
        is_devel=devel_regex.search(name)
        is_source=pkg.isSource()
        for d in deps:
            if use_epoch and d[1] and d[0][0:7] != 'rpmlib(' and not epoch_regex.search(d[1]):
                yield NoEpochInDependency(pkg, d[0] + ' ' + d[1])
            for r in INVALID_REQUIRES:
                if r.search(d[0]):
                    yield InvalidDependency(pkg, d[0])

	    if requires_in_usr_local_regex.search(d[0]):
                    yield InvalidDependency(pkg, d[0])
		
            if not devel_depend and not is_devel and not is_source:
                if devel_regex.search(d[0]):
                    yield DevelDependency(pkg, d[0])
                    devel_depend=1
            if is_source and lib_devel_number_regex.search(d[0]):
                yield InvalidBuildRequires(pkg, d[0])
            if not is_source and not is_devel:
                res=lib_regex.search(d[0])
                if res and not res.group(1) and not d[1]:
                    yield ExplicitLibDependency(pkg, d[0])
            if d[2] == rpm.RPMSENSE_EQUAL and string.find(d[1], '-') != -1:
                yield RequiresOnRelease(pkg, d[0], d[1])
            
	if not name:
	    yield NoNameTag(pkg)
	else:
            if is_devel and not is_source:
                base=is_devel.group(1)
                dep=None
                has_so=0
                for f in pkg.files().keys():
                    if so_regex.search(f):
                        has_so=1
                        break
                if has_so:
                    for d in deps:
                        if d[0] == base:
                            dep=d
                            break
                    if not dep:
                        yield NoDependencyOn(pkg, base)
                    elif version:
                        if use_epoch:
                            expected=str(epoch) + ":" + version
                        else:
                            expected=version
                        if dep[1][:len(expected)] != expected:
                            if dep[1] != '':
                                yield IncoherentVersionDependencyOn(pkg, base, dep[1], expected)
                            else:
                                yield NoVersionDependencyOn(pkg, base, expected)
                    res=devel_number_regex.search(name)
                    if not res:
                        yield NoMajorInName(pkg, name)
                    else:
                        if res.group(3):
                            prov=res.group(1) + res.group(2) + '-devel'
                        else:
                            prov=res.group(1) + '-devel'
                            
                        if not prov in map(lambda x: x[0], pkg.provides()):
                            yield NoProvides(pkg, prov)
                    
	summary=pkg[rpm.RPMTAG_SUMMARY]
	if not summary:
	    yield NoSummaryTag(pkg)
	else:
            spell_check(pkg, summary, 'summary')
            if string.find(summary, '\n') != -1:
                yield SummaryOnMultipleLines(pkg)
            if not capital_regex.search(summary[0]):
                yield SummaryNotCapitalized(pkg, summary)
            if summary[-1] == '.':
                yield SummaryEndedWithDot(pkg, summary)
            if len(summary) >= 80:
                yield SummaryTooLong(pkg, summary)
            if leading_space_regex.search(summary):
                yield SummaryHasLeadingSpaces(pkg, summary)
            res=forbidden_words_regex.search(summary)
            if res:
                yield SummaryUseInvalidWord(pkg, res.group(1))

        description=pkg[rpm.RPMTAG_DESCRIPTION]
	if not description:
	    yield NoDescriptionTag(pkg)
        else:
            spell_check(pkg, description, 'description')
            for l in string.split(description, "\n"):
                if len(l) >= 80:
                    yield DescriptionLineTooLong(pkg, l)
                res=forbidden_words_regex.search(l)
                if res:
                    yield DescriptionUseInvalidWord(pkg, res.group(1))
                
                    
	group=pkg[rpm.RPMTAG_GROUP]
        if not group:
	    yield NoGroupTag(pkg)
	else:
	    if not group in VALID_GROUPS:
		yield NonStandardGroup(pkg, group)

        buildhost=pkg[rpm.RPMTAG_BUILDHOST]
        if not buildhost:
            yield NoBuildhostTag(pkg)
        else:
            if not valid_buildhost_regex.search(buildhost):
                yield InvalidBuildhost(pkg, buildhost)
                
	changelog=pkg[rpm.RPMTAG_CHANGELOGNAME]
        if not changelog:
	    yield NoChangelognameTag(pkg)
        elif use_version_in_changelog and not pkg.isSource():
            ret=changelog_version_regex.search(changelog[0])
            if not ret:
                yield NoVersionInLastChangelog(pkg)
            elif version and release:
                srpm=pkg[rpm.RPMTAG_SOURCERPM]
                # only check when source name correspond to name
                if srpm[0:-8] == '%s-%s-%s' % (name, version, release):
                    expected=version + '-' + release
                    if epoch is not None:
                        expected=str(epoch) + ':' + expected
                    if expected != ret.group(1):
                        yield IncoherentVersionInChangelog(pkg, ret.group(1), expected)

#         provides=pkg.provides()
#         for (provide_name, provide_version, provide_flags) in provides:
#             if name == provide_name:
#                 yield PackageProvidesItself(pkg)
#                 break

        license=pkg[rpm.RPMTAG_LICENSE]
        if not license:
            yield NoLicense(pkg)
        else:
            if license not in VALID_LICENSES:
                licenses=re.split('(?:[- ]like|/|ish|[- ]style|[- ]Style|and|or|&|\s|-)+', license)
                for l in licenses:
                    if l != '' and not l in VALID_LICENSES:
                        yield InvalidLicense(pkg, license)
                        break

        url=pkg[rpm.RPMTAG_URL]
        if url and url != 'none':
            if not url_regex.search(url):
                yield InvalidUrl(pkg, url)
            elif invalid_url_regex.search(url):
                yield InvalidUrl(pkg, url)
        else:
            yield NoUrlTag(pkg)

        obs=map(lambda x: x[0], pkg.obsoletes())
        provs=map(lambda x: x[0], pkg.provides())
	if pkg.name in obs:
		yield ObsoleteOnName(pkg)
		
        for o in obs:
            if not o in provs:
                yield ObsoleteNotProvided(pkg, o)
	useless_provides=[]	
	for p in provs:
	    if provs.count(p) != 1:
		if p not in useless_provides:
			useless_provides.append(p)
	for p in useless_provides:
	    yield UselessExplicitProvides(pkg,p)

        if pkg.isNoSource():
            arch='nosrc'
        elif pkg.isSource():
            arch='src'
        else:
            arch=pkg[rpm.RPMTAG_ARCH]

        expected='%s-%s-%s.%s.rpm' % (name, version, release, arch)
        basename=string.split(pkg.filename, '/')[-1]
        if basename != expected:
            yield NonCoherentFilename(pkg, basename)

# Create an object to enable the auto registration of the test
check=TagsCheck()


def init(context):
	context.installCheck(TagsCheck)
# TagsCheck.py ends here
