from core import boot
from core.db import get_session
from core.db.models import Item

# Start
boot()

for session in get_session():
    # hako_vn = Item(
    #     name="Novel", url="https://docln.net/", username="vyngt", password="abc"
    # )
    # session.add_all([hako_vn])
    # session.commit()
    for item in session.query(Item).all():
        print(item)
        print(item.id)
        print(item.name, item.username, item.url)

    print("-----end-----")
