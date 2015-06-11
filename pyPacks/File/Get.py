#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# File functions get
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
# Copyright 2004-2013 Rick Graves
#

#from os.path import join, isfile, getmtime, split, splitext, exists, basename, isdir
#from os      import stat, environ, getcwd, listdir, rename, remove

# from os.path import exists, join, isfile, isdir


from File.Test      import isFileThere
from File.Spec      import getFullSpec, getFullSpecDefaultOrPassed

class FileNotThereError( Exception ): pass

class LineParserObject( object ):
    #
    def __init__( self, sConfFile = 'LineParserTest.conf' ):
        #
        from Utils.Config     import getConfDict
        #
        dMain       = { 'infile'  : '/tmp/LineParserTestInput.txt',
                        'rowhead' : 'new row',
                        'colhead1': 'next row',
                        'outfile' : '/tmp/LineParserTestOutput.txt' }
        dDefaults   = { 'main' : dMain }
        bNoConfigOK = ( sConfFile == 'LineParserTest.conf' )
        #
        dFile2Parse = getConfDict(
                        sConfFile,
                        dDefaults = dDefaults,
                        bNoConfigOK = bNoConfigOK )
        #
        self.dFile2Parse = dFile2Parse
        #
        if self.dFile2Parse == dDefaults:
            #
            # print3( dFile2Parse )
            #
            self._makeTestFile()
        #
        self.oInFile = open( self.dFile2Parse['main']['infile'] )

    def _makeTestFile( self ):
        #
        from File.Write import QuickDump
        #
        sTestContent = ( '\nnew row\nspam\n\nnext row\ntoast\n\n\n'
                         'new row\neggs\n\nnext row\nbeans\n\n' )
        #
        QuickDump( sTestContent, self.dFile2Parse['main']['infile'], bSayBytes = False )
        #

    def _isNewRow( self, s ):
        #
        '''can be subclassed
        '''
        return s == self.dFile2Parse['main']['rowhead']

    def ReadWrite( self ):
        #
        pass


def getFileObject( *sFileSpec, **kwargs ):
    #
    sMode = 'r'
    #
    if 'sMode' in kwargs: sMode = kwargs[ 'sMode' ]
    #
    sFileSpec = getFullSpec( *sFileSpec )
    #
    f       = None
    #
    if not isFileThere( sFileSpec ): raise FileNotThereError( sFileSpec )
    #
    try:
        #
        f   = open( sFileSpec, sMode )
        #
    except:
        #
        pass
        #
    #
    #
    return f



def getFileContent( *sFileSpec, **kwargs ):
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    sMode = 'r'
    #
    if 'sMode' in kwargs: sMode = kwargs[ 'sMode' ]
    #
    f = getFileObject( sFileSpec, sMode = sMode )
    #
    if f is None:
        #
        sContents = ''
        #
    else:
        #
        try:
            #
            sContents = f.read()
            #
        except UnicodeDecodeError:
            #
            sMode += 'b'
            #
            f = getFileObject( sFileSpec, sMode = sMode )
            #
            sContents = f.read()
            #
        #
        f.close()
        #
    #
    return sContents



def getContent( *sFileSpec ):
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec )
    #
    return getFileContent( sFileSpec )





def getRandomFileName( sDir = None, bCreate = False ):
    #
    from os             import environ
    from os.path        import isfile, join, isdir
    #
    from Numb.Get       import getRandomDigits
    #
    if sDir is None:
        #
        sDir            = environ.get( 'HOME', '/tmp' )
        #
    #
    if not isdir( sDir ): sDir = '' # put in current directory
    #
    while True:
        #
        sFile           = '%s.tmp' % getRandomDigits( 8 )
        #
        sPathFile       = join( sDir, sFile )
        #
        if not isfile( sPathFile ): break
        #
    #
    if bCreate:
        #
        oFile = open( sPathFile, 'w' )
        #
        oFile.close()
        #
    #
    return sPathFile



