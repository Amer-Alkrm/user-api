from datetime import datetime
from os import environ

import sqlalchemy
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker

from enums import Degree, Gender, IntEnum, State

# Database Connection
DATABASE_URL = 'postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'.format(
    **environ)

engine = sqlalchemy.create_engine(DATABASE_URL)
Session = sessionmaker(engine)
metadata = sqlalchemy.MetaData()
metadata.bind = engine

new_uuid = sqlalchemy.text('uuid_generate_v4()')
now = datetime.utcnow
new_time = dict(default=now, server_default=sqlalchemy.func.now())


addresses = Table(
    'address',
    metadata,
    Column('id', UUID(as_uuid=True),
           server_default=new_uuid, primary_key=True),
    Column('address', String, nullable=False),

    Column('street', String, nullable=False),
    Column('apartment_number', Integer, nullable=False),
    Column('state', IntEnum(State), nullable=False, index=True),
    Column('zip_code', Integer),
    Column('created_at', DateTime, nullable=False, **new_time),
    Column('updated_at', DateTime, nullable=False, onupdate=now, **new_time),
    UniqueConstraint('street', 'apartment_number',
                     name='address_street_apartment_number_key')
)


stakeholders = Table(
    'stakeholders',
    metadata,
    Column('id', UUID(as_uuid=True), server_default=new_uuid,
           primary_key=True, nullable=False),
    Column('email', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('created_by_email', String, nullable=True),
    Column('is_admin', Boolean, nullable=False, index=True),
    Column('created_at', DateTime, nullable=False, **new_time),
    Column('updated_at', DateTime, nullable=False, onupdate=now, **new_time)
)

users = Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), server_default=new_uuid,
           primary_key=True, nullable=False),
    Column('address_id', ForeignKey(
        addresses.c.id, name='users_address_id_fkey'), nullable=False),
    Column('user_name', String, nullable=False),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('age', Integer, nullable=False, index=True),
    Column('degree', IntEnum(Degree), nullable=False, index=True),
    Column('created_by_email', String, nullable=False),
    Column('gender', IntEnum(Gender), nullable=False, index=True),
    Column('email', String, nullable=False),
    Column('created_at', DateTime, nullable=False, **new_time),
    Column('updated_at', DateTime, nullable=False, onupdate=now, **new_time),
    UniqueConstraint('first_name', 'last_name', 'age', 'email',
                     name='users_first_name_last_name_age_email_key')
)
