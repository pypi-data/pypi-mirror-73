#! /usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2020 Eli Lilly and Company
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Import files from one or more git repositories to local destinations.
"""

import json
import logging
import os
from tempfile import mkdtemp
from shutil import rmtree, copyfile
from argparse import ArgumentParser
import sys
from pathlib import Path
from typing import Optional, Mapping, List, Tuple, Iterator, Union

from pkg_resources import get_distribution, DistributionNotFound
from git import Repo


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # pragma: no cover
    # module is not installed as expected. Set a dummy string version to
    # prevent failure if directly executed.
    __version__ = "dev"


class GitExtractedFiles:
    """
    Clone a repository into a temporary directory and then copy files out of it
    to new, final destinations locally. If the repository is private and
    requires authentication, either interactively enter the credentials or
    define ssh_key_path for a deploy key or token for personal access token
    to enable non-interactive authentication.
    This class is a context manager
    ( `with GitExtractedFiles(...) as alias:`) to be able
    to operate on the temporary directory containing the cloned repository
    before it is removed and the return value in the alias is the list of
    Paths.

    :param git_url: a git repo URL. The default behavior checks out the
      default branch or the URL can be suffixed with @{revision} to specify a
      commit sha, branch, tag, or release.
    :type git_url: str
    :param source_destination_map: a dictionary defining the source file
      path as keyword, relative to the root of the repository, and its value
      as an absolute path or relative path to PWD of where the file should be
      copied.
    :type source_destination_map: Mapping[str, str]
    :keyword ssh_key_path: git SSH access key path. This SSH key could be a
      deploy key. This file should have permissions 600 or will fail. If
      this is defined, there is not a need to change URLs from HTTPS to SSH
      as this will update those URLs before doing the clone. This cannot be
      defined at the same time as token.
    :type ssh_key_path: Optional[str]
    :keyword token: GitHub Personal Access Token optionally provided as a way
      to authenticate against private registries. Default will use the current
      git login, so this method is useful in non-interactive methods that
      are not already logged in and do not support SSH deploy keys. This
      cannot be defined at the same time as token.
    :type token: Optional[str]
    :keyword temp_dir_base: Optionally define the parent directory path where
      the temporary directory should be created rather than relying on
      systems' defined tmpfs.
    :type temp_dir_base: Optional[str]
    :return: List of PosixPaths for the destination paths of the new files
    """
    def __init__(
            self,
            git_url: str,
            source_destination_map: Mapping[str, str],
            **kwargs
    ):
        self.git_url, self.revision = self.get_git(git_url)
        self.source_destination_map = source_destination_map
        self.ssh_key_path = kwargs.get("ssh_key_path")
        self.token = kwargs.get("token")
        self.temp_dir_base = kwargs.get("temp_dir_base")
        self.temporary_directory = None

    def __enter__(self) -> List[Union[Path, os.PathLike]]:
        """
        Create temporary directory and clone repository.
        Copy the desired files and return their new paths.
        """
        self._only_one_access_method_allowed()
        logging.info("Creating temporary directory")
        self.temporary_directory = mkdtemp(dir=self.temp_dir_base)
        logging.info("Cloning %s to %s", self.git_url,
                     self.temporary_directory)
        self.clone_repo()
        new_files = self.copy_content()
        return list(new_files)

    # pylint: disable=redefined-builtin
    def __exit__(self, type, value, traceback):
        """Clean up repository and temp directory."""
        logging.info("Destroying temporary directory %s",
                     self.temporary_directory)
        rmtree(self.temporary_directory)
    # pylint: enable=redefined-builtin

    def _only_one_access_method_allowed(self):
        """
        Only allow zero or one of SSH Key or Personal Access Token. Using
        both raises an error, this class will not make the decision on
        which to use.
        """
        if self.ssh_key_path and self.token:
            raise ValueError("Only up to one git authentication method "
                             "allowed, but you have provided an SSH key and "
                             "Personal Access Token. Please define one.")

    @staticmethod
    def get_git(git_url: str) -> Tuple[str, Optional[str]]:
        """
        GitPython doesn't support @revision URLs, so detect when that is
        specified and split it up to get the base URL and revision separated.

        :param git_url: git url which can include the revision (commit sha,
          branch, tag, or release) with @revision style suffixing the git URL.
        :type git_url: str
        :return: base_git_url, revision if defined else None
        """
        if '@' in git_url:
            base_url, revision = git_url.split("@")
        else:
            base_url = git_url
            revision = None
        return base_url, revision

    def clone_repo(self):
        """Clone the repository. Checkout branch or revision if specified"""
        if self.ssh_key_path:
            if self.git_url.startswith("https://github.com/"):
                # try to magically switch to url to SSH git url
                self.git_url = self.git_url.replace(
                    "https://github.com/", "git@github.com:")
            # make absolute
            self.ssh_key_path = os.path.abspath(self.ssh_key_path)
            repo = Repo.clone_from(
                self.git_url,
                self.temporary_directory,
                env={"GIT_SSH_COMMAND": f"ssh -i {self.ssh_key_path}"})
        elif self.token:
            self.git_url = self.git_url.replace(
                "https://github.com",
                f"https://{self.token}:x-oauth-basic@github.com"
            )
            repo = Repo.clone_from(self.git_url, self.temporary_directory)
        else:
            repo = Repo.clone_from(self.git_url, self.temporary_directory)
        if self.revision:
            logging.info("Checking out branch/revision: %s", self.revision)
            repo.git.checkout(self.revision)

    def copy_content(self) -> Iterator[Union[Path, os.PathLike]]:
        """
        Copy the files from the cloned repository to a new destination.
        The source is relative to the repo root location (temporary
        directory) and the destination can be absolute or relative to
        the PWD.
        """
        for source, destination in self.source_destination_map.items():
            source = os.path.abspath(os.path.join(
                self.temporary_directory, source))
            destination = os.path.abspath(destination)
            logging.info("Copying %s to %s", source, destination)
            self.create_parents(destination)
            copyfile(source, destination)
            yield Path(destination)

    @staticmethod
    def create_parents(path: str):
        """
        Create parent directories for the destination path if they don't
        already exist.
        """
        # first get the parent of the intended file
        parent = os.path.dirname(path)
        if not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)


def main():
    """Main entry point when invoking script via CLI."""
    arguments = command_line()
    logging.basicConfig(level=os.environ.get('LOGLEVEL', arguments.loglevel),
                        format='%(asctime)s %(name)-12s %(levelname)-8s %('
                               'message)s')
    with open(arguments.input, 'r') as file_handle:
        imports_map = json.load(file_handle)
    for source_repo, source_destination_map in imports_map.items():
        with GitExtractedFiles(
                git_url=source_repo,
                source_destination_map=source_destination_map,
                ssh_key_path=arguments.ssh_key,
                token=os.environ.get("GITHUB_TOKEN"),
                temp_dir_base=arguments.temporary_directory_parent
        ) as extraction:
            logging.info("Copying git pages")
            # convert paths to str to be able to log as simple list
            logging.info(
                "New files available: %s", ', '.join(
                    [str(_) for _ in extraction])
            )


def command_line():
    """
    Command-line interface.

    :return: arguments via a parser.parse_args() object
    """

    class MyParser(ArgumentParser):
        """
        Override default behavior, print the whole help message for any CLI
        error.
        """
        def error(self, message: str):
            print('error: %s\n' % message, file=sys.stderr)
            self.print_help()
            sys.exit(2)

    parser = MyParser(
        add_help=True,
        description="Import files from other repositories. Define the "
                    "imports in a JSON file and pass as input argument. If "
                    "the repositories are private and require authentication "
                    "but you do not have cached credentials and are "
                    "using it in a non-interactive way, you can either "
                    "define a Personal Access Token in your Environment "
                    "under variable GITHUB_TOKEN or you can specify a path "
                    "to an SSH Deploy Key.",
    )
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    parser.add_argument(
        "-v", "--verbose",
        help="Set logging to verbose",
        action="store_const", dest="loglevel",
        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument("input",
                        help="The input json with a hash of repo URLs and "
                             "their value being hash of source path and "
                             "destination path. Source path should be "
                             "relative to root of repository and the "
                             "destination path can be absolute or it can be "
                             "relative to the PWD.")
    parser.add_argument("-t", "--temporary-directory-parent",
                        help="Optionally set the parent directory for "
                             "temporary directories or else will use system "
                             "tmp default.")
    parser.add_argument("--ssh-key",
                        help="Path to an SSH Key with access to the "
                             "repository. This file needs 600 permissions. "
                             "This cannot be defined in combination with "
                             "GITHUB_TOKEN environment variable.")
    return parser.parse_args()


if __name__ == "__main__":
    main()
