#------------------------------------------------------------------------------
# File          	: ZipCheck.py
# Package       	: scrutiny
# Original Author	: Ville Skytta
# Purpose       	: Verify Zip/Jar file correctness
#------------------------------------------------------------------------------

from scrutiny.notice import Error, Warning

from Filter import *
import AbstractCheck
import Config
import os
import re
import stat
import zipfile

# Globals
zip_regex=re.compile('\.(zip|[ewj]ar)$')
jar_regex=re.compile('\.[ewj]ar$')
classpath_regex=re.compile('^\s*Class-Path\s*:', re.M | re.I)

want_indexed_jars = Config.getOption('UseIndexedJars', 1)


class BadCrcInZip(Error):
    label = 'bad-crc-in-zip'
    descr = 'The reported file in the zip fails the CRC check. Usually this is a\nsign of a corrupt zip file.'

class NoJarManifest(Error):
    label = 'no-jar-manifest'
    descr = 'The jar file does not contain a META-INF/MANIFEST file.'

class JarNotIndexed(Warning):
    label = 'jar-not-indexed'
    descr = 'The jar file is not indexed, ie. it does not contain the META-INF/INDEX.LIST\nfile.  Indexed jars speed up the class searching process of classloaders\nin some situations.'

class UncompressedZip(Warning):
    label = 'uncompressed-zip'
    descr = 'The zip file is not compressed.'

class JarIndexed(Warning):
    label = 'jar-indexed'
    descr = 'The jar file is indexed, ie. it contains the META-INF/INDEX.LIST file.\nThese files are known to cause problems with some older Java versions.'

class ClassPathInManifest(Warning):
    label = 'class-path-in-manifest'
    descr = 'The META-INF/MANIFEST file in the jar contains a hardcoded Class-Path.\nThese entries do not work with older Java versions and even if they do work,\nthey are inflexible and usually cause nasty surprises.'


class ZipCheck(AbstractCheck.AbstractCheck):

    def __init__(self):
        AbstractCheck.AbstractCheck.__init__(self, "ZipCheck")

    def check(self, pkg):
        for i in pkg.getFilesInfo():
            f = pkg.dirName() + i[0]
            if zip_regex.search(f) and \
                   stat.S_ISREG(os.lstat(f)[stat.ST_MODE]) and \
                   zipfile.is_zipfile(f):
                zip = None
                try:
                    zip = zipfile.ZipFile(f, 'r')
                    badcrc = zip.testzip()
                    if badcrc:
                        yield BadCrcInZip(pkg, badcrc, i[0])
                    compressed = 0
                    for zinfo in zip.infolist():
                        if zinfo.compress_type != zipfile.ZIP_STORED:
                            compressed = 1
                            break
                    if not compressed:
                        yield UncompressedZip(pkg, i[0])

                    # additional jar checks
                    if jar_regex.search(f):
                        try:
                            mf = zip.read('META-INF/MANIFEST.MF')
                            if classpath_regex.search(mf):
                                yield ClassPathInManifest(pkg, i[0])
                        except KeyError:
                            yield NoJarManifest(pkg, i[0])
                        try:
                            zinfo = zip.getinfo('META-INF/INDEX.LIST')
                            if not want_indexed_jars:
                                yield JarIndexed(pkg, i[0])
                        except KeyError:
                            if want_indexed_jars:
                                yield JarNotIndexed(pkg, i[0])
                            pass
                except:
                    sys.stderr.write('%s: unable-to-read-zip %s "%s"\n' % (pkg.name, i[0], sys.exc_info()[1]))

                zip and zip.close()


check = ZipCheck()

def init(context):
	context.installCheck(ZipCheck)
    
