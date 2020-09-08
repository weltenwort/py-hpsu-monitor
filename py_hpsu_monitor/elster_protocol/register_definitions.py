from typing import List

from .register_types import NumberRegisterDefinition, RegisterDefinition


register_definitions: List[RegisterDefinition] = [
    NumberRegisterDefinition(
        elster_index=0x000E,
        name="t_dhw",
        label="T-WW",
        description="Angezeigt wird die aktuelle Temperatur des Warmwasserspeichers in C. Sollte keine Warmwasserfunktion aktiviert sein, wird --- angezeigt.",
        factor=0.1,
    )
]


register_definitions_by_index = {
    definition.elster_index: definition for definition in register_definitions
}
