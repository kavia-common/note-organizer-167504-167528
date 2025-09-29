from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp
from .utils.errors import register_error_handlers
from .utils.theme import OCEAN_PRO_THEME

# Initialize Flask app with OpenAPI and CORS
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})

# Ocean Professional theme-aligned API metadata
app.config["API_TITLE"] = "Notes API - Ocean Professional"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
# Provide theme metadata in OpenAPI extensions for discoverability
app.config["APISPEC_OPTIONS"] = {
    "info": {
        "x-theme": OCEAN_PRO_THEME
    },
    "tags": [
        {"name": "Health", "description": "Service health and readiness"},
        {"name": "Notes", "description": "CRUD operations for notes"},
    ],
}

# Initialize API
api = Api(app)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(notes_blp)

# Register error handlers
register_error_handlers(app)
