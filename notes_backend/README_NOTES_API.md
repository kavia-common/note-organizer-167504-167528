# Notes API - Ocean Professional

RESTful API implemented with Flask + Flask-Smorest.

Endpoints:
- GET /             Health
- GET /api/v1/notes/           List notes (q, tag, archived)
- POST /api/v1/notes/          Create note {title, content, tags?}
- GET /api/v1/notes/{id}       Get one
- PATCH /api/v1/notes/{id}     Update partial {title?, content?, tags?, archived?}
- DELETE /api/v1/notes/{id}    Delete

Interactive API docs: /docs
```bash
curl -s http://localhost:5000/api/v1/notes/ -X POST -H 'Content-Type: application/json' -d '{"title":"First","content":"Body","tags":["ideas"]}'
```

Architecture is ready to swap the in-memory repository with notes_database.
