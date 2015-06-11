#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Object functions Design Patterns
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


class ObserverClass( object ):
    #
    """
    Implements observer design pattern.
    Clients/observers can subscribe/unsubscribe by calling
    registerObserver( self )/removeObserver( self )
    (self would be a reference to the client object).
    Can also register clients/observers on instantiation.
    Clients must implement update() method.
    Subject will pass dictionary of values.
    This is enhanced --
    when registerObserver or removeObserver is called,
    you get return values (which you can ignore if you do not need).
    """
    #
    def __init__ ( self, uNewSubscribers = None ):
        #
        from Iter.Test     import isIterable
        #
        self.lSubscribers = []
        #
        if isIterable( uNewSubscribers ):
            #
            self.lSubscribers.extend( list( uNewSubscribers ) )
            #
        elif uNewSubscribers:
            #
            self.lSubscribers.append( uNewSubscribers )
            #
        #
    def registerObserver( self, oClient ):
        #
        iAppended       = 0
        #
        if oClient not in self.lSubscribers:
            #
            self.lSubscribers.append( oClient )
            #
            iAppended   = 1
            #
        #
        return iAppended, len( self.lSubscribers )
        #
    def removeObserver( self, oClient ):
        #
        iRemoved        = 0
        #
        if oClient in self.lSubscribers:
            #
            self.lSubscribers.remove( oClient )
            #
            iRemoved    = 1
        #
        iSubscribers    = len( self.lSubscribers )
        #
        return iRemoved, iSubscribers
        #
    def notifyObservers( self, dState = None ):
        #
        from Utils.Both2n3 import print3
        #
        for oClient in self.lSubscribers:
            #
            try:
                oClient.update( dState )
            #
            except ( StopIteration, GeneratorExit, KeyboardInterrupt, SystemExit ):
                #
                raise
                #
            except Exception: # StandardError
                #
                print3( 'got exception on running update(): %s' % str( oClient ) )
            #
        #
    #




if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    class dummyObserver( object ):
        #
        def __init__( self ):
            self.dInfo = None
        def update( self, dInfo ):
            self.dInfo = dInfo
    #
    oObserver1 = dummyObserver()
    oObserver2 = dummyObserver()
    oObserver3 = dummyObserver()
    #
    oServer    = ObserverClass()
    #
    oServer.registerObserver( oObserver1 )
    oServer.registerObserver( oObserver2 )
    oServer.registerObserver( oObserver3 )
    #
    dNewState = dict( foo = 3, bar = 88 )
    #
    oServer.notifyObservers( dNewState )
    #
    if oObserver3.dInfo[ 'bar' ] != 88:
        #
        lProblems.append( 'ObserverClass()' )
        #

    #
    sayTestResult( lProblems )