
from scrutiny.notice import Error, Warning

class InvalidLocaleManDir(Error):
    label = 'invalid-locale-man-dir'

class IncorrectI18nTag(Warning):
    label = 'incorrect-i18n-tag'

class FileNotInLang(Warning):
    label = 'file-not-in-lang'

class NoDependencyOn(Error):
    label = 'no-dependency-on'

class InvalidLcMessagesDir(Error):
    label = 'invalid-lc-messages-dir'

class IncorrectLocale(Error):
    label = 'incorrect-locale'

class IncorrectLocaleSubdir(Error):
    label = 'incorrect-locale-subdir'

#############################################################################
# File		: I18NCheck.py
# Package	: rpmlint
# Author	: Frederic Lepied
# Created on	: Mon Nov 22 20:02:56 1999
# Version	: $Id: I18NCheck.py,v 1.38 2005/08/10 02:05:47 flepied Exp $
# Purpose	: checks i18n bugs.
#############################################################################

from Filter import *
import AbstractCheck
import re
import rpm
import Config

# Defined in header.h
HEADER_I18NTABLE=100

# Associative array of invalid value => correct value
INCORRECT_LOCALES = {
    'in': 'id',
    'in_ID': 'id_ID',
    'iw': 'he',
    'iw_IL': 'he_IL',
    'gr': 'el',
    'gr_GR': 'el_GR',
    'cz': 'cs',
    'cz_CZ': 'cs_CZ',
    'sw': 'sv',
    'lug': 'lg', # 'lug' is valid, but we standardize on 2 letter codes
    'en_UK': 'en_GB'}

# Correct subdirs of /usr/share/local for LC_MESSAGES
# and /usr/share/man for locale man pages.
#
# 'en_RN' and 'en@IPA' are not real language bu funny variations on english
CORRECT_SUBDIRS = (
'af', 'am', 'ar', 'as', 'az', 'az_IR', 'be', 'bg', 'bn', 'br', 'bs',
'ca', 'cs', 'cy', 'da', 'de', 'de_AT', 'dz', 'el', 
'en_AU', 'en_CA', 'en_GB', 'en_IE', 'en_US', 'en_RN', 'en@IPA', 
'eo', 'es', 'es_AR', 'es_ES', 'es_DO', 'es_GT', 'es_HN', 'es_SV', 'es_PE',
'es_PA', 'es_MX', 'et', 'eu',
'fa', 'fi', 'fo', 'fr', 'fur', 'ga', 'gd', 'gl', 'gn', 'gu', 'gv',
'he', 'hi', 'hr', 'hu', 'hy',
'ia', 'id', 'is', 'it', 'iu', 'ja', 'ka', 'kl', 'kn', 'ko', 'ku', 'kw', 'ky',
# 'ltg' is not a standard ISO code; latgalian hasn't yet an ISO code 
'li', 'lo', 'lt', 'ltg', 'lg', 'lv',
'mg', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt',
'nb', 'nds', 'nds_DE', 'ne', 'nl', 'nn', 'no', 'nr', 'nso'
'oc', 'or', 'pa_IN', 'ph', 'pl', 'pp', 'pt', 'pt_BR', 'qu', 'ro', 'ru',
'sc', 'se', 'sk', 'sl', 'sq', 'sr', 'sr@Latn', 'sr@ije', 'ss', 'st', 'sv',
'ta', 'te', 'tg', 'th', 'tk', 'tl', 'tn', 'tr', 'ts', 'tt', 
'ug', 'uk', 'ur', 'uz', 'uz@Latn',
've', 'vi', 'wa', 'wen', 'xh', 'yi', 'yo', 'zh_CN', 'zh_HK', 'zh_TW', 'zu',
# KDE uses 'ven' for 've'
'ven',
# 
# note: zh_CN.GB2312 and zh_TW.Big5 (that is, names with charset information)
# are obsolescent, but still widely used; some day however they should
# be removed from this list.
'zh_CN.GB2312', 'zh_TW.Big5',
)

