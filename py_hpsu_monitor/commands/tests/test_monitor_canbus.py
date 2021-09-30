from ...config import DefaultRegisterConfiguration, RegisterConfiguration
from ...elster_protocol.register_types import NumberSensorRegisterDefinition
from ..monitor_canbus import create_register_polling_configuration


def test_create_register_polling_configuration_with_overrides():
    polling_configuration = create_register_polling_configuration(
        register_definition=NumberSensorRegisterDefinition(
            elster_index=0x0001, name="test-register", owner_id=0x1000
        ),
        register_configuration=RegisterConfiguration(
            elster_index=0x0001, polling_enabled=False, polling_interval=90.0
        ),
        default_register_configuration=DefaultRegisterConfiguration(),
    )

    assert polling_configuration.register_definition.elster_index == 0x0001
    assert polling_configuration.enabled is False
    assert polling_configuration.interval == 90.0


def test_create_register_polling_configuration_with_empty_overrides():
    polling_configuration = create_register_polling_configuration(
        register_definition=NumberSensorRegisterDefinition(
            elster_index=0x0001, name="test-register", owner_id=0x1000
        ),
        register_configuration=RegisterConfiguration(elster_index=0x0001),
        default_register_configuration=DefaultRegisterConfiguration(),
    )

    assert polling_configuration.register_definition.elster_index == 0x0001
    assert polling_configuration.enabled is True
    assert polling_configuration.interval == 60.0


def test_create_register_polling_configuration_without_overrides():
    polling_configuration = create_register_polling_configuration(
        register_definition=NumberSensorRegisterDefinition(
            elster_index=0x0001, name="test-register", owner_id=0x1000
        ),
        register_configuration=None,
        default_register_configuration=DefaultRegisterConfiguration(),
    )

    assert polling_configuration.register_definition.elster_index == 0x0001
    assert polling_configuration.enabled is True
    assert polling_configuration.interval == 60.0
