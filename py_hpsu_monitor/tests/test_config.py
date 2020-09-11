import textwrap

from pydantic import ValidationError
import pytest

from ..config import load_configuration_from_text


def test_load_default_configuration_from_text():
    configuration = load_configuration_from_text("")

    assert configuration.can_bus.sender_id == 0x680
    assert configuration.can_bus.polling_configuration == []


def test_load_configuration_from_text():
    configuration = load_configuration_from_text(
        textwrap.dedent(
            """\
        [can_bus]
        sender_id = 0x900

        [[can_bus.polling_configuration]]
        elster_index = 0x000E
        interval = 30
        receiver_id = 0x180
        start_delay = 1
        """
        )
    )

    assert configuration.can_bus.sender_id == 0x900
    assert configuration.can_bus.polling_configuration[0].elster_index == 0x000E
    assert configuration.can_bus.polling_configuration[0].interval == 30
    assert configuration.can_bus.polling_configuration[0].receiver_id == 0x180


def test_fail_to_load_configuration_from_text():
    with pytest.raises(ValidationError):
        load_configuration_from_text(
            textwrap.dedent(
                """\
            [can_bus]
            sender_id = 0x900

            [[can_bus.polling_configuration]]
            elster_index = 0x000E
            interval = 30
            """
            )
        )
