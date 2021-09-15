# pyright: reportUnnecessaryIsInstance=warning
from typing import Any, Dict

from ..elster_protocol.register_types import (
    NumberRegisterDefinition,
    RegisterDefinition,
)


def get_device_class(register_definition: RegisterDefinition) -> Dict[str, Any]:
    if (
        isinstance(register_definition, NumberRegisterDefinition)
        and register_definition.unit
    ):
        device_class = device_class_by_unit.get(register_definition.unit, None)
        state_class = state_class_by_unit.get(register_definition.unit, None)

        return {
            "unit_of_measurement": register_definition.unit,
            **(
                {
                    "device_class": device_class,
                }
                if device_class
                else {}
            ),
            **(
                {
                    "state_class": state_class,
                }
                if state_class
                else {}
            ),
        }

    return {}


device_class_by_unit = {
    "°C": "temperature",
    "W": "power",
    "kW": "power",
    "Wh": "energy",
    "kWh": "energy",
    "mbar": "pressure",
}

state_class_by_unit = {
    "°C": "measurement",
    "W": "measurement",
    "kW": "measurement",
    "Wh": "total_increasing",
    "kWh": "total_increasing",
    "mbar": "measurement",
}