def getListFromFileLines( *sFileSpec, **kwargs ):
    #
    bStipLines = kwargs.get( 'bStipLines', True )
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec )
    #
    sText       = getFileContent( sFileSpec )
    #
    if sText.count( '\n' ) == sText.count( '\r\n' ):
        #
        lLines  = sText.split( '\r\n' )
        #
    else:
        #
        lLines  = sText.split( '\n' )
        #
    #
    if bStipLines:
        #
        return  [ sLine.strip() for sLine in lLines ]
        #
    else:
        #
        return  lLines


getListOffFileLines = getListFromFileLines



def getTempFile( suffix = None, dir = None ):
    #
    """
    Creates a unique temp file and returns the full path spec.
    """
    #
    from tempfile   import mkstemp
    from os         import close
    #
    # from String.Get import getBackslashEscaped
    #
    kwargs = {}
    #
    if suffix is not None:
        #
        kwargs[ 'suffix' ] = suffix
        #
    if dir is not None:
        #
        kwargs[ 'dir'    ] = dir
        #
    #
    fhTemp, sTempFile = mkstemp( **kwargs )
    #
    close( fhTemp )
    #
    # return getBackslashEscaped( sTempFile )
    #
    return sTempFile






def getObjFromFileContent( *sFileSpec ):
    #
    '''
    Goes with PutReprInTemp in File.Write
    '''
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec )
    #
    sContent    = getFileContent( sFileSpec )
    #
    return eval( sContent )




def getObjFromFileIter( *sFileSpec ):
    #
    '''
    Goes with PutReprInTemp in File.Write
    '''
    #
    sFileSpec = getFullSpecDefaultOrPassed( *sFileSpec )
    #
    oFile = getFileObject( sFileSpec )
    #
    return eval( oFile.read() )




def getFileNameNoSpaces( s ):
    #
    while '  ' in s:
        #
        s = s.replace( '  ', ' ' )
        #
    #
    return s.replace( ' ', '_' )




if __name__ == "__main__":
    #
    lProblems = []
    #
    from Collect.Query  import get1stThatMeets
    from File.Write     import PutReprInTemp
    from Time.ReadWrite import putTimeInFile
    from Time.Test      import isISOdatetime
    from Utils.Result   import sayTestResult
    #
    #
    fThisFile = getFileObject( 'Get.py' )
    #
    def isStartsWithThis( s ): return s.startswith( 'def getFileObject' )
    #
    if get1stThatMeets( fThisFile, isStartsWithThis ) is None:
        #
        lProblems.append( 'getFileObject()' )
        #
    #
    fThisFile.close()
    #
    sContent = getContent( 'Get.py' )
    #
    lLines  = sContent.split( '\n' )
    #
    if get1stThatMeets( lLines, isStartsWithThis ) is None:
        #
        lProblems.append( 'getContent() / getFileContent() file spec passed' )
        #
    #
    putTimeInFile( getFullSpecDefaultOrPassed() )
    #
    sContent = getContent()
    #
    if not isISOdatetime( sContent ):
        #
        lProblems.append( 'getContent() / getFileContent() no file spec argument' )
        #
    #
    if len( getRandomFileName() ) < 10:
        #
        lProblems.append( 'getRandomFileName()' )
        #
    #
    lLines = getListFromFileLines( 'Get.py' )
    #
    if get1stThatMeets( lLines, isStartsWithThis ) is None:
        #
        lProblems.append( 'getListFromFileLines()' )
        #
    #
    if len( getTempFile() ) < 10:
        #
        lProblems.append( 'getTempFile()' )
        #
    #
    d = {'Fischbach': ['Corcoran', 'Ching Wu']}
    #
    PutReprInTemp( d )
    #
    if d != getObjFromFileContent():
        #
        lProblems.append( 'getObjFromFileContent()' )
        #
    #
    if d != getObjFromFileIter():
        #
        lProblems.append( 'getObjFromFileIter()' )
        #
    #



    if getFileNameNoSpaces( 'Jay  Inslee (D)' ) != 'Jay_Inslee_(D)':
        #
        lProblems.append( 'getFileNameNoSpaces()' )
        #
    #
    LineParserObject()
    #
    sayTestResult( lProblems )