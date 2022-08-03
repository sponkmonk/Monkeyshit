from __future__ import annotations

from flask_login import UserMixin
from mongoengine import Document, StringField


class User(Document, UserMixin):
    username = StringField()
    password_hash = StringField()

    @staticmethod
    def get_by_id(id: str):
        return User.objects.get(id)
