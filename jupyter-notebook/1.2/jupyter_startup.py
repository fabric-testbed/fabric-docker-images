#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)
import json
import os
import traceback
from datetime import datetime

from git import Repo
from git import Git
from atomicwrites import atomic_write


class JupyterStartup:
    DEFAULT_NOTEBOOK_LOCATION = "/home/fabric/work/jupyter-examples"
    TOKENS_LOCATION = "/home/fabric/.tokens.json"
    TAGS = "rel1.1.1"
    REPO_URL = "https://github.com/fabric-testbed/jupyter-examples.git"
    REFRESH_TOKEN = "refresh_token"
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    CREATED_AT = "created_at"

    def __init__(self):
        self.notebook_location = os.environ["FABRIC_NOTEBOOK_LOCATION"]
        if self.notebook_location is None:
            self.notebook_location = self.DEFAULT_NOTEBOOK_LOCATION

        self.token_location = os.environ["FABRIC_TOKEN_LOCATION"]
        if self.token_location is None:
            self.token_location = self.TOKENS_LOCATION

        self.tags = os.environ["FABRIC_NOTEBOOK_TAGS"]
        if self.tags is None:
            self.tags = self.TAGS

        self.repo_url = os.environ["FABRIC_NOTEBOOK_REPO_URL"]
        if self.repo_url is None:
            self.repo_url = self.REPO_URL

    def clone_notebooks(self):
        try:
            repo = Repo.clone_from(self.repo_url, self.notebook_location, no_checkout=True)
            g = Git(self.notebook_location)
            g.checkout(self.tags)
        except Exception as e:
            print("Failed to clone github repository for notebooks")
            print("Exception: " + str(e))
            traceback.print_exc()

    def initialize(self):
        """
        Initialize Jupyter Notebook Container
        """
        if not os.path.exists(self.notebook_location):
            """
            First time login into Jupyter Hub, user does not have a persistent volume
            Clone the Git Hub repo
            """
            print("Github repository for notebooks does not exist")
            self.clone_notebooks()

        if not os.path.exists(self.token_location):
            # New notebook container has been created
            # Create a token file
            print("Creating token file")
            tokens_json = {self.REFRESH_TOKEN: os.environ["CILOGON_REFRESH_TOKEN"],
                           self.CREATED_AT: datetime.strftime(datetime.utcnow(), self.TIME_FORMAT)}

            with atomic_write(self.token_location, overwrite=True) as f:
                json.dump(tokens_json, f)


if __name__ == "__main__":
    js = JupyterStartup()
    js.initialize()

