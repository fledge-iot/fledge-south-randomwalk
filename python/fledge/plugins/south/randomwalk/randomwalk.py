# -*- coding: utf-8 -*-

# FLEDGE_BEGIN
# See: http://fledge-iot.readthedocs.io/
# FLEDGE_END

""" Module for RandomWalk poll mode plugin """

import copy
import logging

from fledge.common import logger
from fledge.plugins.common import utils

from random import randint

__author__ = "Bill Hunt"
__copyright__ = "Copyright (c) 2019 Dianomic Systems Inc."
__license__ = "Apache 2.0"
__version__ = "${VERSION}"


_DEFAULT_CONFIG = {
    'plugin': {
        'description': 'Generate random walk data points',
        'type': 'string',
        'default': 'randomwalk',
        'readonly': 'true'
    },
    'assetName': {
        'displayName': 'Asset name',
        'description': 'Name of Asset',
        'type': 'string',
        'default': 'randomwalk',
        'order': '1',
        'mandatory': 'true'
    },
    'minValue': {
        'displayName': 'Minimum Value',
        'description': 'Minimum value reading can go down to',
        'type': 'integer',
        'default': '10',
        'order': '2',
        'mandatory': 'true'
    },
    'maxValue': {
        'displayName': 'Maximum Value',
        'description': 'Maximum value reading can go up to',
        'type': 'integer',
        'default': '100',
        'order': '3',
        'mandatory': 'true'
    }
}

_LOGGER = logger.setup(__name__, level=logging.INFO)


def plugin_info():
    """ Returns information about the plugin.
    Args:
    Returns:
        dict: plugin information
    Raises:
    """
    return {
        'name': 'RandomWalk Poll plugin',
        'version': '3.1.0',
        'mode': 'poll',
        'type': 'south',
        'interface': '1.0',
        'config': _DEFAULT_CONFIG
    }


def plugin_init(config):
    """ Initialise the plugin.
    Args:
        config: JSON configuration document for the South plugin configuration category
    Returns:
        data: JSON object to be used in future calls to the plugin
    Raises:
    """
    data = copy.deepcopy(config)
    data['lastValue'] = None
    return data


def plugin_poll(handle):
    """ Extracts data from the sensor and returns it in a JSON document as a Python dict.
    Available for poll mode only.
    Args:
        handle: handle returned by the plugin initialisation call
    Returns:
        returns a sensor reading in a JSON document, as a Python dict, if it is available
        None - If no reading is available
    Raises:
        Exception
    """
    try:
        max_value = int(handle['maxValue']['value'])
        min_value = int(handle['minValue']['value'])
        last_value = handle['lastValue']

        # The maximum value cannot be less than the minimum value.
        # Therefore, setting the minimum value equal to the maximum value is required.
        if max_value < min_value:
            handle['minValue']['value'] = handle['maxValue']['value']
            min_value = int(handle['minValue']['value'])

        if last_value is None:
            new = randint(min_value, max_value)
        else:
            new = last_value + randint(-1, 1)
            if new > max_value:
                new = max_value
            elif new < min_value:
                new = min_value
        time_stamp = utils.local_timestamp()
        data = {
            'asset': handle['assetName']['value'],
            'timestamp': time_stamp,
            'readings': {
                "randomwalk": new
            }
        }
        handle['lastValue'] = new
    except (Exception, RuntimeError) as ex:
        _LOGGER.exception("RandomWalk exception: {}".format(str(ex)))
        raise ex
    else:
        return data


def plugin_reconfigure(handle, new_config):
    """ Reconfigures the plugin

    Args:
        handle: handle returned by the plugin initialisation call
        new_config: JSON object representing the new configuration category for the category
    Returns:
        new_handle: new handle to be used in the future calls
    """
    _LOGGER.info("Old config for randomwalk plugin {} \n new config {}".format(handle, new_config))
    new_handle = copy.deepcopy(new_config)
    new_handle['lastValue'] = handle['lastValue']
    max_value = int(new_handle['maxValue']['value'])
    # The maximum value cannot be less than the minimum value.
    # Therefore, setting the minimum value equal to the maximum value is required.
    if max_value < int(new_handle['minValue']['value']):
        new_handle['minValue']['value'] = max_value
    if not(new_handle['lastValue'] <= int(new_handle['minValue']['value']) <= max_value):
        new_handle['lastValue'] = randint(int(new_handle['minValue']['value']), max_value)
    return new_handle


def plugin_shutdown(handle):
    """ Shutdowns the plugin doing required cleanup, to be called prior to the South plugin service being shut down.

    Args:
        handle: handle returned by the plugin initialisation call
    Returns:
        plugin shutdown
    """
    _LOGGER.info('randomwalk plugin shut down.')
