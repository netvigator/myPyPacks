#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Utils python Version
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


def _getVersionTuple():
    #
    from sys import version
    #
    lParts = version.split()
    #
    tVersion = lParts[0].split( '.' )
    #
    return tVersion
    

tVERSION = _getVersionTuple()



def _isPython3orMore():
    #
    iMajVers = tVERSION[0]
    #
    return iMajVers >= '3'


PYTHON3 = _isPython3orMore()

PYTHON2 = not PYTHON3


def isVersAtLeast( sNeed ):
    #
    '''
    pass to sNeed param string in form of "2.6"
    returns whether this version is at least sNeed
    '''
    #
    sGot = '.'.join( tVERSION[:2] )
    #
    return sGot >= sNeed
    

def isVersBefore( sNeed ):
    #
    '''
    pass to sNeed param string in form of "2.6"
    returns whether this version is before sNeed
    '''
    #
    sGot = '.'.join( tVERSION[:2] )
    #
    return sGot < sNeed


def getSayVersion():
    #
    return 'Python %s' % '.'.join( tVERSION )
    

if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    def isPython2dot4():
        #
        return tVERSION[:2] == ( 2, 4 )
    #
    PYTHON2DOT4 = isPython2dot4()
    #
    if not isVersAtLeast( '2.4' ):
        #
        lProblems.append( 'isVersAtLeast() we only support 2.4 and later' )
        #
    #
    if isVersBefore( '2.4' ):
        #
        lProblems.append( 'isVersBefore() we only support 2.4 and later' )
        #
    #
    if isVersAtLeast( '3.9' ):
        #
        lProblems.append( 'isVersAtLeast() 3.9 might be a future version' )
        #
    #
    if not isVersBefore( '3.9' ):
        #
        lProblems.append( 'isVersBefore() 3.9 might be a future version' )
        #
    #
    sayTestResult( lProblems )