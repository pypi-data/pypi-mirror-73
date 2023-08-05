"""The HackerLab 9000 Overmind API server library."""

import json

from flask import Flask
from flask_classful import FlaskView
from hal9k import Meta

app = Flask(__name__)


class Hal9kAPI(FlaskView):
    """The Overmind API server class."""

    ABOUT = "".join(
        [
            "This is the HackerLab 9000 Overmind API Server. For more ",
            "information, see <a href='https://github.com/haxys-labs/",
            "Hal9k-Overmind-API'>the GitHub repository</a>.",
        ]
    )

    def __init__(self):
        """Initialize the Overmind API server."""
        self.meta = Meta()

    def __enter__(self):
        """Work with Context Managers."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Work with Context Managers."""
        del self.meta

    def get_tracks(self):
        """Return a listing of tracks in production."""
        tracks = self.meta.get_tracks()
        return json.dumps({"tracks": tracks})

    def index(self):
        """Return information about the API."""
        return self.ABOUT


Hal9kAPI.register(app, route_base="/")
