from app.routes.client_routes import register_client_routes
from app.routes.super_routes import register_super_routes

def register_routes(app):
    register_super_routes(app)
    register_client_routes(app)