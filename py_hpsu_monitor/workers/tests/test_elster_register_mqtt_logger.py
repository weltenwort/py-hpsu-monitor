import json
import mock

import asyncio_mqtt
import pytest

from ...config import MqttBrokerConfig, MqttConfig
from ...utils.publish_subscribe_topic import PublishSubscribeTopic
from ..elster_register_mqtt_logger import mqtt_log_elster_registers


@pytest.mark.asyncio
async def test_mqtt_logger_publishes_autodiscovery():
    elster_frames_topic = PublishSubscribeTopic()
    mqtt_client = mock.create_autospec(
        spec=asyncio_mqtt.Client, instance=True, spec_set=True
    )
    mqtt_config = MqttConfig(
        device_id="test-device-id",
        configuration_topic_template="test/sensor/{device_id}/config",
        state_topic_template="test/sensor/{device_id}/state",
        broker=MqttBrokerConfig(hostname="localhost"),
    )

    await mqtt_log_elster_registers(
        elster_frames=elster_frames_topic,
        mqtt_client=mqtt_client,
        mqtt_config=mqtt_config,
    )

    mqtt_client.publish.assert_has_calls(
        [
            mock.call(
                topic="test/sensor/test-device-id-t_dhw/config",
                payload=json.dumps(
                    {
                        "name": "test-device-id-t_dhw",
                        "state_topic": "test/sensor/test-device-id-t_dhw/state",
                        "unit_of_measurement": "°C",
                    }
                ),
            )
        ]
    )
