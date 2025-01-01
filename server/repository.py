from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

import context
from model import ModuleInfo, Property, ModulePresence, DiscussionItem


# Discussion item


def get_discussion_items() -> List[DiscussionItem]:
    session = context.scoped_factory()
    q = select(DiscussionItem).order_by(DiscussionItem.created.desc())
    return session.scalars(q).all()


def upsert_discussion_items(discussion_items: List[DiscussionItem]) -> List[DiscussionItem]:
    session: Session = context.scoped_factory()
    fresh_items = []
    for items in discussion_items:
        fresh_item = session.merge(items)
        fresh_items.append(fresh_item)
    session.flush()
    return fresh_items


def delete_discussion_items(ids):
    context.scoped_factory().query(DiscussionItem).where(DiscussionItem.id.in_(ids)).delete()


# Module info


def get_module_infos(ids=None, name=None) -> List[ModuleInfo]:
    session = context.scoped_factory()
    q = select(ModuleInfo)
    if name is not None:
        q = q.where(ModuleInfo.name.like(f'%{name}%'))
    if ids:
        q = q.where(ModuleInfo.id.in_(ids))
    return session.scalars(q).all()


def upsert_module_infos(module_infos: List[ModuleInfo]):
    session: Session = context.scoped_factory()
    fresh_module_infos = []
    for module_info in module_infos:
        fresh_module_info = session.merge(module_info)
        fresh_module_infos.append(fresh_module_info)
    session.flush()
    return fresh_module_infos


def delete_module_info(ids):
    context.scoped_factory().query(ModuleInfo).where(ModuleInfo.id.in_(ids)).delete()


# Module presence


def get_module_presences(ids=None, module_info_id=None, timestamp_min=None) -> List[ModulePresence]:
    session = context.scoped_factory()
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
    session: Session = context.scoped_factory()
    fresh_module_presences = []
    for module_presence in module_presences:
        fresh_module_presence = session.merge(module_presence)
        fresh_module_presences.append(fresh_module_presence)
    session.flush()
    return fresh_module_presences


# Property


def get_properties(keys=None) -> List[ModuleInfo]:
    session = context.scoped_factory()
    q = select(Property)
    if keys:
        q = q.where(Property.key.in_(keys))
    return session.scalars(q).all()


def upsert_properties(properties: List[Property]):
    session: Session = context.scoped_factory()
    for property in properties:
        session.merge(property)
    session.flush()
    return properties



