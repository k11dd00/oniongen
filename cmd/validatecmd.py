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
from http.htmlparser import HtmlParser
from concurrent.futures import ThreadPoolExecutor

class ValidateCommand(Command):
    """
    The ValidateCommand class.

    This class handles the option --validate
    The validate command tries to validate a given .onion url.
    """

    def __init__(self):
        Command.__init__(self, self.__validate)

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

    def __validate(self, kwargs):
        """
        Handles the operation --validate

        Parameters
        ----------
        kwargs: dict
            The dictionary parameter containing the attributes:
            * urls    - The url list to be validated
            * workers - The number of url validation workers
        
        Returns
        -------
        result: str
            The list of urls
        """

        result = []

        urls = kwargs["urls"]
        workers = kwargs["workers"]
        url_list = urls.splitlines()

        Log.info("Running HTTP status check in {} url(s)".format(len(url_list)))
        Log.info("Be patient, this may take a looooong time...")

        pool = ThreadPoolExecutor(max_workers=workers)
        for url in url_list:
            pool.submit(self.__url_check, url=url, urls=result)

        pool.shutdown(wait=True)

        Log.info("Found {} of {} urls".format(len(result), len(url_list)))

        return "\n".join(result)

    def execute(self, args):
        """
        The abstract execute method implementation.
        Validates and executes the given cli arguments.
        """

        if not args.url and not args.input:
            raise ValueError("No url given")

        urls = args.url or args.input.read()
        self.delegate(args, urls=urls, workers=args.workers)
