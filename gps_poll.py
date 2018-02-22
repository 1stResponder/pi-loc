"""GPS Library Handler"""
import threading
from gps import *
#from time import *


class GpsPoller(threading.Thread):
    """GPS Class for Pythong"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def get_current_value(self):
        """Returns the current value of GPS"""
        return self.current_value
    def get_fix(self):
        return self.fix

    def run(self):
        try:
            while self.running:
                self.current_value = self.session.next()
        except StopIteration:
            pass
        