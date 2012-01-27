import re
from scrutiny import Error

class FilterError(Error):
    pass


class Filter:
    def __init__(self, *a, **kw):
        pass
        
    def matches(self, notice):
        return False


class RegexFilter(Filter):
    def __init__(self, *a, **kw):
        if type(expression) is str:
            self._expression = re.compile(_expression)
        else:
            self._expression = expression

    def matches(self, notice):
        formatted = notice.formatMessage()
        return not not re.match(self._expression, notice)



class FieldsFilter(Filter):
    def __init__(self, **kwargs):
        self._kwargs = kwargs


    def checkField(self, fvalue, nvalue):
        return fvalue == nvalue
        

    def matches(self, notice):
        checkField = self.checkField
        try:
            for key, value in self._kwargs.iteritems():
                if not checkField(value, getattr(notice, key)):
                    return 
        except AttributeError:
            return False
        return True



class FieldsRegexFilter(Filter):
    def __init__(self, **kwargs):
        self._kwargs = dict([(k, re.compile(v)) 
                        for k, v in kwargs.iteritems()])
        

    def checkField(self, fvalue, nvalue):
        return not not fvalue.match(nvalue)


class FilterContext:
    __slots__ = ()
    def __init__(self):
        self._filters = []


    def addFilter(self, filter):
        self._filters.append(filter)


    def matches(self, notice):
        for filter in self._filters:
            if not filter.matches(notice):
                return False
        return True


# vim:ts=4:sw=4:et
