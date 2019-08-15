# -*- coding: utf-8 -*-

import time
import signal
import lib
import sys

def scrape():
        # Assume we are hitting Streaming API
        # and doing something buzzwordy with it
        while True:
                lib.scrape_me_bro()
                time.sleep(2)
                reload(lib)

def reload_libs(signum, frame):
        print "Received Signal: %s at frame: %s" % (signum, frame)
        print "Excuting a Lib Reload"
        reload(lib)
        sys.exit()

# Register reload_libs to be called on restart
signal.signal(signal.SIGINT, reload_libs)


# Main
scrape()