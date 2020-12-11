# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import os
import time
import sys
import signal
import subprocess
from contextlib import contextmanager

import click


@contextmanager
def kill_process_group_afterwards():
    os.setpgrp()
    try:
        yield
    finally:
        # Kill all processes in my group
        os.killpg(0, signal.SIGKILL)


@click.group(name="experiments")
def experiments_cli():
    pass


@experiments_cli.command(name="run")
@click.argument("script_path", type=click.Path(exists=True), metavar="<script>")
@click.argument("script_args", nargs=-1, type=click.UNPROCESSED)
def run_experiment(script_path, script_args):
    with kill_process_group_afterwards():
        subprocess.Popen(
            ["scl", "envision", "start", "-s", "./scenarios", "-p", "8081"],
        )
        # Just in case: give Envision a bit of time to warm up
        time.sleep(0.5)
        script = subprocess.Popen([sys.executable, script_path, *script_args],)
        script.communicate()


experiments_cli.add_command(run_experiment)