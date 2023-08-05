# -*- coding: utf-8 -*-
from urllib.parse import quote
from datetime import datetime
import requests

from gvapi import errors
from gvapi.pet import Pet


class Hero:
    '''Основной класс пакета.

    Через данный класс осуществляется доступ к данным героя.

    Attributes:
        god (str): Имя бога.
        __token (str, None): API токен.
        _base_url (str): URL для доступа к API.
        _last_upd (py:class:`~datetime.datetime`): Время последнего обновления данных.
        _data (dict): Словарь с последними полученными данными.
        __threshold (int): Задержка для обнолвения данных в секундах. Не может быть меньше 60.
        __need_token_attrs (list): Атрибуты, для доступа к которым необходимо использовать токен.
        pet (:py:class:`~gvapi.pet.Pet`): Экземпляр класса `Pet`, описывающий питомца.

    Args:
        god (str): Имя бога.
        token (str, optional): Токен для доступа к API. Если не указан,
            то обращение производится к открытому API.
        api_url (str, optional): URL для доступа к API. Если не указан,
            то используется `https://godville.net/gods/api`.
        threshold (int, optional): Задержка обновления данных о герое в секундах,
            по умолчанию 300 секунд или 5 минут. Данный параметр не может быть меньше 60(1 минута).
    '''
    def __init__(self, god, token=None, api_url='https://godville.net/gods/api', threshold=300):
        if threshold < 60:
            raise errors.MinThresholdException('Параметр threshold не может быть меньше 60 секунд.')
        self.god = god
        self.__token = token
        self.__threshold = threshold
        self._base_url = api_url
        self._last_upd = datetime.now()
        self._data = self.__get_data()
        self.pet = Pet(self)


    def __getattribute__(self, name):
        if name in ['_Hero__token', '_Hero__get_data', '_base_url',
                    '_last_upd', '_Hero__threshold']:
            return super(Hero, self).__getattribute__(name)

        need_token_attributes = [
            'activatables', 'is_fighting', 'aura', 'diary_last', 'distance_to_town',
            'progress', 'expired', 'fight_type', 'godpower', 'gold', 'health',
            'inventory_num', 'quest_progress', 'quest', 'town'
        ]

        if not self.__token and name in need_token_attributes:
            raise errors.NeedToken('Для доступа к данному атрибуту необходим токен.')

        if self.__token and 'health' not in self._data.keys():
            raise errors.TokenWasResetted('Токен был сброшен, необходимо обновить токен.')

        if datetime.now().timestamp() - self._last_upd.timestamp() > self.__threshold:
            self._data = self.__get_data()
            self._last_upd = datetime.now()

        return super(Hero, self).__getattribute__(name)


    def __repr__(self):
        return '<Hero {}>'.format(self.name)


    def __str__(self):
        if self.gender == 'муж':
            return 'Герой {}'.format(self.name)
        return 'Героиня {}'.format(self.name)


    def __get_data(self):
        '''Получить данные.

        Произвести обращение к API для получения данных о герое.

        Returns:
            Словать с данными полученными от API.

        Raises:
            APIUnavailable: в случае недоступности API.
            UnexpectedAPIResponse: в случае получения неожиданного ответа от API.
        '''
        if self.__token:
            url = '{}/{}/{}'.format(self._base_url, quote(self.god, safe=''), self.__token)
        else:
            url = '{}/{}'.format(self._base_url, quote(self.god, safe=''))

        try:
            response = requests.get(url)
        except (requests.ConnectTimeout, requests.ConnectionError) as exc:
            raise errors.APIUnavailable('Обращение к API закончилось неудачей: {}'.format(exc))

        if response.status_code != 200:
            raise errors.UnexpectedAPIResponse(
                'Неожиданный ответ API(код {}) :{}'.format(response.status_code, response.text)
            )

        return response.json()


    @property
    def threshold(self):
        '''int: Задержка обновления данных о герое в секундах.'''
        return self.__threshold


    @threshold.setter
    def threshold(self, time):
        if time < 60:
            raise errors.MinThresholdException('Параметр threshold не может быть меньше 60 секунд.')
        self.__threshold = time


    @property
    def from_last_updated(self):
        '''int: Количество секунд, прошедших с последнего обновления данных.'''
        return int(datetime.now().timestamp() - self._last_upd.timestamp())


    @property
    def token(self):
        '''str: Токен в защищенном формате(не скрыты только последние 4 символа).
            Если токен не используется, то возвращает `None`'''
        if not self.__token:
            return None
        return '{}{}'.format('*' * len(self.__token[:-4:]), self.__token[-4::])


    @property
    def name(self):
        '''str: Имя героя.'''
        return self._data['name']


    @property
    def gender(self):
        '''str: Пол героя.'''
        return 'муж' if self._data['gender'] == 'male' else 'жен'


    @property
    def is_alive(self):
        '''bool: Жив ли герой.'''
        return self._data['health'] > 0


    @property
    def health(self):
        '''int: Количество очков здоровья героя.'''
        return self._data['health']


    @property
    def health_percent(self):
        '''float: Количество очков здоровья героя в процентах.'''
        return self.health / self.max_health
