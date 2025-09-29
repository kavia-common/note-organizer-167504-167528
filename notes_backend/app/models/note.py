"""
Note model definitions for the Notes API.

This module provides a simple in-memory data model for notes to satisfy the
current task scope without external DB configuration. It is structured to allow
easy replacement with a real database (notes_database container) later by
swapping the repository implementation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Note:
    """
    Domain model for a Note.

    Fields:
        id: Unique identifier for the note.
        title: Title of the note.
        content: Body/content of the note.
        tags: Optional list of tags to organize notes.
        created_at: ISO timestamp when the note was created.
        updated_at: ISO timestamp when the note was last updated.
        archived: Whether the note is archived.
    """
    id: int
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    archived: bool = False

    def update_from(self, title: Optional[str] = None, content: Optional[str] = None,
                    tags: Optional[List[str]] = None, archived: Optional[bool] = None) -> None:
        """
        Update mutable fields and touch updated_at.
        """
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if tags is not None:
            self.tags = tags
        if archived is not None:
            self.archived = archived
        self.updated_at = datetime.utcnow().isoformat() + "Z"


class NotesRepository:
    """
    Repository layer abstracting data persistence for notes.

    This is an in-memory implementation for the current task. Replace with a
    database-backed implementation to integrate with notes_database later.
    """
    def __init__(self):
        self._notes: dict[int, Note] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def list(self, *, q: Optional[str] = None, tag: Optional[str] = None,
             archived: Optional[bool] = None) -> List[Note]:
        results = list(self._notes.values())
        if q:
            low = q.lower()
            results = [n for n in results if low in n.title.lower() or low in n.content.lower()]
        if tag:
            results = [n for n in results if tag in (n.tags or [])]
        if archived is not None:
            results = [n for n in results if n.archived is archived]
        return sorted(results, key=lambda n: n.updated_at, reverse=True)

    def get(self, note_id: int) -> Optional[Note]:
        return self._notes.get(note_id)

    def create(self, title: str, content: str, tags: Optional[List[str]] = None) -> Note:
        note_id = self._next_id()
        note = Note(id=note_id, title=title, content=content, tags=tags or [])
        self._notes[note_id] = note
        return note

    def update(self, note_id: int, *, title: Optional[str] = None, content: Optional[str] = None,
               tags: Optional[List[str]] = None, archived: Optional[bool] = None) -> Optional[Note]:
        note = self._notes.get(note_id)
        if not note:
            return None
        note.update_from(title=title, content=content, tags=tags, archived=archived)
        return note

    def delete(self, note_id: int) -> bool:
        return self._notes.pop(note_id, None) is not None
