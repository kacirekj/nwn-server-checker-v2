import datetime
from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


@dataclass
class ModuleInfo(Base):
    __tablename__ = 'module_info_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    ip: Mapped[str] = mapped_column(nullable=False)
    port: Mapped[int] = mapped_column(nullable=False)
    players: Mapped[int] = mapped_column(nullable=True)
    updated: Mapped[datetime.datetime] = mapped_column(nullable=True)


@dataclass
class ModulePresence(Base):
    __tablename__ = 'module_presence_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    module_info_id: Mapped[int] = mapped_column(ForeignKey("module_info_table.id"), nullable=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(nullable=False)
    players: Mapped[int] = mapped_column(nullable=False)


@dataclass
class Property(Base):
    __tablename__ = 'property_table'
    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(nullable=True)


@dataclass
class DiscussionItem(Base):
    __tablename__ = 'discussion_item_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(nullable=True)
    created: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)
    ip: Mapped[str] = mapped_column(nullable=True)
