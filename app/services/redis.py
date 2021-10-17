
from os import getenv

from redis import Redis
from sqlalchemy.engine.row import LegacyRow

redis_client = Redis(host=getenv('REDIS_HOST'), port=getenv(
    'REDIS_PORT'), charset="utf-8", decode_responses=True)


def redis_send_items(user_key: str, user_items: list) -> None:
    for row in user_items:
        row = dict(row)
        row['id'] = str(row['id'])
        row['address_id'] = str(row['address_id'])
        row['created_at'] = str(row['created_at'])
        row['updated_at'] = str(row['updated_at'])
        redis_client.xadd(user_key, row)


def redis_send_item(user_key: str, user_items: LegacyRow) -> None:
    row = dict(user_items)
    row['id'] = str(row['id'])
    row['address_id'] = str(row['address_id'])
    row['created_at'] = str(row['created_at'])
    row['updated_at'] = str(row['updated_at'])
    redis_client.xadd(user_key, row)


def redis_decode_items(user_data: list) -> list:
    user_final_data = []
    for item in user_data:
        user_final_data.append(item[1])
    return user_final_data
