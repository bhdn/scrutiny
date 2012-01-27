#!/usr/bin/python
import sys
import os

import scrutiny
import scrutiny.notice
    
def get_files(args):
    for file in args:
        if os.path.isdir(file):
            for fname in os.listdir(file):
                if fname.endswith(".rpm"):
                    yield os.path.join(file, fname)
        else:
            yield file
 

def show_version(*a):
    print "scrutiny", scrutiny.VERSION
    raise SystemExit

def parse_options():
    import optparse
    opt = optparse.OptionParser()
    opt.add_option("-e", "--extractdir", dest="extractdir", type="string",
            default="/var/tmp/scrutiny", 
            help="Directory to extract files")
    opt.add_option("-g", "--dontgroup", dest="group_notices",
            action="store_false", default=True,
            help="Don't group notices by type before print")
    opt.add_option("-o", "--option", dest="options", type="string",
            action="append", default=[],
            help="Set an rpmlint rpmlint option (--help-rpmlint for more information)")
    opt.add_option("-i", "--info", dest="show_info", 
            action="store_true", default=False,
            help="Show descriptive information about notices")
    opt.add_option("--version", dest="show_version", 
            action="callback", callback=show_version)
    
    options, args = opt.parse_args()
    if not args:
        opt.print_usage()
        raise SystemExit

    options.files = get_files(args)
    return options
 

def main(args):
    def printNotice(notice):
        print scrutiny.formatNotice(notice)
        if options.show_info:
            print notice.descr, "\n"
    
    try:
        options = parse_options()
        context = scrutiny.CheckContext(extractdir=options.extractdir)
        context.loadChecks()
        notices = {}
        for file in options.files:
            for notice in context.checkFile(file):
                if options.group_notices:
                    notices.setdefault(notice, []).append(notice)
                else:
                    printNotice(notice)
        if options.group_notices:
            for type in scrutiny.notice.sortNoticeTypes(notices):
                for notice in notices[type]:
                    printNotice(notice)
    except scrutiny.Error, msg:
        sys.stderr.write("Error: %s\n" % msg)
    except KeyboardInterrupt:
        sys.stderr.write("Interruped..\n")
    except SystemExit:
        pass
    except:
        import traceback
        traceback.print_exc()
        return 1
    return 0
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))

# vim:ts=4:sw=4:et
