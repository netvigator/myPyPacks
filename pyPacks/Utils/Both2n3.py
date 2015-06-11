#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utility Both2n3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# The GNU General Public License is available from:
#   The Free Software Foundation, Inc.
#   51 Franklin Street, Fifth Floor
#   Boston MA 02110-1301 USA
#
#   http://www.gnu.org/licenses/gpl.html
#
# Copyright 2004-2012 Rick Graves
#
# here, must use built in map -- cannot import iMap

from Utils.Version  import PYTHON3


def print3( *args, **kwargs ):
    #
    from sys import stdout
    #
    sep     = kwargs.pop( 'sep',  ' '    )
    beg     = kwargs.pop( 'beg',  ''     )
    end     = kwargs.pop( 'end',  '\n'   )
    file    = kwargs.pop( 'file', stdout )
    #
    if kwargs: raise TypeError( 'extra keywords: %s' % kwargs )
    #
    # here, must use built in map -- cannot import iMap
    #
    file.write( '%s%s%s' % ( beg, sep.join( map( str, args ) ), end ) )


    

if PYTHON3:
    #
    safe_input = input
    #
else:
    #
    safe_input = raw_input




if PYTHON3:
    #
    translate = str.translate
    maketrans = str.maketrans
    #
else:
    #
    from string import translate, maketrans


if PYTHON3:
    #
    def getZeroFilled( s, i ): return s.zfill( i )
    #
else:
    #
    from string import zfill as getZeroFilled



_tNumbs = 1234, 1.23, 88**88

# here, must use built in map -- cannot import iMap

setNumberTypes = frozenset( map( type, _tNumbs ) )




if PYTHON3:
    #
    getNext = next
    #
else:
    #
    o = iter( range(5) )
    #
    try:
        #
        next( o )
        #
        getNext = next
        #
    except:
        #
        def getNext( o ):
            #
            return o.next()



if PYTHON3:
    #
    from http.client    import BadStatusLine
    from http.cookiejar import CookieJar, LWPCookieJar as FileCookieJar
    from html.entities  import entitydefs
    from io             import StringIO, BytesIO
    from sys            import getdefaultencoding
    from urllib.error   import HTTPError, URLError
    from urllib.parse   import urlencode, urljoin, urlsplit, urlunsplit, \
                            unquote, quote, quote_plus, unquote_plus
    from urllib.request import urlopen, Request, build_opener, install_opener, \
                            HTTPCookieProcessor, urlretrieve
    #
else:
    #
    from cookielib      import CookieJar, LWPCookieJar as FileCookieJar
    from htmlentitydefs import entitydefs
    from httplib        import BadStatusLine
    from StringIO       import StringIO
    from sys            import getdefaultencoding
    from urllib2        import HTTPError, URLError, Request, urlopen, \
                                build_opener, install_opener, URLError, \
                                HTTPCookieProcessor
    from urllib         import urlencode, urlencode, unquote, quote, \
                                quote_plus, unquote_plus, urlretrieve
    # urlopen, 
    from urlparse       import urljoin, urlsplit, urlunsplit

    BytesIO = StringIO


def getBytes( s, encoding = getdefaultencoding() ): return s



try: 
    reduce( lambda x, y: x+y, range(5) )
    Reduce = reduce
except NameError: # reduce removed to functools in python3
    from functools import reduce as Reduce





if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    if getZeroFilled( '1', 3 ) != '001':
        #
        lProblems.append( 'getZeroFilled()' )
        #
    #
    o = iter( range(5) )
    #
    try:
        u = getNext( o )
    except:
        #
        lProblems.append( 'getNext()' )
        #
    #

    #
    #
    sayTestResult( lProblems )