from __future__ import annotations
from typing import List, Optional, Tuple
import abc


class Entity(abc.ABC):
    @abc.abstractmethod
    def _apply_item(self, item: Item) -> bool:
        """ Takes an item and returns True if it was applied to the object. """
        return False


class Player:
    def __init__(self, room: Room, bag: Optional[List[Item]] = None):
        self.__bag: List[Item] = bag if bag else []
        self.__room: Room = room

    @property
    def bag(self) -> Tuple[Item]:
        """ The items in the player's bag. """
        return tuple(self.__bag)

    @property
    def room(self) -> Room:
        """ The room the player is currently in. """
        return self.__room

    def drop(self, item: Item) -> bool:
        """ Attempt to drop an item from the bag, returns True if it was dropped. """
        if item in self.bag:
            self.__bag.remove(item)
            self.room._add_item(item)
            return True
        return False

    def use(self, item: Item, entity: Entity) -> bool:
        """ Attempt to use an item from the bag on an entity (such as a door). Returns True if the item is consumed. """
        if item not in self.__bag:
            raise Exception(f"{item} is not in your bag")

        if entity._apply_item(item):
            self.__bag.remove(item)
            return True

        return False

    def move(self, door: Door) -> Optional[Room]:
        """ Attempt to move through a door. Return the new room or None if the door was locked. """
        if door not in self.room.doors:
            raise Exception(f"{self.room} does not have {door}")

        if door.locked:
            return None

        self.__room = door.to
        return self.room

    def move_to_room(self, room: Room) -> Optional[Room]:
        """ Attempt to move to a room. Return the new room or None if the door was locked. """
        for door in self.room.doors:
            if door.to == room:
                return self.move(door)

        raise Exception(f"{room} cannot be reached from {self.room}")

    def pickup(self, item: Item) -> bool:
        """ Attempt to add an item from the room to the bag. Returns True if the item was picked up. """
        if len(self.bag) >= 5:
            return False

        if self.__room._take(item):
            self.__bag.append(item)
            return True

        raise Exception(f"{item} was not found in {self.room}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.room!r}, {self.bag!r})"


class Item:
    def __init__(self, name: str, item_type: str):
        self.__name = name
        self.__item_type = item_type.casefold()

    @property
    def name(self) -> str:
        """ Name of the item. """
        return self.__name

    @property
    def item_type(self) -> str:
        """ The item's internal type. """
        return self.__item_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.item_type!r})"


class Door(Entity):
    def __init__(self, room: Room, key: Optional[Item] = None):
        self.__key = key.item_type if key else None
        self.__locked = key is not None
        self.__to = room

    @property
    def key(self) -> str:
        """ The item type that is necessary to unlock the door. """
        return self.__key

    @property
    def locked(self) -> bool:
        """ Whether the door is locked or not. """
        return self.__locked

    @property
    def to(self) -> Room:
        """ Get the room that the door goes to """
        return self.__to

    def _apply_item(self, item: Item) -> bool:
        """ If the item type matches the door's key item type unlock the door and consume the key by returning True. """
        if self.locked:
            self.__locked = item.item_type != self.__key
        return not self.locked

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.locked!r}, {self.to!r}, {self.key!r})"


class Room:
    def __init__(self, entry: Room, items: List[Item], depth: int):
        self.__doors: List[Door] = []
        self.__items = items
        self.__depth = depth

        if entry:
            self._connect_room(entry, None)

    @property
    def items(self) -> Tuple[Item]:
        """ All items in the room. """
        return tuple(self.__items)

    @property
    def depth(self) -> int:
        """ How close the room is to the maximum number of rooms for a pathway. """
        return self.__depth

    @property
    def doors(self) -> Tuple[Door]:
        """ All doors that are in the room. """
        return tuple(self.__doors)

    def _add_item(self, item: Item):
        self.__items.append(item)

    def _take(self, item: Item) -> bool:
        if item in self.__items:
            self.__items.remove(item)
            return True
        return False

    def _connect_room(self, room: Room, key: Optional[Item]):
        self.__doors.append(Door(room, key))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__doors[1:]!r}, {self.items!r}>"
