
from scrutiny.notice import Error, Warning, Info
import Config # urgh!

 
class Foo:
    def __init__(self):
        self.items = {}
    def add(self, name, value):
        self.items[name] = value
    def get(self, name):
        return self.items[name]


notices = Foo()

def addDetails(*details):
    global notices
    for i in xrange(0, len(details), 2):
        class Dummy:
            label = details[i]
            descr = details[i + 1]
        Dummy.__name__ = coolizeLabel(Dummy.label)
        notices.add(Dummy.label, Dummy)

def getDescrByLabel(label):
    try:
        return notices.get(label)
    except KeyError:
        return ""


def coolizeLabel(label):
    words = label.split("-")
    return "".join([word.capitalize() for word in words])

def makeNotice(type, pkg, _label, args):
    class Dummy(type):
        label = _label
        descr = getDescrByLabel(_label)
    Dummy.__name__ = coolizeLabel(_label) 
    return Dummy(pkg, args)

def printError(pkg, label, *args):
    return makeNotice(Error, pkg, label, args)

def printWarning(pkg, label, *args):
    return makeNotice(Warning, pkg, label, args)

def printInfo(pkg, label, *args):
    return makeNotice(Info, pkg, label, args)

# vim:ts=4:sw=4:et
