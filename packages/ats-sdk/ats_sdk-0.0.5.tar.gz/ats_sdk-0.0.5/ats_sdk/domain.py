from enum import Enum


class TranslatableMessages(Enum):
    def __str__(self):
        return self.value


class TranslatableFormattedMessages:
    def __init__(self, key, placeholders):
        self._key = key
        self._placeholders = placeholders

    @classmethod
    def fstring(cls, key, **kwargs):
        return cls(key, kwargs)

    @property
    def key(self):
        return self._key

    @property
    def placeholders(self):
        return self._placeholders
