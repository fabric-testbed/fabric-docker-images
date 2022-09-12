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

from fss_utils.sshkey import FABRICSSHKey
from git import Repo
from git import Git
from atomicwrites import atomic_write
import wget
import tarfile


class JupyterStartup:
    DEFAULT_NOTEBOOK_LOCATION = "/home/fabric/work/"
    DEFAULT_FABRIC_CONFIG_LOCATION = "/home/fabric/work/fabric_config"
    TOKENS_LOCATION = "/home/fabric/.tokens.json"
    TAGS = "rel1.3"
    REPO_URL = "https://github.com/fabric-testbed/jupyter-examples/archive/refs/tags/"
    REFRESH_TOKEN = "refresh_token"
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    CREATED_AT = "created_at"
    DEFAULT_PRIVATE_SSH_KEY = "/home/fabric/.ssh/id_rsa"
    DEFAULT_PUBLIC_SSH_KEY = "/home/fabric/.ssh/id_rsa.pub"
    DEFAULT_FABRIC_LOG_LEVEL = "INFO"
    DEFAULT_FABRIC_LOG_FILE = "/tmp/fablib/fablib.log"

    FABRIC_CREDMGR_HOST = "FABRIC_CREDMGR_HOST"
    FABRIC_ORCHESTRATOR_HOST = "FABRIC_ORCHESTRATOR_HOST"
    FABRIC_TOKEN_LOCATION = "FABRIC_TOKEN_LOCATION"
    FABRIC_PROJECT_ID = "FABRIC_PROJECT_ID"
    FABRIC_NOTEBOOK_LOCATION = "FABRIC_NOTEBOOK_LOCATION"
    FABRIC_NOTEBOOK_TAGS = "FABRIC_NOTEBOOK_TAGS"
    FABRIC_NOTEBOOK_REPO_URL = "FABRIC_NOTEBOOK_REPO_URL"
    FABRIC_CONFIG_LOCATION = "FABRIC_CONFIG_LOCATION"
    FABRIC_BASTION_HOST = "FABRIC_BASTION_HOST"
    FABRIC_BASTION_USERNAME = "FABRIC_BASTION_USERNAME"
    FABRIC_BASTION_KEY_LOCATION = "FABRIC_BASTION_KEY_LOCATION"
    FABRIC_SLICE_PRIVATE_KEY_FILE = "FABRIC_SLICE_PRIVATE_KEY_FILE"
    FABRIC_SLICE_PUBLIC_KEY_FILE = "FABRIC_SLICE_PUBLIC_KEY_FILE"
    FABRIC_SLICE_PRIVATE_KEY_PASSPHRASE = "FABRIC_SLICE_PRIVATE_KEY_PASSPHRASE"
    FABRIC_BASTION_PRIVATE_KEY_NAME = "FABRIC_BASTION_PRIVATE_KEY_NAME"
    FABRIC_SLICE_PRIVATE_KEY_NAME = "FABRIC_SLICE_PRIVATE_KEY_NAME"
    FABRIC_SLICE_PUBLIC_KEY_NAME = "FABRIC_SLICE_PUBLIC_KEY_NAME"
    FABRIC_LOG_FILE = "FABRIC_LOG_FILE"
    FABRIC_LOG_LEVEL = "FABRIC_LOG_LEVEL"

    def __init__(self):
        self.notebook_location = os.environ[self.FABRIC_NOTEBOOK_LOCATION]
        if self.notebook_location is None:
            self.notebook_location = self.DEFAULT_NOTEBOOK_LOCATION

        self.token_location = os.environ[self.FABRIC_TOKEN_LOCATION]
        if self.token_location is None:
            self.token_location = self.TOKENS_LOCATION

        self.tags = os.environ[self.FABRIC_NOTEBOOK_TAGS]
        if self.tags is None:
            self.tags = self.TAGS

        self.repo_url = os.environ[self.FABRIC_NOTEBOOK_REPO_URL]
        if self.repo_url is None:
            self.repo_url = self.REPO_URL

        self.config_location = os.environ[self.FABRIC_CONFIG_LOCATION]
        if self.config_location is None:
            self.config_location = self.DEFAULT_FABRIC_CONFIG_LOCATION

    def create_config(self):
        try:
            os.mkdir(self.config_location)
            environment_vars = {
                self.FABRIC_CREDMGR_HOST: os.environ[self.FABRIC_CREDMGR_HOST],
                self.FABRIC_ORCHESTRATOR_HOST: os.environ[self.FABRIC_ORCHESTRATOR_HOST],
                self.FABRIC_BASTION_HOST: os.environ[self.FABRIC_BASTION_HOST],
                self.FABRIC_PROJECT_ID: '<Update Project Id>',
                self.FABRIC_BASTION_USERNAME: '<Update User Name>',
                self.FABRIC_BASTION_KEY_LOCATION: f'{self.config_location}/{os.environ[self.FABRIC_BASTION_PRIVATE_KEY_NAME]}',
                self.FABRIC_SLICE_PRIVATE_KEY_FILE: f'{self.config_location}/{os.environ[self.FABRIC_SLICE_PRIVATE_KEY_NAME]}',
                self.FABRIC_SLICE_PUBLIC_KEY_FILE: f'{self.config_location}/{os.environ[self.FABRIC_SLICE_PUBLIC_KEY_NAME]}',
                self.FABRIC_SLICE_PRIVATE_KEY_PASSPHRASE: '<Update Passphrase>',
                self.FABRIC_LOG_LEVEL: self.DEFAULT_FABRIC_LOG_LEVEL,
                self.FABRIC_LOG_FILE: self.DEFAULT_FABRIC_LOG_FILE
            }
            string_to_write = ""
            for key, value in environment_vars.items():
                if '<' in value and '>':
                    string_to_write += f"#export {key}={value}\n"
                else:
                    string_to_write += f"export {key}={value}\n"

            with atomic_write(f'{self.config_location}/fabric_rc', overwrite=True) as f:
                f.write(string_to_write)

            string_to_write = f"UserKnownHostsFile /dev/null\n" \
                              f"StrictHostKeyChecking no\n" \
                              f"ServerAliveInterval 120 \n" \
                              f"Host bastion-?.fabric-testbed.net\n" \
                              f"User <Update Bastion User Name>\n" \
                              f"ForwardAgent yes\n" \
                              f"Hostname %h\n" \
                              f"IdentityFile {self.config_location}/{os.environ[self.FABRIC_BASTION_PRIVATE_KEY_NAME]}\n" \
                              f"IdentitiesOnly yes\n" \
                              f"Host * !bastion-?.fabric-testbed.net\n" \
                              f"ProxyJump <Update Bastion User Name>@{os.environ[self.FABRIC_BASTION_HOST]}:22\n"
            with atomic_write(f'{self.config_location}/ssh_config', overwrite=True) as f:
                f.write(string_to_write)
        except Exception as e:
            print("Failed to create config directory and default environment file")
            print("Exception: " + str(e))
            traceback.print_exc()

    def clone_notebooks(self):
        try:
            repo = Repo.clone_from(self.repo_url, self.notebook_location, no_checkout=True)
            g = Git(self.notebook_location)
            g.checkout(self.tags)
        except Exception as e:
            print("Failed to clone github repository for notebooks")
            print("Exception: " + str(e))
            traceback.print_exc()

    def download_notebooks(self):
        try:
            file_name_release = f"{self.repo_url}/{self.tags}.tar.gz"
            print(f"Downloading the {file_name_release}")
            file_name = wget.download(f"{self.repo_url}/{self.tags}.tar.gz", self.notebook_location)
            print(f"Extracting the tarball for the Downloaded code: {file_name}")
            with tarfile.open(file_name) as f:
                f.extractall()
            print(f"Removing the downloaded tarball")
            os.remove(file_name)
        except Exception as e:
            print("Failed to download github repository for notebooks")
            print("Exception: " + str(e))
            traceback.print_exc()

    def create_tokens_file(self):
        try:
            tokens_json = {self.REFRESH_TOKEN: os.environ["CILOGON_REFRESH_TOKEN"],
                           self.CREATED_AT: datetime.strftime(datetime.utcnow(), self.TIME_FORMAT)}

            with atomic_write(self.token_location, overwrite=True) as f:
                json.dump(tokens_json, f)
        except Exception as e:
            print("Failed to create tokens file")
            print("Exception: " + str(e))
            traceback.print_exc()

    def initialize(self):
        """
        Initialize Jupyter Notebook Container
        """
        if not os.path.exists(f"{self.notebook_location}/jupyter-examples-{self.tags}"):
            """
            First time login into Jupyter Hub, user does not have a persistent volume
            Download the Release Tag
            """
            print("Download Jupyter Examples")
            self.download_notebooks()

        if not os.path.exists(self.token_location):
            # New notebook container has been created
            # Create a token file
            print("Creating token file")
            self.create_tokens_file()

        if not os.path.exists(self.config_location):
            print("Creating config directory and all files")
            self.create_config()

        # Create SSH Keys
        ssh_key = FABRICSSHKey.generate(comment="fabric@localhost", algorithm="rsa")
        with atomic_write(f'{self.DEFAULT_PRIVATE_SSH_KEY}', overwrite=True) as f:
            f.write(ssh_key.private_key)
        with atomic_write(f'{self.DEFAULT_PUBLIC_SSH_KEY}', overwrite=True) as f:
            f.write(f'{ssh_key.name} {ssh_key.public_key} {ssh_key.comment}')

        # Default key in config directory
        default_ssh_priv_key_config = f'{self.config_location}/{os.environ[self.FABRIC_SLICE_PRIVATE_KEY_NAME]}'
        default_ssh_pub_key_config = f'{self.config_location}/{os.environ[self.FABRIC_SLICE_PUBLIC_KEY_NAME]}'
 
        if not os.path.exists(default_ssh_priv_key_config):
            with atomic_write(default_ssh_priv_key_config, overwrite=True) as f:
                f.write(ssh_key.private_key)

        if not os.path.exists(default_ssh_pub_key_config):
            with atomic_write(default_ssh_pub_key_config, overwrite=True) as f:
                f.write(f'{ssh_key.name} {ssh_key.public_key} {ssh_key.comment}')


if __name__ == "__main__":
    js = JupyterStartup()
    js.initialize()

