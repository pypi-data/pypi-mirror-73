from typing import List, Tuple, Optional
from beginnerpy.challenges.adventure_game.game import Item, Room, Player
import random


def generate_items() -> List[Item]:
    items = {
        "Gold key": "gold_key",
        "Silver key": "silver_key",
        "Copper key": "copper_key",
        "Spoon": "spoon",
        "Excaliber": "sword",
        "Long Sword": "sword",
        "Python": "python"
    }
    return [
        Item(name, item_type)
        for name, item_type in random.sample(
            items.items(),
            random.randint(0, 3)
        )
    ]


def generate_room(depth: int, entry_room: Optional[Room]) -> Room:
    items = generate_items()
    keys: List[Optional[Item]] = [item for item in items if "key" in item.item_type]
    room = Room(entry_room, items, depth)

    if depth:
        for i in range(random.randint(1, 3)):
            new_room = generate_room(depth - 1, room)
            key = random.choice(keys + [None])
            if key in keys:
                keys.remove(key)
            room._connect_room(new_room, key)

    return room


def add_holy_grail(room: Room) -> Item:
    if room.depth == 0:
        grail = Item("Holy Grail", "holy_grail")
        room._connect_room(Room(room, [grail], -1), None)
        return grail

    return add_holy_grail(random.choice(room.doors).to)


def generate_game(depth: int) -> Tuple[Player, Item]:
    room = generate_room(depth, None)
    grail = add_holy_grail(room)
    return Player(room), grail
