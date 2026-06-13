import os

from api.settings import get_config
from api.app import create_app


def find_assets():
    """Yield paths for all static files and templates."""
    for name in ['static', 'templates']:
        directory = os.path.join(app.config['PATH'], name)
        for entry in os.scandir(directory):
            if entry.is_file():
                yield entry.path


config = get_config(os.getenv('FLASK_ENV'))

app = create_app(config)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG'],
        extra_files=list(find_assets()),
    )
