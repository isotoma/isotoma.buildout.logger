# Copyright 2010 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess, os, sys

class Logger(object):

    def load(self, buildout):
        """
        Called when an extension is loaded, before recipe processing occurs

        Consults ${buildout:buildout-log} to find out where we are writing to
        Then spawns tee and gives it our stdout and stderr

        End result is normal console output and a log containing the same info
        """
        self.log = buildout['buildout'].get("buildout-log", "log.txt")

        self.tee = subprocess.Popen(["tee", self.log], stdin=subprocess.PIPE)
        os.dup2(self.tee.stdin.fileno(), sys.stdout.fileno())
        os.dup2(self.tee.stdin.fileno(), sys.stderr.fileno())

    def unload(self, buildout):
        """
        Called when an extension is unloaded, after recipe processing occurs

        Print out where we wrote the log file, for convenient c&p
        """
        print "Wrote log to: ", self.log

logger = Logger()


# These are the entry points listed in setup.py:
def load(buildout):
    logger.load(buildout)

def unload(buildout):
    logger.unload(buildout)
