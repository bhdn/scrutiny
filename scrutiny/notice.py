from scrutiny import Error

__all__ = ("Notice", "Error", "Info", "Warning", "getNoticeByName",
           "sortNoticeTypes")

class NoticeMarker(type):
    notices = []
    def __new__(cls, name, bases, dict):
        if "name" not in dict:
            dict["name"] = name
        if "label" not in dict:
            dict["label"] = name
        
        klass = type.__new__(cls, name, bases, dict)
        cls.notices.append(klass)
        return klass


class NoSuchNotice(Error):
    pass


class Notice(object):
    __metaclass__ = NoticeMarker
    
    descr = ""
    infourl = "http://mandriva.com/bla/bla"


    def __init__(self, package, *args):
        self.package = package
        self.args = args
        self.formatted = None


    def getNotices():
        return NoticeMarker.notices
    getNotices = staticmethod(getNotices)


    def formatMessage(self):
        if self.formatted:
            return self.formatted
        if self.label:
            label = self.label
        else:
            label = self.__name__
        self.formatted = "%s %s: %s" % (self.package.name, self.label,
                "".join([str(i) for i in self.args if i or i != "\n"]))
        return self.formatted


class Error(Notice):
    _order = 0
    prefix = "E"
    label = "Error"


class Warning(Notice):
    _order = 1
    prefix = "W"
    label = "Warning"


class Info(Notice):
    _order = 2
    prefix = "I"
    label = "Info"


def createNotice(type, label, description):
    pass

def getNoticeByName(name):
    notices = Notice.getNotices()
    try:
        return notices[name]
    except KeyError:
        for notice in notices:
            if notice.label == name:
                return notice
    raise NoSuchNotice, name


def sortNoticeTypes(types):
    types = [(type._order, type) for type in types]
    types.sort()
    return [item[1] for item in types]


# vim:ts=4:sw=4:et
