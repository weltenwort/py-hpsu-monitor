from pydantic import BaseModel

from ..config import MqttConfig


def get_write_topic(mqtt_config: MqttConfig):
    return mqtt_config.write_topic_template.format(
        device_id=mqtt_config.device.id, platform="writable-sensor"
    )


def parse_write_payload(payload: bytes):
    return NumberMqttWriteMessagePayload.parse_raw(payload)


class NumberMqttWriteMessagePayload(BaseModel):
    kind: str = "number"
    register_name: str
    value: float
