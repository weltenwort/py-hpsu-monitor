from pathlib import Path

from ...elster_protocol.register_types import (
    ReadonlyNumberRegisterDefinition,
    WritableNumberRegisterDefinition,
)
from ..register_definitions import load_register_definitions_from_file_path

test_data_dir = Path(__file__).resolve().parent / "data"


def test_load_number_register_definitions_from_file_path():
    register_definitions = load_register_definitions_from_file_path(
        test_data_dir / "test_register_definitions.toml"
    ).register_definitions

    assert (
        ReadonlyNumberRegisterDefinition(
            elster_index=0x0001,
            factor=0.123,
            name="test-number-register",
            owner_id=0x180,
            unit="test-unit",
        )
        in register_definitions
    )

    assert (
        ReadonlyNumberRegisterDefinition(
            elster_index=0x0002,
            factor=1.0,
            name="test-number-register-without-factor",
            owner_id=0x180,
            unit="test-unit",
        )
        in register_definitions
    )

    assert (
        WritableNumberRegisterDefinition(
            elster_index=0x0003,
            name="test-writable-number-register",
            owner_id=0x180,
            unit="test-unit",
        )
        in register_definitions
    )
