from unittest.mock import MagicMock

import pytest
from flask import Response

from common.agent_plugins import AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.puppet import PluginRegistry


class StubIslandAPIClient:
    def __init__(self, status: int):
        self._status = status

    def get_agent_plugin(self, _, __):
        return Response(status=self._status)


@pytest.fixture
def stub_plugin_source_extractor():
    return MagicMock()


@pytest.fixture
def stub_plugin_loader():
    return MagicMock()


def test_get_plugin_not_found(plugin_source_extractor, plugin_loader):
    plugin_registry = PluginRegistry(
        StubIslandAPIClient(status=404), plugin_source_extractor, plugin_loader
    )

    with pytest.raises(UnknownPluginError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


# modify when plugin architecture is fully implemented
def test_get_plugin_not_implemented(plugin_source_extractor, plugin_loader):
    plugin_registry = PluginRegistry(
        StubIslandAPIClient(status=200), plugin_source_extractor, plugin_loader
    )

    with pytest.raises(NotImplementedError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


def test_get_plugin_unexpected_response(plugin_source_extractor, plugin_loader):
    plugin_registry = PluginRegistry(
        StubIslandAPIClient(status=100), plugin_source_extractor, plugin_loader
    )

    with pytest.raises(Exception):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)
