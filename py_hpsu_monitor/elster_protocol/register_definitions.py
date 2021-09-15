from pathlib import Path
from typing import List

from pydantic import BaseModel
import tomlkit

from .register_types import (
    # NumberRegisterDefinition,
    RegisterDefinition,
)


class RegisterDefinitions(BaseModel):
    register_definitions: List[RegisterDefinition] = []


def load_default_register_definitions():
    return RegisterDefinitions()


def load_register_definitions_from_file_path(definition_file_path: Path):
    if not definition_file_path.is_file():
        return load_default_register_definitions()

    return load_register_definitions_from_text(definition_file_path.read_text())


def load_register_definitions_from_text(
    definition_file_text: str,
) -> RegisterDefinitions:
    return RegisterDefinitions.parse_obj(dict(tomlkit.parse(definition_file_text)))


def group_register_definitions_by_index(register_definitions: List[RegisterDefinition]):
    return {definition.elster_index: definition for definition in register_definitions}


def group_register_definitions_by_name(register_definitions: List[RegisterDefinition]):
    return {definition.name: definition for definition in register_definitions}
