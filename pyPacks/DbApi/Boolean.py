#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# DbApi functions Boolean
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
# Copyright 2004-2011 Rick Graves
#

setBooleanTrue          = frozenset( ( 't', 'true',  'y', 'yes', '1' ) )
setBooleanFalse         = frozenset( ( 'f', 'false', 'n', 'no',  '0' ) )


setNumberTypes          = frozenset( ( int, float, long, bool ) )


tBooleansSQL            = ( 'FALSE', 'TRUE' )


def _isNumber( u ): return type( u ) in setNumberTypes




def getBooleanInteger( uValue, bDebug = 1 ):
    #
    from String.Get     import getContentOutOfQuotes
    from Utils.Both2n3  import print3
    #
    if _isNumber( uValue ):
        #
        iValue = int( bool( uValue ) )
        #
    else:
        #
        iValue = None
        #
        uValue = getContentOutOfQuotes( uValue ).lower()
        #
        if   uValue in setBooleanTrue:  iValue = 1
        elif uValue in setBooleanFalse: iValue = 0
        else:
            if bDebug:
                print3( uValue )
            raise TypeError
        #
    #
    return iValue



def getBoolFactory( sSystemSQL ):
    #
    if sSystemSQL == 'sqlite':
        #
        getBool = getBooleanInteger
        #
    else:
        #
        def getBool( uValue ):
            #
            return tBooleansSQL[ getBooleanInteger( uValue ) ]
    #
    return getBool



if __name__ == "__main__":
    #
    from Iter.AllVers   import lMap, tMap
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    tBoolStrings = ( 8, 't', 'true',  'y', 'yes', '1', 0, 'f', 'false', 'n', 'no',  '0' )
    #
    lBools = tMap( getBooleanInteger, tBoolStrings )
    #
    if lBools != ( 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0 ):
        #
        lProblems.append( 'getBooleanInteger() valid values' )
        #
    #
    try:
        #
        getBooleanInteger( 'xyz', bDebug = 0 )
        #
    except TypeError:
        #
        pass
        #
    else:
        #
        # we are here only if a TypeError exception was not raised!
        #
        lProblems.append( 'getBooleanInteger() invalid value' )
        #
    #
    dResults = {}
    #
    for sSystemSQL in ( 'sqlite', 'postgresql' ):
        #
        getBool = getBoolFactory( sSystemSQL )
        #
        dResults[ sSystemSQL ] = lMap( getBool, tBoolStrings )
        #
    #
    if dResults[ 'sqlite' ] != [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]:
        #
        lProblems.append( 'getBoolFactory() for sqlite'  )
        #
    #
    if dResults[ 'postgresql' ] != \
            [ 'TRUE',  'TRUE',  'TRUE',  'TRUE',  'TRUE',  'TRUE',
              'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE' ]:
        #
        lProblems.append( 'getBoolFactory() for SQL compatibles' )
        #
    #
    sayTestResult( lProblems )