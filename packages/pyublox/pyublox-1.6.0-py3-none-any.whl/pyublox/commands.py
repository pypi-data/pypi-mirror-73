import datetime
import json
import os.path
import sys
import serial
import signal
import time
import queue

from roktools import logger

from .ublox import io as ublox_io
from .ublox import core as ublox_core
from .ublox import constants
from .ublox import helpers
from .ublox import SERIAL_PORT_STR
from . import OUTPUT_DIR_STR, NAME_STR, FILE_STR, JSON_STR, RATE_STR, MESSAGES_STR

# ------------------------------------------------------------------------------

_record_thread = None

# ------------------------------------------------------------------------------

def config(**kwargs):

    serial_port = kwargs.get(SERIAL_PORT_STR, None)
    conn_config = ublox_io.detect_connection(serial_port=serial_port)

    serial_port = conn_config[SERIAL_PORT_STR]

    logger.info(f'Attempting to configure device in serial port [ {serial_port} ]')

    stream = serial.Serial(serial_port)

    config_file = kwargs.get(FILE_STR, None)
    json_file = kwargs.get(JSON_STR, None)
    if config_file:
        logger.info(f'Configuring device from file [ {config_file} ]')
        with open(config_file, 'r') as fh:
            ublox_io.set_config_from_ucenter_file(stream, fh)

    elif json_file:
        logger.info(f'Configuring device from JSON file [ {json_file} ]')
        with open(json_file, 'r') as fh:
            ublox_io.set_config_from_json_file(stream, fh) 

    else:
        config_dict = {}

        if RATE_STR in kwargs:
            config_dict[constants.RATES_STR] = {
                constants.MEASUREMENTS_STR : kwargs[RATE_STR],
                constants.SOLUTION_STR : kwargs[RATE_STR] * 5
            }

        logger.info(f'Configuring device from command line options: {config_dict}')
        ublox_io.set_config_from_dict(stream, config_dict)

    stream.close()


# ------------------------------------------------------------------------------

def detect(**kwargs):

    serial_port = kwargs.get(SERIAL_PORT_STR, None)
    messages = kwargs.get(MESSAGES_STR, False)

    config = ublox_io.detect(serial_port=serial_port, messages=messages)

    if not config:
        sys.exit(1)
    else:
        json.dump(config, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write('\n')



# ------------------------------------------------------------------------------

def reset(**kwargs):

    serial_port = kwargs.get(SERIAL_PORT_STR, None)
    if not serial_port:
        logger.critical('Need to specify the port to be reset')
        sys.exit(1)
    else:
        logger.info(f'Resetting device in [ {serial_port} ]')

    ublox_io.reset(serial_port)



def record(**kwargs):

    logger.debug('Record arguments ' + str(kwargs))

    slice_period = helpers.SlicePeriodicity.from_string(kwargs['slice'])

    global _record_thread
    _record_thread = ublox_io.UbloxRecorder(serial_port=kwargs.get(SERIAL_PORT_STR, None),
                                   slice_period=slice_period,
                                   output_dir=kwargs[OUTPUT_DIR_STR],
                                   receiver_name=kwargs[NAME_STR])

    _record_thread.start()


# ------------------------------------------------------------------------------

def interruption_handler(sig, frame):
    logger.info('You pressed Ctrl+C, gracefully closing files and serial streams')

    global _record_thread
    _record_thread.stop()

    sys.exit(0)

signal.signal(signal.SIGINT, interruption_handler)
