import asyncio
from typing import Any, List, Optional

import asyncio_mqtt
import can

from ..config import DefaultRegisterConfiguration, MqttConfig, RegisterConfiguration
from ..elster_protocol.elster_frame import ElsterFrame
from ..elster_protocol.register_types import (
    RegisterDefinition,
    RegisterValue,
    WritableRegisterDefinition,
)
from ..utils.publish_subscribe_topic import PublishSubscribeTopic
from ..utils.shutting_down import shutting_down
from ..workers.elster_canbus_reader import read_elster_canbus
from ..workers.elster_canbus_writer import write_elster_canbus
from ..workers.elster_frame_logger import log_elster_frames
from ..workers.elster_register_canbus_poller import (
    RegisterPollingConfiguration,
    poll_elster_registers_canbus,
)
from ..workers.elster_register_logger import log_elster_registers
from ..workers.elster_register_mqtt_listener import mqtt_listen_for_elster_registers
from ..workers.elster_register_mqtt_logger import mqtt_log_elster_registers


async def run_monitor_canbus(
    can_interface: str,
    sender_id: int,
    mqtt_config: MqttConfig,
    default_register_configuration: DefaultRegisterConfiguration,
    log_frames: bool = False,
    log_registers: bool = False,
    register_configurations: List[RegisterConfiguration] = [],
    register_definitions: List[RegisterDefinition] = [],
):
    elster_frames: PublishSubscribeTopic[ElsterFrame] = PublishSubscribeTopic()
    written_register_values: PublishSubscribeTopic[
        RegisterValue[Any, WritableRegisterDefinition]
    ] = PublishSubscribeTopic()

    register_configurations_by_index = {
        register_configuration.elster_index: register_configuration
        for register_configuration in register_configurations
    }

    polling_configurations = [
        create_register_polling_configuration(
            register_definition=register_definition,
            register_configuration=register_configurations_by_index.get(
                register_definition.elster_index
            ),
            default_register_configuration=default_register_configuration,
        )
        for register_definition in register_definitions
    ]

    with shutting_down(
        can.Bus(channel=can_interface, bustype="socketcan", receive_own_messages=True)
    ) as bus:
        async with asyncio_mqtt.Client(
            hostname=mqtt_config.broker.hostname,
            port=int(mqtt_config.broker.port) if mqtt_config.broker.port else 1883,
            username=mqtt_config.broker.username,
            password=mqtt_config.broker.password,
        ) as mqtt_client:
            await asyncio.gather(
                log_elster_frames(topic=elster_frames) if log_frames else async_noop(),
                log_elster_registers(
                    topic=elster_frames, register_definitions=register_definitions
                )
                if log_registers
                else async_noop(),
                mqtt_log_elster_registers(
                    elster_frames=elster_frames,
                    mqtt_client=mqtt_client,
                    mqtt_config=mqtt_config,
                    register_definitions=register_definitions,
                )
                if mqtt_config.enabled
                else async_noop(),
                mqtt_listen_for_elster_registers(
                    written_register_values=written_register_values,
                    mqtt_client=mqtt_client,
                    mqtt_config=mqtt_config,
                    register_definitions=register_definitions,
                )
                if mqtt_config.enabled
                else async_noop(),
                read_elster_canbus(topic=elster_frames, bus=bus),
                poll_elster_registers_canbus(
                    bus=bus,
                    polling_configurations=polling_configurations,
                    sender_id=sender_id,
                ),
                write_elster_canbus(
                    bus=bus,
                    sender_id=sender_id,
                    written_register_values=written_register_values,
                ),
            )


async def async_noop():
    pass


def create_register_polling_configuration(
    register_definition: RegisterDefinition,
    register_configuration: Optional[RegisterConfiguration],
    default_register_configuration: DefaultRegisterConfiguration,
) -> RegisterPollingConfiguration:
    return RegisterPollingConfiguration(
        register_definition=register_definition,
        enabled=register_configuration.polling_enabled
        if register_configuration and register_configuration.polling_enabled is not None
        else default_register_configuration.polling_enabled,
        interval=register_configuration.polling_interval
        if register_configuration
        and register_configuration.polling_interval is not None
        else default_register_configuration.polling_interval,
    )
