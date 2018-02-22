"""This module uploads logs to S3"""

import subprocess
import datetime
import boto
from boto.s3.key import Key

# You will need to fill out your own details here for logging
S3 = boto.connect_s3('<aws access key>', '<aws secret key>')
BUCKETNAME = 'BUCKETNAME'
BUCKET = S3.get_bucket(BUCKETNAME, validate=True)
FILENAME = 'pi-loc-dev-log-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.tar.gz'
FLAGS = '/tmp/' + FILENAME
subprocess.call(['/bin/tar', '-zcvf', FLAGS, '/var/log'])
K = Key(BUCKET)
K.key = FILENAME
K.set_contents_from_filename(FLAGS)
