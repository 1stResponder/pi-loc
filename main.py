"""This module does blah blah."""
import ConfigParser
import os
import time
import logging
import logging.handlers
import sys
import requests
from gps_poll import GpsPoller
from edxlde_util import generate_de

if __name__ == '__main__':
    GPSP = GpsPoller()
    CONFIG = ConfigParser.RawConfigParser()
    CONFIG.read('config.cfg')
    URL = CONFIG.get('Main', 'URL')
    LOGLEVEL = CONFIG.get('Main', 'Logging')
    LOGLOC = CONFIG.get('Main', 'LogLocation')
    LOG_LEVEL_NUM = getattr(logging, LOGLEVEL, None)
    if not isinstance(LOG_LEVEL_NUM, int):
        raise ValueError('Invalid log level: %s' % LOGLEVEL)
    LOG_FILENAME = LOGLOC+'py-loc.out'
    if not os.access(LOG_FILENAME, os.W_OK):
        LOG_FILENAME = "/var/log/pi-loc.out"
    LOGGER = logging.getLogger('py-loc')
    LOGGER.setLevel(LOG_LEVEL_NUM)
    HANDLER = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=20000000, backupCount=5)
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    HANDLER.setFormatter(FORMATTER)
    LOGGER.addHandler(HANDLER)
    SESS = requests.Session()
    SESS.headers.update({'Content-Type': 'text/xml'})
    LOGGER.info('session established')

    try:
        GPSP.start()
        while True:
            try:
                REPORT = GPSP.get_current_value()
                LOGGER.debug(REPORT)
                DESTR = generate_de(str(REPORT['lat']), str(REPORT['lon']))
                RESP = SESS.post(url=URL, data=DESTR)
                LOGGER.info('Response: %s\tContent: %s', RESP.status_code, RESP.content)
                LOGGER.debug(DESTR)
                #print RESP.status_code
                #print RESP.content
                #print DESTR
                time.sleep(4.5)
            except AttributeError as attribex:
                LOGGER.warn("Attribute Error %s: %s", attribex.args, attribex.message)
            except KeyError as keyex:
                LOGGER.warn("Attribute Error %s: %s", keyex.args, keyex.message)
            except:
                LOGGER.error('Error in loop: %s', sys.exc_info()[0])
            time.sleep(0.5)

    except(KeyboardInterrupt, SystemExit):
        LOGGER.info('Killing Thread..')
        GPSP.running = False
        GPSP.join()
    LOGGER.info('Done; Exiting.')
