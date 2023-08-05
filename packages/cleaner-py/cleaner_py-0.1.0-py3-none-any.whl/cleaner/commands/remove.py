from cleo import Command

import os
import shutil

from cleaner.searcher import Searcher


class RemoveCommand(Command):
    """
    Check for virtual environments and packages that you haven't used recently and remove it.

    remove
        {directory : Check the following repositories in this directory}
        {--mtime=30 : Check repositories that have not been updated within x days}
        {--d|depth=3 : Depth of search}
    """

    # Todo If the directory is not specified, try to find the current directory
    def handle(self):
        searcher = Searcher(self.argument('directory'), self.option('depth'), self.option('mtime'), io=self.io)

        packages_not_recently_used = searcher.run()

        if not self.confirm("Do you want to remove these packages from these repositories?"):
            self.line("OK, do nothing")
        else:
            self.line("OK, remove packages from these repositories")
            for pkg in packages_not_recently_used:
                try:
                    shutil.rmtree(pkg)
                except OSError:
                    self.line_error("%s has not exist, skip", pkg)
                else:
                    self.info(f"remove {pkg}")
