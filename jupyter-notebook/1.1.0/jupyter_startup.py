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
import os
import subprocess

from fabrictestbed.slice_manager import SliceManager


class JupyterStartup:
    DEFAULT_NOTEBOOK_LOCATION = "/home/fabric/work/jupyter-examples"
    TOKENS_LOCATION = "/home/fabric/.tokens.json"

    def __init__(self):
        self.notebook_location = os.environ["FABRIC_NOTEBOOK_LOCATION"]
        if self.notebook_location is None:
            self.notebook_location = self.DEFAULT_NOTEBOOK_LOCATION

        self.token_location = os.environ["FABRIC_TOKEN_LOCATION"]
        if self.token_location is None:
            self.token_location = self.TOKENS_LOCATION

        self.credmgr_host = os.environ['FABRIC_CREDMGR_HOST']
        self.orchestrator_host = os.environ['FABRIC_ORCHESTRATOR_HOST']

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
            cmd = ["git", "clone", "https://github.com/fabric-testbed/jupyter-examples.git",
                   self.DEFAULT_NOTEBOOK_LOCATION]
            FNULL = open(os.devnull, 'w')
            rt_code = subprocess.call(cmd, stdout=FNULL)
            if rt_code != 0:
                print("Failed to clone github repository for notebooks")

        if not os.path.exists(self.token_location):
            # New notebook container has been created
            # Initializing the slice manager loads the tokens and saves them at the location specified in token_location
            slice_manager = SliceManager(oc_host=self.orchestrator_host, cm_host=self.credmgr_host,
                                         token_location=self.token_location)
            slice_manager.initialize()


if __name__ == "__main__":
    js = JupyterStartup()
    js.initialize()