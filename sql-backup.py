#!/usr/bin/env python

# Copyright (c) 2013 Alexander Chernyakhovsky
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import logging
import sys
import subprocess
from datetime import datetime
from optparse import OptionParser

# Configuration has to be stored in a global variable as it has to be
# accessible to all functions
config = None

def main():
    parser = OptionParser()
    parser.add_option('-c', '--config', dest='config',
                      help='path to configuration', metavar='FILE')
    parser.add_option('-v', '--verbose',
                      action='store_true', dest='verbose', default=False,
                      help='print status messages to stdout')
    (options, args) = parser.parse_args()

    # Uncomment this to make -v actually work
    #logger.setLevel(logging.INFO if options.verbose else 
    #                logging.WARNING)

    logger.debug(options)

    if options.config is None:
        die('No configuration file specified')
    load_config(options.config)

    logger.debug(config)

    result_file = get_backup_file_path()
    logger.info('Backing up to "%s"' % (result_file,))
    perform_backup(result_file)

def setup_logger():
    logger = logging.getLogger('sql-backup')
    logger.setLevel(logging.DEBUG)
    
    # Create console handler and formatter
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger

def load_config(filename):
    global config
    try:
        config = json.load(open(filename, 'r'))
    except:
        logger.exception('Failed to load configuration file "%s"' % (filename,))
        sys.exit(1)

    logger.info('Loaded "%s"' % (filename,))

def get_backup_dir(backup_type):
    return "%s/%s" % (config['backup_path'], backup_type)

def get_backup_file_path(backup_type='daily'):
    format_str = '{dir}/' + config['naming_scheme']
    now = datetime.now()
    return format_str.format(dir=get_backup_dir(backup_type), date=now)

def perform_backup(filename):
    try:
        with open(filename, 'wb') as backup_file:
            dumper = log_and_popen(config['dumper'], stdout=subprocess.PIPE)
            compressor = log_and_popen(config['compressor'], stdin=dumper.stdout, stdout=backup_file)
            dumper.stdout.close()
            compressor.wait()
            dumper.wait()
    except:
        logger.exception('Failed to perform backup')
        sys.exit(1)

def log_and_popen(*args, **kwargs):
    logger.debug('Popen(%r, %r)' % (args, kwargs))
    return subprocess.Popen(*args, **kwargs)

def die(error):
    logger.error(error)
    sys.exit(1)

logger = setup_logger()

if __name__ == '__main__':
    main()
