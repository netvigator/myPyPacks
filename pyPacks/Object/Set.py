#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Object functions Set
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



def AttributesFromDict(d, obj=None, objName="self"):
    #
    """No more self.foo = foo, self.bar = bar, etc."""
    #
    from Dict.Get import getItemIter
    #
    if obj is None:
        obj = d.pop(objName)
    for n, v in getItemIter( d ):
        setattr(obj, n, v)

getAttributesFromDict = AttributesFromDict


if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    class SelfTest( object ):
        #
        def __init__( self, **kwargs ):
            #
            kwargs[ 'self' ] = self
            #
            AttributesFromDict( kwargs )
    #
    oTest = SelfTest( foo = 3, bar = 88 )
    #

    if oTest.bar != 88:
        #
        lProblems.append( 'AttributesFromDict()' )
        #


    #
    sayTestResult( lProblems )