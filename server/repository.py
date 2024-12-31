from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from model import ModulePresence
from __main__ import scoped_factory

from model import ModuleInfo, Property


# Module info


def get_module_infos(ids=None, name=None) -> List[ModuleInfo]:
    session = scoped_factory()
    q = select(ModuleInfo)
    if name is not None:
        q = q.where(ModuleInfo.name.like(f'%{name}%'))
    if ids:
        q = q.where(ModuleInfo.id.in_(ids))
    return session.scalars(q).all()


def upsert_module_infos(module_infos: List[ModuleInfo]):
    session: Session = scoped_factory()
    fresh_module_infos = []
    for module_info in module_infos:
        fresh_module_info = session.merge(module_info)
        fresh_module_infos.append(fresh_module_info)
    session.flush()
    return fresh_module_infos


def delete_module_info(ids):
    scoped_factory().query(ModuleInfo).where(ModuleInfo.id.in_(ids)).delete()


# Module presence


def get_module_presences(ids=None, module_info_id=None, timestamp_min=None) -> List[ModulePresence]:
    session = scoped_factory()
    q = select(ModulePresence)
    if module_info_id is not None:
        q = q.where(ModulePresence.module_info_id == module_info_id)
    if ids:
        q = q.where(ModulePresence.id.in_(ids))
    if timestamp_min:
        q = q.where(ModulePresence.timestamp > timestamp_min)
    q.order_by(ModulePresence.timestamp.asc())
    return session.scalars(q).all()


def upsert_module_presences(module_presences: List[ModulePresence]):
    session: Session = scoped_factory()
    fresh_module_presences = []
    for module_presence in module_presences:
        fresh_module_presence = session.merge(module_presence)
        fresh_module_presences.append(fresh_module_presence)
    session.flush()
    return fresh_module_presences


# Property


def get_properties(keys=None) -> List[ModuleInfo]:
    session = scoped_factory()
    q = select(Property)
    if keys:
        q = q.where(Property.key.in_(keys))
    return session.scalars(q).all()


def upsert_properties(properties: List[Property]):
    session: Session = scoped_factory()
    for property in properties:
        session.merge(property)
    session.flush()
    return properties



