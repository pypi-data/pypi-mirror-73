from __future__ import annotations
from beginnerpy.challenges.adventure_game.game import Player, Room, Item
from typing import Optional


def find_the_holy_grail(player: Player, previous_room: Optional[Room] = None) -> Optional[Item]:
    if player.room.items and player.room.items[0].item_type == "holy_grail":
        return player.room.items[0]

    room = player.room
    for door in player.room.doors:
        if door.to is previous_room:
            continue

        if door.locked:
            for item in room.items:
                if item.item_type == door.key:
                    player.pickup(item)
                    player.use(item, door)
                    break

        player.move(door)
        item = find_the_holy_grail(player, room)
        if item:
            return item
        player.move_to_room(room)
