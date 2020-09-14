import textwrap

from pydantic import ValidationError
import pytest

from ..config import load_configuration_from_text


def test_load_default_configuration_from_text():
    configuration = load_configuration_from_text("")

    assert configuration.can_bus.sender_id == 0x680
    assert configuration.can_bus.default_register_configuration.polling_interval == 60
    assert configuration.can_bus.register_configuration == []
    assert configuration.mqtt.broker.hostname == "localhost"


def test_load_configuration_from_text():
    configuration = load_configuration_from_text(
        textwrap.dedent(
            """\
        [can_bus]
        sender_id = 0x900

        [can_bus.default_register_configuration]
        polling_enabled = false
        polling_interval = 90.0

        [[can_bus.register_configuration]]
        elster_index = 0x000E
        polling_interval = 30
        """
        )
    )

    assert configuration.can_bus.sender_id == 0x900
    assert configuration.can_bus.default_register_configuration.polling_enabled == False
    assert configuration.can_bus.default_register_configuration.polling_interval == 90.0
    assert configuration.can_bus.register_configuration[0].elster_index == 0x000E
    assert configuration.can_bus.register_configuration[0].polling_interval == 30


def test_fail_to_load_configuration_from_text():
    with pytest.raises(ValidationError):
        load_configuration_from_text(
            textwrap.dedent(
                """\
            [can_bus]
            sender_id = 0x900

            [[can_bus.register_configuration]]
            polling_interval = 30
            """
            )
        )
