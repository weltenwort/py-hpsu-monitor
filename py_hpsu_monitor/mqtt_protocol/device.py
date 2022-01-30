# pyright: reportUnnecessaryIsInstance=warning
from typing import Any, Dict

from ..elster_protocol.register_types import (
    NumberSensorRegisterDefinition,
    RegisterDefinition,
)


def get_device_class(register_definition: RegisterDefinition) -> Dict[str, Any]:
    unit_of_measurement_attributes = (
        {"unit_of_measurement": register_definition.unit}
        if (isinstance(register_definition, NumberSensorRegisterDefinition))
        else {}
    )
    device_class_attributes = (
        {"device_class": device_class}
        if (
            isinstance(register_definition, NumberSensorRegisterDefinition)
            and (
                device_class := device_class_by_unit.get(register_definition.unit, None)
            )
        )
        else {}
    )
    state_class_attributes = (
        {"state_class": state_class}
        if (
            isinstance(register_definition, NumberSensorRegisterDefinition)
            and (state_class := state_class_by_unit.get(register_definition.unit, None))
        )
        else {}
    )

    return {
        **unit_of_measurement_attributes,
        **device_class_attributes,
        **state_class_attributes,
    }


device_class_by_unit = {
    None: None,
    "°C": "temperature",
    "W": "power",
    "kW": "power",
    "Wh": "energy",
    "kWh": "energy",
    "mbar": "pressure",
}

state_class_by_unit = {
    None: None,
    "°C": "measurement",
    "W": "measurement",
    "kW": "measurement",
    "Wh": "total_increasing",
    "kWh": "total_increasing",
    "mbar": "measurement",
}
