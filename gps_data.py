"""Sample Main File to Poll GPS"""
import os
import time
from gps_poll import GpsPoller

if __name__ == '__main__':
    GPSP = GpsPoller()
    try:
        GPSP.start()
        while True:
            os.system('clear')
            REPORT = GPSP.get_current_value()
            # print report
            try:
                if REPORT.keys()[0] == 'epx':
                    print REPORT['lat']
                    print REPORT['lon']
                time.sleep(.5)
            except(AttributeError, KeyError):
                pass
            time.sleep(0.5)

    except(KeyboardInterrupt, SystemExit):
        print "\nKilling Thread.."
        GPSP.running = False
        GPSP.join()

    print "Done.\nExiting."
        