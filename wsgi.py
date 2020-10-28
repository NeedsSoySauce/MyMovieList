"""App entry point."""

from movie import create_app
from cache import cache

app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False)
