from typing import List

import requests
import re
import logging

from .longpoll import GroupLongpoll
from .handlers import UpdateHandler
from ..objects.objects import BotMessage
from ..methods import Messages

logger = logging.getLogger('easy_vk.bot')
logger.setLevel(logging.DEBUG)


class GroupBot:
    def __init__(self, owner_access_token: str,
                 group_access_token: str,
                 group_id: int,
                 wait: int = 25,
                 debug_mode: bool = False,
                 owner_id: int = None):
        self._owner_access_token = owner_access_token
        self._group_access_token = group_access_token
        self._group_id = group_id
        self._wait = wait
        self._debug_mode = debug_mode
        self._owner_id = owner_id

        self._handlers: List[UpdateHandler] = []

        self.longpoll = GroupLongpoll(owner_access_token, group_id, wait)

        # api methods
        session = requests.Session()
        self.messages = Messages(session, group_access_token, '5.120', 25)

    ############################# Handlers
    def message_typing_state_handler(self, user_id: int = None,
                                     user_ids: List[int] = None):
        def decorator(function):
            update_type = 'message_typing_state'
            filters = []
            if user_id:
                filters.append(lambda x: x['from_id'] == user_id)
            if user_ids:
                filters.append(lambda x: x['from_id'] in user_ids)

            handler = UpdateHandler(update_type, filters, function)
            self._handlers.append(handler)
            return function

        return decorator

    def message_new_handler(self, regexp: str = None,
                            user_id: int = None,
                            user_ids: List[int] = None,
                            attachment_type: str = None):
        if self._debug_mode:
            user_id = self._owner_id

        def decorator(function):
            update_type = 'message_new'
            filters = []
            if regexp:
                filters.append(lambda x: True if re.fullmatch(regexp, x.get('text', '')) else None)
            if user_id:
                filters.append(lambda x: x['message']['from_id'] == user_id)
            if user_ids:
                filters.append(lambda x: x['message']['from_id'] in user_ids)
            if attachment_type:
                filters.append(lambda x: attachment_type in [a['type'] for a in x['message']['attachments']])

            handler = UpdateHandler(update_type, filters, function, handled_object_type=BotMessage)
            self._handlers.append(handler)
            return function

        return decorator

    def group_leave_handler(self, user_id: int = None,
                            user_ids: List[int] = None,
                            self_: bool = None):
        def decorator(function):
            update_type = 'group_leave'
            filters = []
            if user_id:
                filters.append(lambda x: x['user_id'] == user_id)
            if user_ids:
                filters.append(lambda x: x['user_id'] in user_ids)
            if self_:
                filters.append(lambda x: x['self'] == self_)

            handler = UpdateHandler(update_type, filters, function)
            self._handlers.append(handler)
            return function

        return decorator

    def group_join_handler(self, user_id: int = None,
                           user_ids: List[int] = None,
                           join_type: bool = None):
        def decorator(function):
            update_type = 'group_join'
            filters = []
            if user_id:
                filters.append(lambda x: x['user_id'] == user_id)
            if user_ids:
                filters.append(lambda x: x['user_id'] in user_ids)
            if join_type:
                filters.append(lambda x: x['join_type'] == join_type)

            handler = UpdateHandler(update_type, filters, function)
            self._handlers.append(handler)
            return function

        return decorator

    ####################################################

    def _handle(self, update):
        for handler in self._handlers:
            handler.notify(update)

    def run(self):
        logger.debug(f'Run bot for group https://vk.com/public{self._group_id}\n')
        for updates in self.longpoll.listen():
            for update in updates:
                self._handle(update)
