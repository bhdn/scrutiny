from scrutiny.config import getOption, setOption

from setuplist import *

info = True


# cut & paste
DEFAULT_LAUNCHERS_OLD = (['(?:/usr/bin/)?kdesu', ('/usr/bin/kdesu', 'kdesu')],
                         ['(?:/usr/bin/)?launch_x11_clanapp', ('/usr/bin/launch_x11_clanapp', 'clanlib', 'libclanlib0')],
                         ['(?:/usr/bin/)?soundwrapper', None],
                         ['NO_XALF', None],
                         )
DEFAULT_LAUNCHERS_90 = (['(?:/usr/bin/)?kdesu', ('/usr/bin/kdesu', 'kdesu')],
                        ['(?:/usr/bin/)?launch_x11_clanapp', ('/usr/bin/launch_x11_clanapp', 'clanlib', 'libclanlib0')],
                        ['(?:/usr/bin/)?soundwrapper', None],
                        )

DEFAULT_LAUNCHERS = DEFAULT_LAUNCHERS_90

STANDARD_GROUPS = STANDARD_GROUPS_NEW
STANDARD_USERS = STANDARD_USERS_NEW


# vim:ts=4:sw=4:et
