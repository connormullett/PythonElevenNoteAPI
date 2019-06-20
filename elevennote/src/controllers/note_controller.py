
from flask import request, g
from flask_restplus import Resource

from ..utils.dto import NoteCreateDto, NoteDto, NoteDetailDto, NoteUpdateDto
from ..services import note_service
from ..utils.decorator import Authenticate

api = NoteCreateDto.api
note = NoteDto.note
note_create = NoteCreateDto.note
note_detail = NoteDetailDto.note
note_update = NoteUpdateDto.note


@api.route('/')
class NoteList(Resource):

    @api.doc('list_of_notes')
    @api.marshal_list_with(note)
    @Authenticate
    def get(self):
        return note_service.get_all_notes()
    
    @api.response(201, 'Note Created')
    @api.doc('create new note')
    @api.expect(note_create, validate=True)
    @Authenticate
    def post(self):
        data = request.json
        data['owner_id'] = g.user['owner_id']
        return note_service.create_note(data)


@api.route('/<note_id>')
@api.param('note_id', 'notes unique id')
@api.response(404, 'note not found')
@api.response(401, 'owner_id mismatch')
class Note(Resource):

    @api.doc('get note by ID')
    @api.marshal_with(note_detail)
    def get(self, note_id):
        data = request.json
        return note_service.get_note_by_id(note_id)
    
    @api.doc('update note by id')
    @api.expect(note_update, validate=True)
    @api.marshal_with(note_update)
    @Authenticate
    def put(self, note_id):
        data = request.json
        user_id = g.user.get('owner_id')
        note = note_service.get_note_by_id(note_id)
        if not note:
            api.abort(404)
        if user_id != note.owner_id:
            api.abort(401)
        return note_service.update_note(note_id, data)
    
    @api.doc('delete note by id')
    @Authenticate
    def delete(self, note_id):
        if g.user.get('owner_id') != note_service.get_note_by_id(note_id).owner_id:
            api.abort(401)

        return note_service.delete_note(note_id)


@api.route('/by_owner_id/<owner_id>')
@api.param('note_id', 'owners public id')
@api.response(404, 'owner id not found')
class NoteByOwner(Resource):

    @api.doc('get notes by owner id')
    @api.marshal_list_with(note, envelope='data')
    def get(self, owner_id):
        notes = note_service.get_notes_by_owner_id(owner_id)
        print(notes)
        return notes, 200
