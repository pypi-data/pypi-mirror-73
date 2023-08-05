from .commands import CheckCommand, RemoveCommand
from cleo import Application

application = Application('cleaner')
application.add(CheckCommand())
application.add(RemoveCommand())

if __name__ == '__main__':
    application.run()
