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

# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
# pylint: disable=C0103,C0301,W1202,W0212

import abc
import sys
import socks
import logging
from colorama import Fore
from utils.log import Log
from utils.ioutils import IOUtils
from http.torproxy import TorProxy
from http.torcheck import TorCheck

class Command(object):
    """
    The abstract Command class.

    All command handlers should inherit this class.
    This class has a default command execution
    based on the given cli arguments. It also handles
    the piped/output option.
    """

    __metaclass__ = abc.ABCMeta

    BANNER = """
             <ONIONGEN>
    Deep Web .onion URL Generator

                        [k1dd00]
                          v1.0.0
    """

    def __init__(self, handler):
        """
        Initiates the class.

        Parameters
        ----------
        handler: function
            The function handler to be executed based on the given cli args.
        """

        self.handler = handler

    def delegate(self, args, **kwargs):
        """
        Executes the command based on the given cli args.

        Parameters
        ----------
        args: Namespace
            The argparse cli arguments
        kwargs: dict
            The arguments to be passed to the handler
        """

        Log.raw_info(self.BANNER)

        if not args.dry_run:
            
            Log.info("Setting up proxy config")
            Log.info("Proxy IP:   {}".format(args.proxy_ip))
            Log.info("Proxy PORT: {}".format(args.proxy_port))

            TorProxy.setup(args.proxy_ip, args.proxy_port)
            tor = TorCheck()
            tor_status = ""

            Log.info("Checking Tor Status")
        
            success = tor.check_tor_status()
            if success:
                tor_status = "{}{}".format(Fore.GREEN, "\033[1mREADY\033[0m")
            else:
                tor_status = "{}{}".format(Fore.RED, "\033[1mNOT READY\033[0m")

            Log.info("Tor Status: {}".format(tor_status))
            Log.info("Checking IP Address")
            Log.info("IP: \033[1m{}{}\033[0m".format(Fore.GREEN, tor.check_ip()))

            if not success:
                raise ValueError("Unable to route traffic through Tor")

        else:

            Log.warn("Dry run enabled, skipping proxy setup")

        result = self.handler(kwargs)
        result_std = "{}\n".format(result)

        if args.output:
            out = args.output
            out.write(result)
            out.close()

        if args.dry_run or (not args.output and IOUtils.is_piped_output()):
            sys.stdout.write(result_std)

    @abc.abstractmethod
    def execute(self, args):
        """
        Handles the command execution.
        """
        raise NotImplementedError('The execute method must be implemented')
