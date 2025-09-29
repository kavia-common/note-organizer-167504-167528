"""
Marshmallow schemas for Note validation and serialization.
"""
from marshmallow import Schema, fields, validate


class NoteBaseSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200), metadata={"description": "Title of the note"})
    content = fields.String(required=True, validate=validate.Length(min=1), metadata={"description": "Content/body of the note"})
    tags = fields.List(fields.String(validate=validate.Length(min=1, max=50)), required=False, load_default=list, metadata={"description": "List of tags"})


class NoteCreateSchema(NoteBaseSchema):
    pass


class NoteUpdateSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=200), metadata={"description": "Title of the note"})
    content = fields.String(required=False, validate=validate.Length(min=1), metadata={"description": "Content/body of the note"})
    tags = fields.List(fields.String(validate=validate.Length(min=1, max=50)), required=False, metadata={"description": "List of tags"})
    archived = fields.Boolean(required=False, metadata={"description": "Archive state"})


class NoteResponseSchema(Schema):
    id = fields.Integer(required=True, metadata={"description": "Unique identifier"})
    title = fields.String(required=True)
    content = fields.String(required=True)
    tags = fields.List(fields.String(), required=True)
    archived = fields.Boolean(required=True)
    created_at = fields.String(required=True, metadata={"description": "Created timestamp (ISO8601 UTC)"})
    updated_at = fields.String(required=True, metadata={"description": "Last updated timestamp (ISO8601 UTC)"})


class NotesListQuerySchema(Schema):
    q = fields.String(required=False, metadata={"description": "Search query applied to title and content"})
    tag = fields.String(required=False, metadata={"description": "Filter by a tag"})
    archived = fields.Boolean(required=False, metadata={"description": "Filter by archived state"})
