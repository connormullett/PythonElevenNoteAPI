
import datetime
import jwt

from .. import db, bcrypt


class Note(db.Model):

    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
