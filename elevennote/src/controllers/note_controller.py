
from flask import request, g
from flask_restplus import Resource
from flask_restplus.marshalling import marshal

from ..utils.dto import NoteCreateDto, NoteDto, NoteDetailDto, NoteUpdateDto
from ..services import note_service
from ..utils.decorator import Authenticate

api = NoteDto.api
note = NoteDto.note
note_create = NoteCreateDto.note
note_detail = NoteDetailDto.note
note_update = NoteUpdateDto.note


@api.route('/')
@api.response(404, 'no notes found')
class NoteList(Resource):

    @api.doc('list of notes')
    @Authenticate
    def get(self):
        notes = note_service.get_all_notes()
        print(len(notes))
        if len(notes) == 0:
            return {'status': 'no notes found'}, 404
        return marshal(notes, note)
    
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
    @Authenticate
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
