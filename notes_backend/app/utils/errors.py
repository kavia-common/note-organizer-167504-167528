"""
Error handling utilities and standardized error responses.
"""
from flask import jsonify


class APIError(Exception):
    """Base API error with status code."""
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None, errors: dict | None = None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = int(status_code)
        self.message = message
        self.errors = errors or {}

    def to_response(self):
        return jsonify({
            "code": self.status_code,
            "status": "error",
            "message": self.message,
            "errors": self.errors
        }), self.status_code


class NotFoundError(APIError):
    status_code = 404


class BadRequestError(APIError):
    status_code = 400


def register_error_handlers(app):
    """
    Register error handlers for APIError and generic Exception on the Flask app.
    """
    @app.errorhandler(APIError)
    def handle_api_error(err: APIError):
        return err.to_response()

    @app.errorhandler(404)
    def handle_404(_):
        return NotFoundError("Resource not found").to_response()

    @app.errorhandler(405)
    def handle_405(_):
        return BadRequestError("Method not allowed").to_response()

    @app.errorhandler(Exception)
    def handle_generic_error(err: Exception):
        # Avoid leaking internal details in production style.
        return APIError("Internal Server Error", status_code=500).to_response()
