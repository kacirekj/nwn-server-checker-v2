import importlib

import repository


def reload_properties():
    properties = repository.get_properties()
    constant_module = importlib.import_module('constant')
    for property in properties:
        setattr(constant_module, property.key, property.value)
