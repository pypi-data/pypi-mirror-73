from aiogram import types
from random import randint
from .container import RoomsContainer
from tgusers.tables.tables import Tables
from tgusers.bot.bot_class import TelegramBot
from tgusers.database.database import DataBase, PostgresAuthData
from tgusers.utils.runfunc import run_function_with_arguments_by_annotations
from tgusers.dataclasses.rooms import Room
from tgusers.utils.validator import valid_check
from tgusers.errors.rooms import RoomsErrors
from tgusers.dataclasses.rooms import Arguments, Argument


"""
Room content type can be in range of ['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker']
"""


class RoomsAlerts:
    @staticmethod
    def access_denied(get_alerts):
        if get_alerts:
            return [False, "Access denied"]
        else:
            return False

    @staticmethod
    def room_not_found(get_alerts):
        if get_alerts:
            return [False, "Room not found"]
        else:
            return False

    @staticmethod
    def successfully(get_alerts):
        if get_alerts:
            return [True, "Successfully"]
        else:
            return True



class Rooms:
    def __new__(cls, bot_token: str = None, pgData: PostgresAuthData = None, message_logging: bool = False,
                get_alerts: bool = False, antispam: bool = False):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Rooms, cls).__new__(cls)

            cls.rooms = []
            cls.get_alerts = get_alerts
            cls.db = DataBase(pgData)
            cls.tables = Tables(cls.db)
            cls.telegram_bot = TelegramBot(bot_token, cls.tables, cls.rooms, message_logging, antispam=antispam)
            cls.bot = cls.telegram_bot.bot
        return cls.instance

    def add_message_room(self, name: str = None, content_type: list = None, roles: list = None,
                         is_global: bool = False):
        if roles is None:
            roles = ["all"]
        if content_type is None:
            content_type = []
        if name is None:
            name = str(randint(100000, 999999))
        if not valid_check(name):
            raise RoomsErrors("Invalid room name")

        def decorator(room_func):
            if is_global:
                room = Room(name=name, content_type=content_type, roles=roles, function=room_func, is_global=True,
                            message_handler=True)
                self.rooms.append(room)
            else:
                room = Room(name=name, content_type=content_type, roles=roles, function=room_func, is_global=False,
                            message_handler=True)
                self.rooms.append(room)

        return decorator

    def add_callback_room(self, name: str = None, is_global: bool = False):
        if name is None:
            name = str(randint(100000, 999999))
        if not valid_check(name):
            raise RoomsErrors("Invalid room name")

        def decorator(room_func):
            room = Room(name=name, roles=[], function=room_func, is_global=is_global, callback_query_handler=True)
            self.rooms.append(room)

        return decorator

    def on_join_room(self, name: str = None):
        def decorator(fuc):
            self.get_room_by_name(name).on_join = fuc

        return decorator

    def add_role(self, role: str, users: list):
        for user in users:
            if not self.tables._users.check_user_for_registration(telegram_id=user):
                users.remove(user)
        for user in users:
            self.tables._users.set_user_role(role, telegram_id=user)
        self.db.commit()

    def get_user_role(self, user: int):
        return self.tables._users.get_user_role(telegram_id=user)

    def get_room_by_name(self, name) -> Room:
        for room in self.rooms:
            if room.name == name:
                return room
        return None

    def get_rooms_names(self):
        names = []
        for room in self.rooms:
            names.append(room.name)
        return names

    async def user_go_to_room(self, message, room_name: str):
        if not self.get_room_by_name(room_name):
            return
        if self.tables._users.get_user_role(message) in self.get_room_by_name(room_name).roles or "all" in self.get_room_by_name(room_name).roles:
            if self.tables._users.set_room(message, self.get_rooms_names(), room_name):
                if self.get_room_by_name(room_name).on_join:
                    o_args = [
                        Argument(value=message, annotation=types.Message)
                    ]
                    n_o_args = [
                        Argument(value=self, annotation=Rooms)
                    ]
                    args = Arguments(obligatory=o_args, not_obligatory=n_o_args)
                    await run_function_with_arguments_by_annotations(self.get_room_by_name(room_name).on_join, args)
                return RoomsAlerts.successfully(self.get_alerts)
            else:
                return RoomsAlerts.room_not_found(self.get_alerts)
        else:
            return RoomsAlerts.access_denied(self.get_alerts)

    async def go_to_one_of_the_rooms(self, message, rooms_dict: dict):
        get_room = rooms_dict.get(message.text)
        if get_room:
            return await self.user_go_to_room(message, get_room)
        else:
            return False


    # async def go_to_previous_room(self, message, rooms_dict: dict):
    #     get_room = rooms_dict.get(message.text)
    #     if get_room:
    #         return await self.user_go_to_room(message, get_room)
    #     else:
    #         return False

    # async def broadcast_do(self, message: str, mark_down: bool = False):
    #     users = self.tables._users.get_users_ids()
    #     user_count = 0
    #     for user in users:
    #         if user_count > 25: sleep(1)
    #         await self.telegram_bot.bot.send_message(user.get("id"), message, mark_down=mark_down)

    # async def broadcast(self, message: str, mark_down: bool = False):
    #     await self.broadcast_do(message, mark_down)


    def show_rooms(self):
        print(self.rooms)

    def upload_rooms(self, rooms_container: RoomsContainer):
        self.rooms += rooms_container.rooms

