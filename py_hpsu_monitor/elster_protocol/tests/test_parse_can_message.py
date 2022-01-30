import can

from ..elster_frame import (
    ElsterGenericFrame,
    ElsterReadRequestFrame,
    ElsterReadResponseFrame,
    ElsterWriteFrame,
)
from ..parse_can_message import parse_can_message


def test_parse_read_request_message():
    elster_frame = parse_can_message(
        can.Message(
            timestamp=1000000000,
            arbitration_id=0x680,
            data=b"\x31\x00\xFA\x00\x0E",
        )
    )

    assert isinstance(elster_frame, ElsterReadRequestFrame)
    assert elster_frame.timestamp == 1000000000
    assert elster_frame.sender == 0x680
    assert elster_frame.receiver == 0x180
    assert elster_frame.elster_index == 0x000E


def test_parse_read_response_message():
    elster_frame = parse_can_message(
        can.Message(
            timestamp=1000000000,
            arbitration_id=0x180,
            data=b"\xD2\x00\xFA\x00\x0E\x01\xC3",
        )
    )

    assert isinstance(elster_frame, ElsterReadResponseFrame)
    assert elster_frame.timestamp == 1000000000
    assert elster_frame.sender == 0x180
    assert elster_frame.receiver == 0x680
    assert elster_frame.elster_index == 0x000E
    assert elster_frame.value == 0x01C3


def test_parse_write_message():
    elster_frame = parse_can_message(
        can.Message(
            timestamp=1000000000,
            arbitration_id=0x680,
            data=b"\x30\x00\xFA\x00\x13\x00\x30",
        )
    )

    assert isinstance(elster_frame, ElsterWriteFrame)
    assert elster_frame.timestamp == 1000000000
    assert elster_frame.sender == 0x680
    assert elster_frame.receiver == 0x180
    assert elster_frame.elster_index == 0x0013
    assert elster_frame.value == 0x0030


def test_parse_generic_message():
    elster_frame = parse_can_message(
        can.Message(
            timestamp=1000000000,
            arbitration_id=0x680,
            data=b"\x36\x00\xFA\xDE\xAD\xBE\xEF",
        )
    )

    assert isinstance(elster_frame, ElsterGenericFrame)
    assert elster_frame.timestamp == 1000000000
    assert elster_frame.sender == 0x680
    assert elster_frame.receiver == 0x180
    assert elster_frame.frame_type == 0x06
    assert elster_frame.payload == b"\xDE\xAD\xBE\xEF"
