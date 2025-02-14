from ipaddress import IPv4Address
from uuid import UUID

import pytest
from tests.unit_tests.monkey_island.cc.models.test_agent import AGENT_ID

from common import OperatingSystem
from common.agent_events import PingScanEvent

PING_EVENT = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address("1.1.1.1"),
    timestamp=1664371327.4067292,
    response_received=True,
    os=OperatingSystem.LINUX,
)

PING_OBJECT_DICT = {
    "source": UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10"),
    "target": IPv4Address("1.1.1.1"),
    "timestamp": 1664371327.4067292,
    "tags": frozenset(),
    "response_received": True,
    "os": OperatingSystem.LINUX,
}

PING_SIMPLE_DICT = {
    "source": "012e7238-7b81-4108-8c7f-0787bc3f3c10",
    "target": "1.1.1.1",
    "timestamp": 1664371327.4067292,
    "tags": [],
    "response_received": True,
    "os": "linux",
}


def test_constructor():
    assert PingScanEvent(**PING_OBJECT_DICT) == PING_EVENT


def test_from_dict():
    assert PingScanEvent(**PING_SIMPLE_DICT) == PING_EVENT


def test_to_dict():
    ping_scan_event = PingScanEvent(**PING_OBJECT_DICT)

    assert ping_scan_event.dict(simplify=True) == PING_SIMPLE_DICT


@pytest.mark.parametrize(
    "key, value",
    [
        ("source", "not-an-uuid"),
        ("source", -1),
        ("timestamp", "not-a-timestamp"),
        ("response_received", "not-a-bool"),
        ("os", 2.1),
        ("os", "bsd"),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = PING_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        PingScanEvent(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("target", "not-a-IPv4Address"),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_type_dict = PING_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(ValueError):
        PingScanEvent(**invalid_type_dict)


def test_optional_os_field():
    none_field_dict = PING_SIMPLE_DICT.copy()
    none_field_dict["os"] = None

    # Raises exception_on_failure
    PingScanEvent(**none_field_dict)


def test_construct__extra_fields_forbidden():
    extra_field_dict = PING_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        PingScanEvent(**extra_field_dict)


def test_ping_scan_event_deserialization_dict():
    serialized_event = PING_EVENT.dict()
    deserialized_event = PingScanEvent(**serialized_event)
    assert deserialized_event == PING_EVENT