str='-('
for s in CORRECT_SUBDIRS:
    str=str+'|'+s[0:2]
str=str+')$'

package_regex=re.compile(str)
locale_regex=re.compile('^(/usr/share/locale/([^/]+))/')
correct_subdir_regex=re.compile('^(([a-z][a-z](_[A-Z][A-Z])?)([.@].*$)?)$')
lc_messages_regex=re.compile('/usr/share/locale/([^/]+)/LC_MESSAGES/.*(mo|po)$')
man_regex=re.compile('/usr(?:/share)?/man/([^/]+)/man./[^/]+$')
mo_regex=re.compile('\.mo$')
webapp_regex=re.compile('/etc/httpd/webapps.d/[^/]+$/')

# list of exceptions
#
# note: ISO-8859-9E is non standard, ISO-8859-{6,8} are of limited use
# as locales (since all modern handling of bidi is based on utf-8 anyway),
# so they should be removed once UTF-8 is deployed)
EXCEPTION_DIRS=('C', 'POSIX', 'CP1251', 'CP1255', 'CP1256',
'ISO-8859-1', 'ISO-8859-2', 'ISO-8859-3', 'ISO-8859-4', 'ISO-8859-5',
'ISO-8859-6', 'ISO-8859-7', 'ISO-8859-8', 'ISO-8859-9', 'ISO-8859-9E',
'ISO-8859-10', 'ISO-8859-13', 'ISO-8859-14', 'ISO-8859-15',
'KOI8-R', 'KOI8-U', 'UTF-8')

class I18NCheck(AbstractCheck.AbstractCheck):
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, 'I18NCheck')

    def check(self, pkg):

        if pkg.isSource():
            return
        
	files=pkg.files()
	locales=[]			# list of locales for this packages
        webapp=False
        
	i18n_tags = pkg[HEADER_I18NTABLE]
        #i18n_files = pkg.langFiles()
        
	for i in i18n_tags:
	    try:
		correct=INCORRECT_LOCALES[i]
		yield printError(pkg, 'incorrect-i18n-tag-' + correct, i)
	    except KeyError:
		pass

	# as some webapps have their files under /var/www/html, and
	# others in /usr/share or /usr/lib, the only reliable way
	# sofar to detect them is to look for an apache configuration file
	for f in files.keys():
	    if mo_regex.search(f):
		webapp=True
	    
	for f in files.keys():
	    res=locale_regex.search(f)
	    if res:
		locale=res.group(2)
		# checks the same locale only once
		if not locale in locales:
		    locales.append(locale)
		    res2=correct_subdir_regex.search(locale)
		    if not res2:
			if not locale in EXCEPTION_DIRS:
			    yield IncorrectLocaleSubdir(pkg, f)
		    else:
			locale_name = res2.group(2)
			try:
			    correct=INCORRECT_LOCALES[locale_name]
			    yield IncorrectLocale(pkg, correct, f)
			except KeyError:
			    pass
            res=lc_messages_regex.search(f)
            subdir=None
            if res:
                subdir=res.group(1)
                if not subdir in CORRECT_SUBDIRS:
                    yield InvalidLcMessagesDir(pkg, f)
            else:
                res=man_regex.search(f)
                if res:
                    subdir=res.group(1)
                    if subdir != 'man' and not subdir in CORRECT_SUBDIRS:
                        yield InvalidLocaleManDir(pkg, f)
                    else:
                        subdir=None

            if mo_regex.search(f) or subdir:
                if pkg.fileLang(f) == '' and not webapp:
                    yield FileNotInLang(pkg, f)

        name=pkg[rpm.RPMTAG_NAME]
        res=package_regex.search(name)
        if res:
            locales='locales-' + res.group(1)
            if locales != name:
                if not locales in map(lambda x: x[0], pkg.requires()):
                    yield NoDependencyOn(pkg, locales)

# Create an object to enable the auto registration of the test
check=I18NCheck()



def init(checkcontext):
	checkcontext.installCheck(I18NCheck)
		

# I18NCheck.py ends here
