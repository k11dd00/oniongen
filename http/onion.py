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

from random import randint

class Onion(object):
    """
    The Onion class.

    This class generates random .onion urls
    based on the rules that can be found at:
    https://en.wikipedia.org/wiki/.onion
    """

    DOMAIN_LENGTH = 16
    CHARS = '234567abcdefghijklmnopqrstuvwxyz'
    
    def __init__(self):
        self.url_format = "{}://{}{}{}{}"

    def __randomize(self):
        """
        Generates random position

        Returns
        -------
        position: int
            The random position
        """

        return randint(0, len(self.CHARS) - 1)

    def __url_length(self, suffix, prefix):
        """
        Calculates the url length

        Parameters
        ----------
        prefix: str
            The url prefix
        suffix: str
            The url suffix
        
        Returns
        -------
        length: int
            The url length
        """

        return self.DOMAIN_LENGTH - (len(suffix) + len(prefix))

    def generate(self, prefix="", suffix="", protocol="http", tld=".onion"):
        """
        Generates a random .onion url

        Parameters
        ----------
        prefix: str
            The url prefix
        suffix: str
            The url suffix
        protocol: str
            The protocol
        tld: str
            The top level domain
        
        Returns
        -------
        url: str
            The random .onion url
        """

        random_chars = []
        url_length = self.__url_length(prefix, suffix)
        
        for _ in xrange(0, url_length):
            pos = self.__randomize()
            random_chars.append(self.CHARS[pos])

        return self.url_format.format(
                protocol, 
                prefix, 
                "".join(random_chars),
                suffix,
                tld) 
