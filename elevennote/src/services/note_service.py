
from flask import g

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
    notes = Note.query.filter_by(g.user.get('owner_id'))

    if notes:
        return notes
    return {'status': 'no public notes found'}, 200


def get_note_by_id(id):
    return Note.query.filter_by(id=id, owner_id=g.user.get('owner_id')).first()


def update_note(id, data):
    note = get_note_by_id(id)
    if note:
        for key, item in data.items():
                setattr(note, key, item)
        note.modified_at = datetime.utcnow()
        db.session.commit()
        return Note.query.get(id), 200
    else:
        return {'status': 'note not found'}, 404


def delete_note(id):
    note = get_note_by_id(id)

    if note:
        db.session.delete(note)
        db.session.commit()
        return {'status': 'no content'}, 204
    else:
        return {'status': 'note not found'}, 404


def save_changes(data):
    db.session.add(data)
    db.session.commit()
