
from scrutiny.notice import Error, Warning

from scrutiny import notice, check

import Config

class PackageNameNotCool(notice.Warning):
    name = "package name is not cool" # optional, class name is the default
    descr = "Why don't you give the name 'bleh' to your package?"
    infourl = "http://www.google.com/"


class MyFooCheck(check.Check):
    def check(self, package):
        if package.name != "bleh":
            yield PackageNameNotCool(package, package.name)


def init(checkcontext):
    checkcontext.installCheck(MyFooCheck)
    
# vim:ts=4:sw=4:et
