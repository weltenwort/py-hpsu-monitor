from typing import List

from .register_types import NumberRegisterDefinition, BaseRegisterDefinition


register_definitions: List[BaseRegisterDefinition] = [
    NumberRegisterDefinition(
        elster_index=0x000E,
        name="t_dhw",
        label="T-WW",
        description="Angezeigt wird die aktuelle Temperatur des Warmwasserspeichers in C. Sollte keine Warmwasserfunktion aktiviert sein, wird --- angezeigt.",
        factor=0.1,
        unit="°C",
    ),
    NumberRegisterDefinition(
        elster_index=0x01D6,
        name="t_hs",
        label="T-WE",
        description="Angezeigt wird die aktuelle Vorlauftemperatur (TVBH) des Waermeerzeugers in C",
        factor=0.1,
        unit="°C",
    ),
    NumberRegisterDefinition(
        elster_index=0x091C,
        name="qboh",
        label="EHS für DHW",
        description="Angezeigt wird die Waermemenge des zusaetzlichen Waermeerzeugers fuer die Warmwasserbereitung in kWh",
        unit="Wh",
    ),
    NumberRegisterDefinition(
        elster_index=0xC0F9,
        name="ehs",
        label="EHS",
        description="Aktuelle Leistung des Backup-Heaters in kW",
        unit="W",
    ),
]


register_definitions_by_index = {
    definition.elster_index: definition for definition in register_definitions
}
