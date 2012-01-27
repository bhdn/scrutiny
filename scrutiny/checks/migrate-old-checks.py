#
# It must be run in the directory of the tests!
#
import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

import sys, os
import re
from sys import stderr

sys.path.insert(0, os.path.abspath("../../compat"))
sys.path.insert(0, os.path.abspath("../../../"))

import scrutiny
import scrutiny.notice
import Filter # from compat

def coolize(name):
    return "".join([i.capitalize() for i in name.split('-')])

# first stupid step, collect classes
klasses = {}
for fname in os.listdir("."):
    if fname.endswith("Check.py"):
        klasses[fname] = Filter.notices.items = {} 
        mod = __import__(fname[:-3])

# second step, discover which is the type (error, warning, info..) of the
# class, and then recreate that class with the properly Parent (engrish
# sucks!)
nottype = re.compile("print([a-zA-Z]+)\\s*\\(\\w+,\\s*[\"\']([a-z-_]+)[\"\']")
for fname, kdict in klasses.iteritems():
    untouched = kdict.keys()
    contents = open(fname).read()
    #for label, klass in kdict.iteritems():
    #    print "looking for", (nottype % label)
    #    found = re.findall(nottype % label, contents)
    #    if not found:
    #        print>>stderr, "WARN: não achei o uso desse label: %s" % label
    #        klass.realtype = "Warn"
    #    else:
    #        klass.realtype = typemap[found[0]]
    found = nottype.findall(contents)
    if not found:
        sys.stderr.write("WARN: print* expression matches none\n")
    else:
        for type, _label in found:
            realtype = type
            if _label not in kdict:
                class Dummy: 
                    label = _label 
                    descr = ''
                    realtype = realtype
                Dummy.__name__ = coolize(_label)
                kdict[_label] = Dummy
            else:
                kdict[_label].realtype = realtype
                try:
                    untouched.remove(_label)
                except ValueError:
                    pass
                    
    for label in untouched:
        kdict[label].realtype = "Warning"

# step three: patch files
import cStringIO
notext = "print\w+\s*\\(\s*(\w+)\s*,\s*[\"\']%s[\"\']\\s*(.*?)\\)"
notrep = "%s(\\1\\2)"
for fname, klasses in klasses.iteritems():
    contents = open(fname).read()
    for label, klass in klasses.iteritems():
        expr = notext % klass.label 
        newexpr = notrep % klass.__name__
        contents = re.sub(expr, newexpr, contents) 
    print "rewriting: %s", contents
    f = open(fname, "w+")
    f.write("\nfrom scrutiny.notice import Error, Info, Warning\n\n")
    for label, klass in klasses.iteritems():
        f.write("class %s(%s):\n" % (klass.__name__, klass.realtype))
        f.write("    label = %s\n" % repr(label))
        if klass.descr != "\n":
            f.write("    descr = %s\n" % repr(klass.descr))
        f.write("\n")
    f.write(contents)

def init(fsdf):
    pass


# vim:ts=4:sw=4:et
