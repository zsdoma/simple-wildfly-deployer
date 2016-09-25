import wildflyTool
import os
import sys

if __name__ == '__main__':
    pid = str(os.getpid())
    pidfile = "/tmp/wildflyTool.pid"
    if os.path.isfile(pidfile):
        print "%s already exists, exiting" % pidfile
        sys.exit()
    file(pidfile, 'w').write(pid)
    try:
        wildfly = wildflyTool.WildflyTool("")
        wildfly.start()
    finally:
        os.unlink(pidfile)
