
from datetime import datetime

from elevennote.src import db
from elevennote.src.models.note import Note


def create_note(data):

    new_note = Note(
        owner_id=data['owner_id'],
        title=data['title'],
        content=data['content'],
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow()
    )
    save_changes(new_note)

    response_object = {
        'status': 'success',
        'message': 'created',
    }

    return response_object


def get_all_notes():
    return Note.query.all()


def get_note_by_id(id):
    return Note.query.filter_by(id=id).first()


def get_notes_by_owner_id(owner_id):
    return Note.query.filter_by(owner_id=owner_id)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
