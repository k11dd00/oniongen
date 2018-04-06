# MIT License
#
# Copyright (c) 2018 k1dd00
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
# SOFTWARE

#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
# pylint: disable=C0103,C0301,W1202,W0212

"""
Deep Web .onion URL Generator.
This is a small cli tool that generates and validades .onion urls.
"""

import os
import sys
import argparse
from colorama import Fore
from utils.log import Log
from utils.ioutils import IOUtils
from cmd.cmdstrategy import CommandStrategy
from utils.clihelpformatter import CliHelpFormatter

parser = argparse.ArgumentParser(
    prog="oniongen.py",
    usage="python oniongen.py <options>",
    formatter_class=CliHelpFormatter
)

parser.add_argument(
    "url",
    nargs="?",
    help="the .onion url to validate"
)

parser.add_argument(
    "-c",
    "--count",
    metavar="",
    type=int,
    help="the number of urls to generate(default: 100)"
)

parser.add_argument(
    "-p",
    "--prefix",
    metavar="",    
    help="the url prefix"
)

parser.add_argument(
    "-s",
    "--suffix",
    metavar="",    
    help="the url suffix"
)

parser.add_argument(
    "-w",
    "--workers",
    metavar="", 
    type=int,   
    help="the number of url validation workers"
)

parser.add_argument(
    "-g",
    "--generate",
    action="store_true",
    help="generates random .onion urls"
)

parser.add_argument(
    "-i",
    "--input",
    metavar="",
    type=argparse.FileType('r'),
    help="the url list file"
)

parser.add_argument(
    "-o",
    "--output",
    metavar="",
    type=argparse.FileType('w'),
    help="the output file"
)

parser.add_argument(    
    "--protocol",
    metavar="",    
    help="the protocol(http or https)"
)

parser.add_argument(
    "--tld",
    metavar="",    
    help="the top level domain(default: .onion)"
)

parser.add_argument(
    "--validate",
    action="store_true",
    help="validates the given url"
)

parser.add_argument(
    "--discover",
    action="store_true",
    help="enables the discover mode"
)

parser.add_argument(
    "--proxy-ip",
    metavar="",    
    help="the proxy ip(default: 127.0.0.1)"
)

parser.add_argument(
    "--proxy-port",
    metavar="",
    type=int,
    help="the proxy port(default: 9050)"
)

parser.add_argument(
    "--dry-run",
    action="store_true",
    help="disables proxy and url validation"
)

parser.add_argument(
    "--version",
    action="version",
    version="v1.0.0",
    help="shows the current version"
)

parser.set_defaults(count=100)
parser.set_defaults(prefix="")
parser.set_defaults(suffix="")
parser.set_defaults(protocol="http")
parser.set_defaults(tld=".onion")
parser.set_defaults(timeout=10)
parser.set_defaults(workers=100)
parser.set_defaults(proxy_ip="127.0.0.1")
parser.set_defaults(proxy_port=9050)
parser.set_defaults(dry_run=False)

def main(args):
    """
    Executes the oniongen cli tool
    """

    try:

        executor = CommandStrategy.resolve(args)
        executor.execute(args)

        sys.stdout.close()
        sys.stderr.close()
    
    except KeyError:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    except ValueError as error:
        Log.error(str(error))
        sys.exit(1)

if __name__ == "__main__":

    try:

        url = None

        if IOUtils.is_piped_input():
            url = IOUtils.read_piped_input()

        cli_args = parser.parse_args()
        cli_args.url = cli_args.url or url

        main(cli_args)

    except KeyboardInterrupt:
        Log.raw_info("")
        Log.warn("User requested to stop")
        Log.warn("Killing all processes")
        os._exit(0)
