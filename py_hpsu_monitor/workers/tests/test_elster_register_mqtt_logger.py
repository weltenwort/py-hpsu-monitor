import asyncio
import json
import mock

import asyncio_mqtt
import pytest

from ...config import MqttBrokerConfig, MqttConfig, MqttDeviceConfig
from ...elster_protocol.register_types import NumberRegisterDefinition
from ...utils.publish_subscribe_topic import PublishSubscribeTopic
from ..elster_register_mqtt_logger import mqtt_log_elster_registers


@pytest.mark.asyncio
async def test_mqtt_logger_publishes_autodiscovery(
    event_loop: asyncio.AbstractEventLoop,
):
    elster_frames_topic = mock.create_autospec(
        PublishSubscribeTopic, instance=True, spec_set=True
    )

    mqtt_client = mock.create_autospec(
        spec=asyncio_mqtt.Client, instance=True, spec_set=True
    )
    mqtt_config = MqttConfig(
        configuration_topic_template="test/sensor/{device_id}/config",
        state_topic_template="test/sensor/{device_id}/state",
        broker=MqttBrokerConfig(hostname="localhost"),
        device=MqttDeviceConfig(
            id="test-device-id",
            model="test-model",
            name="test-name",
            manufacturer="test-manufacturer",
        ),
    )
    register_definitions = [
        NumberRegisterDefinition(
            elster_index=0x0001,
            factor=0.123,
            name="test-number-register",
            owner_id=0x180,
            unit="°C",
        )
    ]

    await mqtt_log_elster_registers(
        elster_frames=elster_frames_topic,
        mqtt_client=mqtt_client,
        mqtt_config=mqtt_config,
        register_definitions=register_definitions,
    )

    mqtt_client.publish.assert_has_calls(
        [
            mock.call(
                topic="test/sensor/test-device-id-test-number-register/config",
                payload=json.dumps(
                    {
                        "name": "test-device-id-test-number-register",
                        "state_topic": "test/sensor/test-device-id-test-number-register/state",
                        "value_template": "{{ value_json.value }}",
                        "device": {
                            "identifiers": ["test-device-id"],
                            "manufacturer": "test-manufacturer",
                            "model": "test-model",
                            "name": "test-name",
                        },
                        "unique_id": "test-device-id-test-number-register",
                        "unit_of_measurement": "°C",
                        "device_class": "temperature",
                        "state_class": "measurement",
                    }
                ),
                retain=True,
            )
        ]
    )
