"""Flask application factory and development entry point."""

from flask import Flask

from routes import CURRENT, blueprint
from sudoku import generator as sudoku_logic


def create_app() -> Flask:
    """Create and configure the Sudoku Flask application."""
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)