from flask_smorest import Blueprint
from flask.views import MethodView

# Consistent naming and description for OpenAPI docs
blp = Blueprint("Health", "health", url_prefix="/", description="Service health and readiness")

@blp.route("/")
class HealthCheck(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """
        summary: Health check
        description: Returns a simple healthy status to indicate service readiness.
        responses:
          200:
            description: Service is healthy.
        """
        return {"message": "Healthy"}
