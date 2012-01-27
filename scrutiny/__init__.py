import sys
import os

__all__ = "Error", "CheckContext", "formatNotice", "VERSION"

VERSION = "0.01"

class Error(Exception):
    pass

class CheckContext:
    def __init__(self, 
          extractdir="/var/tmp/scrutiny",
          checksdir="/var/lib/scrutiny/checks",
          filter=None):
        self._extractDir = "/var/tmp/scrutiny"
        self._checksDir = [
            os.path.join(os.path.split(__file__)[0], "checks")]
        self._checks = []
        self.filter = filter 
        if not os.path.exists(extractdir):
            os.makedirs(extractdir)
       
    def addChecksDir(self, checksdir):
        self._checksDir.append(checksDir)


    def loadChecks(self):
        checksdir = [dir for dir in self._checksDir if os.path.exists(dir)]
        sys.path.insert(0, os.path.join(os.path.split(__file__)[0], "compat"))
        origpath = sys.path[:]
        for dir in checksdir:
            sys.path.insert(0, dir)
            for sdir in "error", "warning", "info":
                sdirpath = os.path.join(dir, sdir)
                if os.path.exists(sdirpath):
                    reload(__import__(sdir))
                    for file in os.listdir(sdirpath):
                        if file[0] not in "._" and file.endswith(".py"):
                            modname = file[:-3]
                            mod = __import__(sdir + "." + file[:-3], 
                                             None, None, modname)
                            try:
                                f = getattr(mod, "init")
                            except AttributeError:
                                raise Error, ("The module %s must provide an "
                                              "'init()' function" % 
                                              (os.path.join(sdirpath, file)))
                            f(self)
            sys.path = origpath[:]


    def installCheck(self, check):
        self._checks.append(check())


    def checkFile(self, file):
        from scrutiny.package import Pkg
        pkg = Pkg(file, self._extractDir)
        return self.checkPackage(pkg)


    def checkPackage(self, package):
        filter = self.filter
        for check in self._checks:
            for notice in check.check(package):
                if filter and filter.matches(notice):
                    continue
                else:
                    yield notice
        package.cleanup()


    def shutdown(self):
        for check in self._checks:
            check.shutdown()


    def setFilter(self, filter):
        self.filter = filter


def formatNotice(notice):
    return "%s: %s" % (notice.prefix, notice.formatMessage())
            

# vim:ts=4:sw=4:et
