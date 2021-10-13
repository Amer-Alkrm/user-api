from uuid import UUID

from pydantic import BaseModel, Field

from enums import Degree, Gender, State, all_enum_to_str


class UserRequestDoc(BaseModel):
    address_id: UUID = Field('Address ID', example='a54304e0-db24-49e7-bbe9-2acec8b0b500',
                             descrption='The address ID must exist in the Address Table.')
    user_name: str = Field('Username', example='ameralkrm',
                           description=('The username of the user which'
                                        + ' will be displayed on the forum.'))
    first_name: str = Field('First Name', example='Amer')
    last_name: str = Field('Last Name', example='Alkrm')
    age: int = Field('Age', example='24',
                     description='The age must be between 10 and 100')
    degree: int = Field('Degree', example='2',
                        descrption=f'Degree: {all_enum_to_str(Degree)}')
    gender: int = Field('Gender', example='1',
                        descrption=f'Gender: {all_enum_to_str(Gender)}')
    email: str = Field('Email', example='example@gmail.com',
                       description='The email address of the user')


class UserResponseDoc(BaseModel):
    id: UUID = Field('User_ID', example='a0e25ba5-74f8-4982-8151-89c01cfcf099',
                     description='The ID of the user (Auto)')
    email: str = Field('Email', example='example@gmail.com',
                       description='The email address of the user')
    user_name: str = Field('Username', example='ameralkrm',
                           description=('The username of the user which'
                                        + ' will be displayed on the forum.'))
    first_name: str = Field('First Name', example='Amer')
    last_name: str = Field('Last Name', example='Alkrm')
    age: int = Field('Age', example='24',
                     description='The age must be between 10 and 100')
    address_id: UUID = Field('Address ID', example='a54304e0-db24-49e7-bbe9-2acec8b0b500',
                             descrption='The address ID must exist in the Address Table.')
    degree: int = Field('Degree', example='2',
                        descrption=f'Degree: {all_enum_to_str(Degree)}')
    created_by_email: str = Field('Created By Email', example='example@gmail.com',
                                  description=('The email address of the stakeholder'
                                               + ' that created this user.'))
    gender: int = Field('Gender', example='1',
                        descrption=f'Gender: {all_enum_to_str(Gender)}')
    created_at: UUID = Field(
        'Created At', example='2021-09-19T12:17:32.655357')
    updated_at: UUID = Field(
        'Updated At', example='2021-09-19T12:17:32.655357')


class AddressRequestDoc(BaseModel):

    address: str = Field('Address', example="Jordan/Az'Zarqa",
                         description='The name of the Address')
    street: str = Field('Street', example='Al-Quds',
                        description='The name of the Street.')
    state: int = Field('State', example='5',
                       description=f'States: {all_enum_to_str(State)}')
    zip_code: int = Field('Zip_Code', example='13115',
                          description='Zipcode of the address, it must not exceed 5 characters.')
    apartment_number: str = Field('Apartment Number', example='12',
                                  description='The number of the apartment.')


class AddressResponseDoc(BaseModel):
    id: UUID = Field(
        'Address ID', example='a0e25ba5-74f8-4982-8151-89c01cfcf099')
    address: str = Field('Address', example="Jordan/Az'Zarqa",
                         description='The name of the Address')
    street: str = Field('Street', example='Al-Quds',
                        description='The name of the Street.')
    state: int = Field('State', example='5',
                       description=f'States: {all_enum_to_str(State)}')
    zip_code: int = Field('Zip_Code', example='13115',
                          description='Zipcode of the address, it must not exceed 5 characters.')
    apartment_number: str = Field('Apartment Number', example='12',
                                  description='The number of the apartment.')
    created_at: UUID = Field(
        'Created At', example='2021-09-19T12:17:32.655357')
    updated_at: UUID = Field(
        'Updated At', example='2021-09-19T12:17:32.655357')


class StakeholderRequestDoc(BaseModel):

    email: str = Field('Email', example='example@gmail.com',
                       description='The email address of the stakeholder')
    password: str = Field('Password', example='password#123',
                          description='The password of the stakeholder')
    created_by_email: int = Field('Created By', example='amer@gmail.com',
                                  description=('It contains the email of the'
                                               + ' admin that created this stakeholder.'))
    is_admin: bool = Field('Is_Admin', example='True',
                           description=('If the stakeholder is an admin'
                                        + ' it is set to True otherwise False.'))


class StackholderResponseDoc(BaseModel):
    id: UUID = Field(
        'Stackholder ID', example='a0e25ba5-74f8-4982-8151-89c01cfcf099')
    email: str = Field('Email', example='example@gmail.com',
                       description='The email address of the stakeholder')
    password: str = Field('Password', example='password#123',
                          description='The password of the stakeholder')
    created_by_email: int = Field('Created By', example='amer@gmail.com',
                                  description=('It contains the email of the admin'
                                               + ' that created this stakeholder.'))
    is_admin: bool = Field('Is_Admin', example='True',
                           description=('If the stakeholder is an admin'
                                        + ' it is set to True otherwise False.'))
    created_at: UUID = Field(
        'Created At', example='2021-09-19T12:17:32.655357')
    updated_at: UUID = Field(
        'Updated At', example='2021-09-19T12:17:32.655357')
