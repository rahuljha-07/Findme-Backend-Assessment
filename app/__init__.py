from flask import Flask, send_from_directory
from flasgger import Swagger
import os

def initialize_app():
    """
    This function creates and sets up the Flask application.
    """
    # Set static folder to the correct path at the project root
    static_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
    app = Flask(__name__, static_folder=static_folder_path)


    # Configure Swagger for API documentation
    app.config['SWAGGER'] = {
        'title': 'Product Management API',
        'uiversion': 3
    }
    Swagger(app)  # Initialize Swagger

    # Register blueprints for modular route handling
    from .routes import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')

    # Route to serve the index.html at root URL
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    return app
