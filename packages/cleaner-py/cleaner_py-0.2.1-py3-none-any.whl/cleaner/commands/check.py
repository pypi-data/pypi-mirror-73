from cleo import Command

from cleaner.searcher import Searcher


class CheckCommand(Command):
    """
    Check for virtual environments and packages that you haven't used recently.

    check
        {directory : Check the following repositories in this directory}
        {--mtime=30 : Check repositories that have not been updated within x days}
        {--d|depth=3 : Depth of search}
        {--config : config file path}
    """
    # Todo If the directory is not specified, try to find the current directory
    def handle(self):
        searcher = Searcher(self.argument('directory'), self.option('depth'), self.option('mtime'), io=self.io)
        searcher.run()
