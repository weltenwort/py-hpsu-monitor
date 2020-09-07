import struct

import can

from .elster_frame import (
    ElsterFrame,
    ElsterGenericFrame,
    ElsterReadRequestFrame,
    ElsterReadResponseFrame,
    ElsterFrameType,
)


def parse_can_message(message: can.Message) -> ElsterFrame:
    sender = message.arbitration_id
    data = message.data
    receiver = (data[0] & 0xF0) * 8 + (data[1] & 0x0F)
    frame_type = data[0] & 0x0F
    is_extended = data[2] == 0xFA
    value = 0

    if is_extended:
        elster_index = struct.unpack(">H", data[3:5])[0]
        if len(data) == 7:
            value = struct.unpack(">h", data[5:7])[0]
    else:
        elster_index = data[2]
        if len(data) >= 5:
            value = struct.unpack(">h", data[3:5])[0]

    if frame_type == ElsterFrameType.READ_REQUEST:
        return ElsterReadRequestFrame(
            timestamp=message.timestamp,
            sender=sender,
            receiver=receiver,
            elster_index=elster_index,
        )
    elif frame_type == ElsterFrameType.READ_RESPONSE:
        return ElsterReadResponseFrame(
            timestamp=message.timestamp,
            sender=sender,
            receiver=receiver,
            elster_index=elster_index,
            value=value,
        )
    else:
        return ElsterGenericFrame(
            timestamp=message.timestamp,
            sender=sender,
            receiver=receiver,
            frame_type=frame_type,
            payload=bytes(data[3:]),
        )
