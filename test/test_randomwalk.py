# -*- coding: utf-8 -*-

# FLEDGE_BEGIN
# See: http://fledge.readthedocs.io/
# FLEDGE_END

from unittest.mock import patch
import pytest

from python.fledge.plugins.south.randomwalk import randomwalk

__author__ = "Bill Hunt"
__copyright__ = "Copyright (c) 2019 Dianomic Systems"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

config = randomwalk._DEFAULT_CONFIG


def test_plugin_contract():
    # Evaluates if the plugin has all the required methods
    assert callable(getattr(randomwalk, 'plugin_info'))
    assert callable(getattr(randomwalk, 'plugin_init'))
    assert callable(getattr(randomwalk, 'plugin_poll'))
    assert callable(getattr(randomwalk, 'plugin_shutdown'))
    assert callable(getattr(randomwalk, 'plugin_reconfigure'))


def test_plugin_info():
    assert randomwalk.plugin_info() == {
        'name': 'RandomWalk Poll plugin',
        'version': '1.8.1',
        'mode': 'poll',
        'type': 'south',
        'interface': '1.0',
        'config': config
    }


def test_plugin_init():
    expected_config = randomwalk.plugin_init(config)
    expected_config['lastValue'] = None
    actual_config = config
    actual_config['lastValue'] = None
    assert expected_config == actual_config


@pytest.mark.skip(reason="To be implemented")
def test_plugin_poll():
    pass


@pytest.mark.skip(reason="To be implemented")
def test_plugin_reconfigure():
    pass


def test_plugin_shutdown():
    with patch.object(randomwalk._LOGGER, 'info') as patch_logger_info:
        randomwalk.plugin_shutdown(config)
    patch_logger_info.assert_called_once_with('randomwalk plugin shut down.')
