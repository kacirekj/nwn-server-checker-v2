from typing import List

from model import Serving
from server.model import ModulePresence, ModuleInfo


def to_module_infos(to_module_infos: List[dict]):
    return [to_to_module_info(to_module_info) for to_module_info in to_module_infos]


def to_to_module_info(to_module_info: dict):
    if to_module_info is None:
        return None
    return ModuleInfo(
        id=to_module_info.get('id'),
        name=to_module_info.get('name'),
        ip=to_module_info.get('ip'),
        port=to_module_info.get('port'),
    )
