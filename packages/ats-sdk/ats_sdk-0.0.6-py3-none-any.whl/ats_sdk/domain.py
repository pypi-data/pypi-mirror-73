from enum import Enum


class TranslatableMessagesMeta(type):
    def __new__(metacls, cls, bases, classdict):
        translatable_messages_class = super().__new__(metacls, cls, bases, classdict)
        if not bases:
            return translatable_messages_class

        added_members = [key for key in classdict if key[0] != "_"]
        for member in added_members:
            obj = translatable_messages_class(classdict[member])
            setattr(translatable_messages_class, member, obj)

        return translatable_messages_class


class TranslatableMessages(metaclass=TranslatableMessagesMeta):
    def __init__(self, key, placeholders=None):
        self._key = key
        self._placeholders = placeholders or {}

    def format(self, **kwargs):
        return self.__class__(self.key, kwargs)

    @property
    def key(self):
        return self._key

    @property
    def placeholders(self):
        return self._placeholders

    def __str__(self):
        return self.key
