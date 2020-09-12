from typing import List

from .register_types import NumberRegisterDefinition, BaseRegisterDefinition


register_definitions: List[BaseRegisterDefinition] = [
    NumberRegisterDefinition(
        elster_index=0x000E,
        name="temp-speicher-ist-t-dhw",
        factor=0.1,
        unit="°C",
    ),
    NumberRegisterDefinition(
        elster_index=0x01D6,
        name="temp-vorlauf-ist-t-hs",
        factor=0.1,
        unit="°C",
    ),
    NumberRegisterDefinition(
        elster_index=0x091C,
        name="energie-aufnahme-ehs-ww",
        unit="kWh",
    ),
    NumberRegisterDefinition(
        elster_index=0x0920,
        name="energie-aufnahme-ehs-hz",
        unit="kWh",
    ),
    NumberRegisterDefinition(
        elster_index=0xC0F9,
        name="leistung-ehs",
        unit="W",
    ),
]


register_definitions_by_index = {
    definition.elster_index: definition for definition in register_definitions
}
