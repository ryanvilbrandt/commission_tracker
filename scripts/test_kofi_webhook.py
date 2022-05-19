import os
from json import dumps
from time import ctime
from uuid import uuid4

from faker import Faker
from requests import post

from src.utils import load_config


def create_fake_commission():
    fake = Faker()
    config = load_config()
    host, port = config.get("Settings", "host"), config.getint("Settings", "port")
    r = post(f"http://{host}:{port}/kofi_webhook", data={
        "data": dumps({
            "message_id": str(uuid4()),
            "timestamp": ctime(),
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
        })
    })
    print(r)


if __name__ == "__main__":
    if not os.path.isdir("src"):
        os.chdir("..")
    for _ in range(1):
        create_fake_commission()
