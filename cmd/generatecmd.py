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

import urllib2
from colorama import Fore
from utils.log import Log
from command import Command
from http.onion import Onion
from http.htmlparser import HtmlParser
from concurrent.futures import ThreadPoolExecutor

class GenerateCommand(Command):
    """
    The GenerateCommand class.

    This class handles the options -g, --generate and --dry-run
    The generate command generates and validates .onion urls.
    """

    def __init__(self):
        Command.__init__(self, self.__generate)
        self.onion = Onion()

    def __url_check(self, url=None, urls=[]):
        """
        Checks if the given url exists.

        Parameters
        ----------
        url: str
            The .onion url
        urls: list
            The result list
        """

        try:
                        
            http_status = urllib2.urlopen(url).getcode()
            
            if http_status < 400:
                html = urllib2.urlopen(url).read()
                parser = HtmlParser(html)
                title = parser.get_title()

                Log.info("Found: \033[1m{}{} | {}{}\033[0m".format(Fore.GREEN, title, url, Fore.RESET))
                urls.append(url)

        except urllib2.URLError:
            pass                

    def __generate(self, kwargs):
        """
        Handles the operations -g, --generate and --dry-run

        Parameters
        ----------
        kwargs: dict
            The dictionary parameter containing the attributes:
            * count    - The number of urls to generate
            * prefix   - The url prefix
            * suffix   - The url suffix
            * protocol - The protocol
            * tld      - The top level domain
            * workers  - The number of url validation workers
            * dry_run  - The dry run mode
        
        Returns
        -------
        result: str
            The list of urls
        """

        result = []

        size = kwargs["count"]
        prefix = kwargs["prefix"]
        suffix = kwargs["suffix"]
        protocol = kwargs["protocol"]
        tld = kwargs["tld"]
        workers = kwargs["workers"]
        dry_run = kwargs["dry_run"]

        Log.info("Generating {} {} url(s)".format(size, tld))
        Log.info("Protocol: {}".format(protocol.upper()))
        Log.info("Prefix:   {}".format(prefix if prefix else None))
        Log.info("Suffix:   {}".format(suffix if suffix else None))
        Log.info("TLD:      {}".format(tld))
        Log.info("Workers:  {}".format(workers))
        
        urls = []
        index = 1
        pool = ThreadPoolExecutor(max_workers=workers)
        
        while index <= size:
            url = self.onion.generate(prefix, suffix, protocol, tld)
            urls.append(url)
            index += 1

        Log.info("Generated {} {} url(s)".format(len(urls), tld))

        if dry_run:
            Log.warn("Dry run enabled, skipping url validation")
            return "\n".join(urls)

        Log.info("Running HTTP status check in all urls")
        Log.info("Be patient, this may take a looooong time...")
        
        for url in urls:
            pool.submit(self.__url_check, url=url, urls=result)

        pool.shutdown(wait=True)

        Log.info("Found {} of {} urls".format(len(result), len(urls)))

        return "\n".join(result)

    def execute(self, args):
        """
        The abstract execute method implementation.
        Validates and executes the given cli arguments.
        """

        url_length = len(args.prefix) + len(args.suffix)
        if url_length > 16:
            raise ValueError("URL prefix + suffix cannot be greater than 16 chars")

        self.delegate(
            args, 
            prefix=args.prefix, 
            suffix=args.suffix,
            protocol=args.protocol, 
            tld=args.tld,            
            workers=args.workers,
            count=args.count,
            dry_run=args.dry_run)
