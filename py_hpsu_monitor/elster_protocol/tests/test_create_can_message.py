from ..create_can_message import create_can_message
from ..elster_frame import ElsterGenericFrame, ElsterReadRequestFrame, ElsterWriteFrame


def test_create_write_can_message():
    can_message = create_can_message(
        ElsterWriteFrame(
            timestamp=1000000000,
            sender=0x680,
            receiver=0x180,
            elster_index=0x0013,
            value=48,
        )
    )

    assert can_message.arbitration_id == 0x680  # type: ignore
    assert can_message.data == b"\x30\x00\xFA\x00\x13\x00\x30"


def test_create_read_request_can_message():
    can_message = create_can_message(
        ElsterReadRequestFrame(
            timestamp=1000000000, sender=0x680, receiver=0x180, elster_index=0x000E
        )
    )

    assert can_message.arbitration_id == 0x680  # type: ignore
    assert can_message.data == b"\x31\x00\xFA\x00\x0E"


def test_create_generic_can_message():
    can_message = create_can_message(
        ElsterGenericFrame(
            timestamp=1000000000,
            sender=0x680,
            receiver=0x180,
            frame_type=0x06,
            payload=b"\xDE\xAD\xBE\xEF",
        )
    )

    assert can_message.arbitration_id == 0x680  # type: ignore
    assert can_message.data == b"\x36\x00\xFA\xDE\xAD\xBE\xEF"
