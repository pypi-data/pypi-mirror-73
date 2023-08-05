# Copyright 2017-2019 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3

import typing

from dewi_module_framework.messages import Level
from ..common.base_module_ import LogparserBaseModule


class PostfixModule(LogparserBaseModule):
    def get_registration(self):
        return [
            {
                'program': 'postfix/error',
                'message_substring': 'delivery temporarily suspended',
                'callback': self.delivery_suspended
            }
        ]

    def start(self):
        self._events = list()

    def delivery_suspended(self, time: str, program: str, pid: typing.Optional[str], msg: str):
        self._events.append(f'{time} - {msg}')

    def finish(self):
        if self._events:
            self.add_message(
                Level.ALERT, 'Postfix', 'Postfix',
                "Emails cannot be delivered; count='{}'".format(len(self._events)),
                details=(self._events if len(self._events) < 220 else self._events[:200] + ['...']))
