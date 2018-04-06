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

import socket
import socks

class TorProxy(object):
    """
    The TorProxy class

    This class performs a Tor proxy setup
    """

    @staticmethod
    def setup(proxy_ip, proxy_port):
        """
        Setup the Tor proxy

        Parameters
        ----------
        proxy_ip: str
            The proxy ip
        proxy_port: int
            The proxy port
        """

        def create_connection(address, timeout=10, source_address=None):
            """
            The inner function create_conection

            Parameters
            ----------
            address: tuple
                The destination address
            timeout: int
                The connection timeout
            source_address: tuple
                The connection source address
            
            Returns
            -------
            connection: sock
                The socket connection
            """

            try:
                
                sock = socks.socksocket()
                sock.connect(address)
                return sock

            except socks.ProxyConnectionError as error:
                raise ValueError(str(error))

            except socks.SOCKS5Error as error:
                raise ValueError(str(error))

            except socks.GeneralProxyError as error:
                raise ValueError(str(error))
    
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, proxy_ip, proxy_port)
        socket.socket = socks.socksocket
        socket.create_connection = create_connection
