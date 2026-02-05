from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    UnicodeText,
    Unicode,
    DateTime
    )

from .meta import Base


__all__ = ['Subject', 'Contact']


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)


Index('subject_name_index', Subject.name, unique=True, mysql_length=255)


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode(255), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id))
    text = Column(UnicodeText, nullable=False)
    created = Column(DateTime, default=datetime.now)


Index('contact_email_index', Contact.email, mysql_length=255)
