#!env/bin/python

import os
import logging

from flask_script import Manager, Server

from coveragespace.settings import get_config
from coveragespace.app import create_app


config = get_config(os.getenv('CONFIG'))
app = create_app(config)
manager = Manager(app)


manager.add_command('server', Server(host='0.0.0.0'))


if __name__ == '__main__':
    manager.run()
