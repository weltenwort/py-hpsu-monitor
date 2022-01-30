from pathlib import Path

from ...elster_protocol.register_types import (
    NumberSensorRegisterDefinition,
    NumberSettingRegisterDefinition,
)
from ..register_definitions import load_register_definitions_from_file_path

test_register_definitions_path = (
    Path(__file__).resolve().parent / "data" / "test_register_definitions.toml"
)
default_register_definitions_path = (
    Path(__file__).resolve().parent.parent / "register_definitions.toml"
)


def test_load_number_register_definitions_from_file_path():
    register_definitions = load_register_definitions_from_file_path(
        test_register_definitions_path
    ).register_definitions

    assert (
        NumberSensorRegisterDefinition(
            elster_index=0x0001,
            factor=0.123,
            name="test-number-register",
            owner_id=0x180,
            unit="test-unit",
        )
        in register_definitions
    )

    assert (
        NumberSensorRegisterDefinition(
            elster_index=0x0002,
            factor=1.0,
            name="test-number-register-without-factor",
            owner_id=0x180,
            unit="test-unit",
        )
        in register_definitions
    )

    assert (
        NumberSettingRegisterDefinition(
            elster_index=0x0003,
            name="test-writable-number-register",
            owner_id=0x180,
            unit="test-unit",
        )
        in register_definitions
    )


def test_load_default_number_register_definitions_from_file_path():
    register_definitions = load_register_definitions_from_file_path(
        default_register_definitions_path
    ).register_definitions

    assert len(register_definitions) == 30
