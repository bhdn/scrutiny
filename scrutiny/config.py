# argh!

options = {}

def setOption(name, value):
    global options
    options[name] = value

def getOption(name, default=None):
    global options
    try:
        return options[name]
    except KeyError:
        return default

# vim:ts=4:sw=4:et
