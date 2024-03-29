from datetime import datetime
from typing import List

from typer import colors, echo, style

from ..elster_protocol.elster_frame import ElsterFrame, ElsterReadResponseFrame
from ..elster_protocol.register_definitions import group_register_definitions_by_index
from ..elster_protocol.register_types import RegisterDefinition
from ..utils.publish_subscribe_topic import PublishSubscribeTopic


async def log_elster_registers(
    topic: PublishSubscribeTopic[ElsterFrame],
    register_definitions: List[RegisterDefinition],
):
    register_definitions_by_index = group_register_definitions_by_index(
        register_definitions
    )

    async for frame in topic.items():
        if (
            isinstance(frame, ElsterReadResponseFrame)
            and frame.elster_index in register_definitions_by_index
        ):
            register_value = register_definitions_by_index[
                frame.elster_index
            ].parse_elster_frame(frame)

            echo(
                " ".join(
                    [
                        f"[{datetime.utcfromtimestamp(register_value.timestamp)}]",
                        f"Register {style(register_value.register_type.name, fg=colors.CYAN)}:",
                        style(str(register_value.value), bold=True),
                    ]
                )
            )
