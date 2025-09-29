from flask_smorest import Blueprint
from flask.views import MethodView
from app.schemas.note import (
    NoteCreateSchema,
    NoteUpdateSchema,
    NoteResponseSchema,
    NotesListQuerySchema,
)
from app.models.note import NotesRepository
from app.utils.errors import NotFoundError
from typing import Any

# Blueprint with Ocean Professional theme meta applied via description
blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/api/v1/notes",
    description="CRUD operations for managing notes (Ocean Professional)",
)

# Singleton-like repository instance for current process
repo = NotesRepository()


@blp.route("/")
class NotesCollection(MethodView):
    # PUBLIC_INTERFACE
    @blp.arguments(NotesListQuerySchema, location="query")
    @blp.response(200, NoteResponseSchema(many=True))
    def get(self, args: dict[str, Any]):
        """
        summary: List notes
        description: Retrieve all notes with optional search and filters.
        responses:
          200:
            description: A list of notes.
        """
        notes = repo.list(q=args.get("q"), tag=args.get("tag"), archived=args.get("archived"))
        return notes

    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteResponseSchema)
    def post(self, payload: dict[str, Any]):
        """
        summary: Create a note
        description: Create a new note with title, content, and optional tags.
        responses:
          201:
            description: The created note.
        """
        note = repo.create(title=payload["title"], content=payload["content"], tags=payload.get("tags", []))
        return note


@blp.route("/<int:note_id>")
class NoteItem(MethodView):
    @blp.response(200, NoteResponseSchema)
    def get(self, note_id: int):
        """
        summary: Get a note
        description: Get a note by its ID.
        responses:
          200:
            description: The requested note.
          404:
            description: Note not found.
        """
        note = repo.get(note_id)
        if not note:
            raise NotFoundError("Note not found")
        return note

    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteResponseSchema)
    def patch(self, payload: dict, note_id: int):
        """
        summary: Update a note
        description: Patch fields of a note by its ID.
        responses:
          200:
            description: The updated note.
          404:
            description: Note not found.
        """
        note = repo.update(note_id, title=payload.get("title"), content=payload.get("content"),
                           tags=payload.get("tags"), archived=payload.get("archived"))
        if not note:
            raise NotFoundError("Note not found")
        return note

    @blp.response(204)
    def delete(self, note_id: int):
        """
        summary: Delete a note
        description: Delete a note by its ID.
        responses:
          204:
            description: Note deleted successfully.
          404:
            description: Note not found.
        """
        ok = repo.delete(note_id)
        if not ok:
            raise NotFoundError("Note not found")
        return ""
