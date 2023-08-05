"""Data Plugins.

This module handles the initialization of standard and custom data plugins,
and maintains a global registry of plugin protocols vs. plugin instances.
"""
import importlib

from qtpyvcp import PLUGINS
from qtpyvcp.utilities.logger import getLogger
from qtpyvcp.plugins.plugin import DataPlugin, DataChannel

LOG = getLogger(__name__)


def loadDataPlugins(plugins):
    """Load data plugins from list of object references.

    Args:
        plugins (dict) : List of dictionaries.
    """

    for protocol, plugin_dict in plugins.items():

        try:
            object_ref = plugin_dict['provider']
        except KeyError:
            raise ValueError("No provider class specified for %s plugin" % protocol)

        args = plugin_dict.get('args', [])
        kwargs = plugin_dict.get('kwargs', {})

        LOG.debug("Loading plugin '{}' from '{}'".format(protocol, object_ref))

        modname, sep, clsname = object_ref.partition(':')

        try:
            plugin = getattr(importlib.import_module(modname), clsname)
        except Exception:
            LOG.critical("Failed to import data plugin.")
            raise

        assert issubclass(plugin, DataPlugin), "Not a valid plugin, must be a DataPlugin subclass."

        if protocol in PLUGINS:
            LOG.warning("Replacing {} with {} for use with protocol {}"
                        .format(PLUGINS[protocol].__class__,
                                plugin,
                                protocol)
                        )

        try:
            obj = plugin(*args, **kwargs)
            obj.setLogLevel(plugin_dict.get('log_level'))
            PLUGINS[protocol] = obj
        except TypeError:
            LOG.critical("Error initializing plugin: {}(*{}, **{})".format(object_ref, args, kwargs))
            raise


def getPlugin(protocol):
    """Get data plugin instance from a protocol name.

    Args:
        protocol (str) : The protocol of the plugin to retrieve.

    Returns:
        A plugin instance, or None.

    Raises:
        NoSuchPlugin if the no plugin for ``protocol`` is found.
    """
    try:
        return PLUGINS[protocol]
    except KeyError:
        raise ValueError("Failed to find plugin for '{}' protocol.".format(protocol))
