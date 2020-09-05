import struct
from typing import Union

import can

from .elster_frame import (
    ElsterGenericFrame,
    ElsterReadRequestFrame,
)


def create_can_message(
    frame: Union[ElsterReadRequestFrame, ElsterGenericFrame]
) -> can.Message:
    header = struct.pack(
        ">BBB",
        (frame.frame_type & 0xF) | ((frame.receiver >> 3) & 0xF0),
        frame.receiver & 0x7F,
        0xFA,
    )

    if isinstance(frame, ElsterReadRequestFrame):
        body = struct.pack(">H", frame.elster_index)
    else:
        body = frame.payload

    data = b"".join([header, body])

    return can.Message(arbitration_id=frame.sender, data=data, is_extended_id=False)
