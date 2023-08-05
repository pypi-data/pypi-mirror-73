from datetime import datetime, timedelta
from typing import List, Tuple

from clikit.io import ConsoleIO
from clikit.api.io.flags import DEBUG
import os
from .utils import walk_level


class Searcher:
    def __init__(self, directory, depth, mtime, io: ConsoleIO):
        self.directory = directory
        self.depth = depth
        self.mtime = mtime
        self._io = io
        self.package_dirs = [".venv", "node_modules"]

    # Todo ignore_repository settings
    def run(self) -> List[str]:
        """
        Recursively looks under directories and returns a list of repositories with .venv etc.

        Returns: not recently used repository list: List((repository, last_modified_time))
        """
        self._io.write_line(f"Searching for repositories up to {self.depth} depths under {self.directory}")
        self._io.write_line(f"mtime: {self.mtime}, depth: {self.depth}")
        repositories_w_packages = {
            pkg_dir: [root for root, dirs, _ in walk_level(self.directory, int(self.depth)) if pkg_dir in dirs]
            for pkg_dir in self.package_dirs
        }

        self._io.write_line(f"repositories: {repositories_w_packages}", DEBUG)

        by_last_modified_time = datetime.now() - timedelta(days=int(self.mtime))
        self._io.write_line(f"Search repository that has not been updated since {by_last_modified_time}")
        repositories_not_recently_used = {pkg: self.filter_by_last_modified_time(repos, by_last_modified_time) for pkg, repos in repositories_w_packages.items()}

        self._io.write_line(f"<info>these repositories hasn't been updated in {self.mtime} days.</info>")
        for pkg, repos in repositories_not_recently_used.items():
            self._io.write_line(f"<info>{pkg}</info>")
            self.output(repos)

        packages_not_recently_used = [repo[0] + f"/{pkg}" for pkg, repos in repositories_not_recently_used.items() for repo in repos]
        self._io.write_line(f"packages_not_recently_used {packages_not_recently_used}", DEBUG)
        return packages_not_recently_used

    @staticmethod
    def filter_by_last_modified_time(repos_w_pkgs: List[str], by_last_modified_time) -> List[Tuple[str, datetime]]:
        # FIXME Consider adding a depth restriction here as well.
        repositories_not_recently_used = []
        for path in repos_w_pkgs:
            last_modified_time = datetime.fromtimestamp(max(os.stat(root).st_mtime for root, _, _ in os.walk(path)))
            if last_modified_time < by_last_modified_time:
                repositories_not_recently_used.append((path, last_modified_time))

        return repositories_not_recently_used

    def output(self, repositories_not_recently_used: List[Tuple[str, datetime]]):
        # Todo sort by last_modified_time or repo name
        # Todo datetime format
        [self._io.write_line(
            "    {}, last_modified_time: {}".format(os.path.relpath(repo, self.directory), last_modified_time))
            for repo, last_modified_time in repositories_not_recently_used]
        if len(repositories_not_recently_used) == 0:
            self._io.write_line("    There is no virtual environment or packages in the old repositories under this directory")
