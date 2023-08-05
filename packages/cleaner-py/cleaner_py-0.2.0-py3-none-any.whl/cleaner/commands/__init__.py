from .check import CheckCommand
from .remove import RemoveCommand
from cleo import Application

application = Application('cleaner')
application.add(CheckCommand())
application.add(RemoveCommand())


def main():
    application.run()
