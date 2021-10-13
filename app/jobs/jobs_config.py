from os import getenv

default_stakeholder = {'email': getenv('DEF_EMAIL'),
                       'password': getenv('DEF_PASS'),
                       'is_admin': bool(getenv('DEF_ADMIN'))}
