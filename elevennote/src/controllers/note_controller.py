
from flask import request, g
from flask_restplus import Resource

from ..utils.dto import NoteCreateDto, NoteResponseDto
from ..services import note_service
from ..utils.decorator import Authenticate

api = NoteCreateDto.api
_note = NoteCreateDto.note
_note_response = NoteResponseDto.note_response


@api.route('/')
class NoteList(Resource):

    @api.doc('list_of_notes')
    @api.marshal_list_with(_note_response)
    @Authenticate
    def get(self):
        return note_service.get_all_notes()
    
    @api.response(201, 'Note Created')
    @api.doc('create new note')
    @api.expect(_note, validate=True)
    @Authenticate
    def post(self):
        data = request.json
        data['owner_id'] = g.user['owner_id']
        return note_service.create_note(data)
