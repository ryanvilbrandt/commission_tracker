import os
from json import dumps
from time import strftime
from uuid import uuid4

from faker import Faker
from requests import post

from src.utils import load_config

if not os.path.isdir("src"):
    os.chdir("..")
config = load_config()
HOST, PORT = config.get("Settings", "host"), config.getint("Settings", "port")


def create_fake_commission():
    fake = Faker()
    url = f"http://{HOST}:{PORT}/kofi_webhook"
    print(url)
    payload = {
        "message_id": str(uuid4()),
        "timestamp": strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": "Commission",
        "is_public": True,
        "from_name": fake.name(),
        "message": fake.text(20),
        "amount": "{:.2f}".format(fake.pyfloat(min_value=1, max_value=99.99)),
        # "url": f"https://ko-fi.com/Home/CoffeeShop?txid={uuid4()}&readToken={uuid4()}",
        "url": "https://youtu.be/dQw4w9WgXcQ?autoplay=1",
        "email": fake.email(),
        "currency": "USD",
        "is_subscription_payment": False,
        "is_first_subscription_payment": False,
        "kofi_transaction_id": str(uuid4()),
        "verification_token": os.environ["KOFI_VERIFICATION_TOKEN"],
        "shop_items": None,
        "tier_name": None,
    }
    data = {"data": dumps(payload)}
    print(data)
    r = post(url, data=data)
    print(r)


def test_note():
    r = post(f"http://{HOST}:{PORT}/add_note", data={
        "commission_id": 85,
        "user_id": 4,
        "text": "I like reading about cats dying!"
    })
    print(r)


if __name__ == "__main__":
    for _ in range(5):
        create_fake_commission()
    # test_note()
