#!/usr/bin/env python3

from .connection import Connection

class API:
    def __init__(self, *,
        host:str = 'localhost',
        password:str = None,
        port:int = 36330
    ):
        self._connection = None
        self._host = host
        self._port = port
        self._password = password


    def heartbeat(self) -> int:
        return self.__basic_command('heartbeat')


    def info(self) -> dict:
        return self.__basic_command('info')


    def num_slots(self) -> int:
        return self.__basic_command('num-slots')


    def options(self) -> dict:
        return self.__basic_command('options -a')


    def pause(self, slot_id: int):
        try:
            self.__start_conversation()
            if slot_id is None:
                self.__send_command('pause')
            else:
                self.__send_command('pause %d' % (slot_id))
        finally:
            self.__end_conversation()


    def queue_info(self) -> list:
        return self.__basic_command('queue-info')


    def save_all_options(self):
        try:
            self.__start_conversation()
            self.__send_command('save')
        finally:
            self.__end_conversation()


    def set_idle(self, idle:bool = True, slot_id:int = None):
        try:
            self.__start_conversation()
            if idle:
                if slot_id is None:
                    self.__send_command('on_idle')
                else:
                    self.__send_command('on_idle %d' % (slot_id))
            else:
                if slot_id is None:
                    self.__send_command('always_on')
                else:
                    self.__send_command('always_on %d' % (slot_id))
        finally:
            self.__end_conversation()


    def set_power(self, power:str):
        try:
            power = power.upper()
            if power != 'LIGHT' and power != 'MEDIUM' and power != 'FULL':
                raise Exception('Argument to set_power() must be LIGHT, MEDIUM, or FULL')
            self.__start_conversation()
            self.__send_command('options power="%s"' % (power))
            self.__send_command('save')
        finally:
            self.__end_conversation()


    def set_slot_option(self, slot_id :int, key, value):
        try:
            self.__start_conversation()
            opts = self.__send_command_and_parse('slot-options %d %s=%s' % (slot_id, key, value))
            return opts
        finally:
            self.__end_conversation()


    def slot_info(self) -> list:
        try:
            self.__start_conversation()
            slots = self.__send_command_and_parse('slot-info')
            for slot in slots:
                slot['options'] = self.__send_command_and_parse('slot-options %s -a' % slot['id'])
            return slots
        finally:
            self.__end_conversation()


    def unpause(self, slot_id :int):
        try:
            self.__start_conversation()
            if slot_id is None:
                self.__send_command('unpause')
            else:
                self.__send_command('unpause %d' % (slot_id))
        finally:
            self.__end_conversation()

    ###

    def __start_conversation(self):
        conn = self.__get_connection()
        conn.read_data()
        if self._password is not None:
            conn.write_data(b'auth %s\n' % (self._password.encode('utf-8')))
            return conn.read_data()
        else:
            return None


    def __get_connection(self):
        if self._connection is None:
            self._connection = Connection(self._host, self._port)
        return self._connection


    def __end_conversation(self):
        if self._connection is not None: self._connection.close()


    def __basic_command(self, chars):
        try:
            self.__start_conversation()
            rval = self.__send_command_and_parse(chars)
            return rval
        finally:
            self.__end_conversation()


    def __send_command(self, chars):
        conn = self.__get_connection()
        conn.write_data(b'%s\n' % (chars.encode('utf-8')))
        conn.read_data()


    def __send_command_and_parse(self, chars):
        conn = self.__get_connection()
        conn.write_data(b'%s\n' % (chars.encode('utf-8')))
        text = conn.read_data()
        pyon = conn.parse_pyon(text)
        return pyon
