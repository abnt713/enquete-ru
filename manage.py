from flask_script import Manager
from enqueteru.app import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()