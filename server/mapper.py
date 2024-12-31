from typing import List

from model import ModuleInfo, Property


def to_module_infos(module_infos: List[dict]):
    return [to_to_module_info(to_module_info) for to_module_info in module_infos]


def to_to_module_info(module_info: dict):
    if module_info is None:
        return None
    return ModuleInfo(
        id=module_info.get('id'),
        name=module_info.get('name'),
        ip=module_info.get('ip'),
        port=module_info.get('port'),
        players=module_info.get('players'),
        updated=module_info.get('updated'),
    )


def to_properties(properties: List[dict]):
    return [to_property(property) for property in properties]


def to_property(property: dict):
    if property is None:
        return None
    return Property(
        key=property.get('key'),
        value=property.get('value'),
    )
