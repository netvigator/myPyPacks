#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# django models file
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
# Copyright 2017 Rick Graves
#
'''
note there is no settings.py (django default)

either:
export DJANGO_SETTINGS_MODULE="auctionshoppingbot.settings.dev"
or
python manage.py syncdb --settings=auctionshoppingbot.settings.dev
'''


from django.db import models

# depends on:
# via apt-get install
# python-django-countries
# via pip install
# py-moneyed django-money

import moneyed

from django_countries.fields    import CountryField
from djmoney.models.fields      import MoneyField
from django.db.models           import fields
from django.utils.six           import with_metaclass
from django.db                  import models

# Django v 1.8 will support directly
#class CaseInsensitiveTextField(fields.TextField):
    #def db_type(self, connection):
        #return "citext"

# Django v 1.8 will support directly
class EmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super(EmailField, self).get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value

class LowerCharField(with_metaclass(models.SubfieldBase, models.CharField)):
    def __init__(self, *args, **kwargs):
        self.is_lowercase = kwargs.pop('lowercase', False)
        super(LowerCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super(LowerCharField, self).get_prep_value(value)
        if self.is_lowercase:
            value = value.lower()
        return value

class IntegerRangeField(models.PositiveSmallIntegerField):
    def __init__(self,
            verbose_name=None, name=None, min_value=None, max_value=None,
            **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.PositiveSmallIntegerField.__init__(
            self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class User(models.Model):
    cnamegiven      = models.CharField(
                        'given/first name', max_length = 48, db_index = True)
    cnamefamily     = models.CharField(
                        'family/last name', max_length = 48, db_index = True)
    cemail          = EmailField(
                        'email address',    max_length=248, unique=True)
    cusername       = LowerCharField(
                        'unique user name', max_length = 48, lowercase=True,
                                            null=False, unique=True )
    cpasswordhash   = models.TextField( 'password hash' )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'users'
        db_table            = verbose_name_plural
#
class Brand(models.Model):
    cbrandname      = models.CharField(
                        'brand name', max_length = 48, db_index = True)
    bwanted         = models.BooleanField(
                        'want anything from this brand?', default = True )
    ballofinterest  = models.BooleanField(
                        'want everything from this brand?', default = True )
    istars          = IntegerRangeField(
                        'desireability, five star brand is most desireable',
                        min_value = 0, max_value = 5 )
    ccomment        = models.TextField( 'comments', null = True )
    cnationality    = CountryField( null = True )
    cexcludeif      = models.TextField(
                        'exclude item when this text is found' )
    ilegacykey      = models.PositiveIntegerField('legacy key', unique=True )
    tlegacycreate   = models.DateTimeField( 'legacy row created on' )
    tlegacymodify   = models.DateTimeField( 'legacy row updated on' )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'brands'
        db_table            = verbose_name_plural
#
class Type(models.Model):
    ctypedescribe   = models.CharField(
                        'type description', max_length = 48, db_index = True)
    ctypekeywords   = models.CharField( 'type key words', max_length = 88 )
    bkeywordrequired= models.BooleanField(
                        'key word required?', default = True )
    istars          = IntegerRangeField(
                        'desireability, five star type is most desireable',
                            min_value = 0, max_value = 5 )
    ballofinterest  = models.BooleanField(
                        'want everything of this type?', default = True )
    bwantpair       = models.BooleanField('only want pairs?', default = False)
    baccessory      = models.BooleanField('accessory?', default = False)
    bcomponent      = models.BooleanField('component?', default = False)
    cfamily         = models.ForeignKey( 'self', null = True )
    ccomment        = models.TextField( 'comments', null = True )
    cnationality    = CountryField( null = True )
    ilegacykey      = models.PositiveIntegerField( 'legacy key', unique=True )
    tlegacycreate   = models.DateTimeField( 'legacy row created on' )
    tlegacymodify   = models.DateTimeField( 'legacy row updated on' )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'types'
        db_table            = verbose_name_plural
#

class Model(models.Model):
    cmodelnumber    = models.CharField(
                        'model number or name', max_length = 48, db_index = True)
    cmodelkeywords  = models.CharField( 'model key words', max_length = 88 )
    bkeywordrequired= models.BooleanField(
                        'key word required?', default = True )
    bsplitdigitsok  = models.BooleanField(
                        'split digits OK?', default = False )
    istars          = IntegerRangeField(
                        'desireability, five star model is most desireable',
                                                min_value = 0, max_value = 5 )
    bgenericmodel   = models.BooleanField('generic model?', default = True )
    bsubmodelsok    = models.BooleanField(
                        'want to get sub models?', default = True )
    bmusthavebrand  = models.BooleanField(
                        'must have brand key words?', default = False)
    bwanted         = models.BooleanField('want this model?', default = True )
    bgetpictures    = models.BooleanField(
                        'want to download pics?', default = True )
    bgetdescription = models.BooleanField(
                        'want the description text?', default = True )
    ibrand          = models.ForeignKey( Brand )
    itype           = models.ForeignKey( Type )
    ilegacykey      = models.PositiveIntegerField('legacy key', unique=True )
    tlegacycreate   = models.DateTimeField( 'legacy row created on' )
    tlegacymodify   = models.DateTimeField( 'legacy row updated on' )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'models'
        db_table            = verbose_name_plural
#

class BrandType(models.Model):
    ibrand          = models.ForeignKey( Brand )
    itype           = models.ForeignKey( Type )
    bwanted         = models.BooleanField('want this combination?', default = True )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    
    class Meta:
        verbose_name_plural = 'brandtypes'
        db_table            = verbose_name_plural
#

class ModelPic(models.Model):
    imodel          = models.ForeignKey( Model )
    cfilespec       = models.FilePathField( 'file path and name for model picture' )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'modelpics'
        db_table            = verbose_name_plural
#

class CharacterTranslation(models.Model):
    ctranslatefrom  = models.TextField( 'if this text is found' )
    ctranslateto    = models.TextField( 'change to this' )
    iwhendigit      = IntegerRangeField(
                        'not sure what this was for',
                        min_value = 1, max_value = 4 )
    bignoreembedded = models.BooleanField('ignore embdeded?', default = True )
    bignoredouble   = models.BooleanField('ignore double?',   default = True )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'charactertranslations'
        db_table            = verbose_name_plural
#


class ComboStar(models.Model):
    istars          = IntegerRangeField(
                        '0 to 100, 100 is most desireable',
                        min_value = 0, max_value = 100 )
    imodel          = models.ForeignKey( Model )
    ibrand          = models.ForeignKey( Brand )
    itype           = models.ForeignKey( Type )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'combostars'
        db_table            = verbose_name_plural
#


class Condition(models.Model):
    ccondition      = models.CharField(
                        'condition', max_length = 18, db_index = True)
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'conditions'
        db_table            = verbose_name_plural
#


class FetchPriorty(models.Model):
    iminstars       = IntegerRangeField(
                        '0 to 100, 100 is most desireable',
                        min_value = 0, max_value = 100 )
    icompsyearly    = IntegerRangeField(
                        'target number of comparables wanted yearly',
                        min_value = 0, max_value = 100 )
    ilotsofbids     = IntegerRangeField(
                        'consider fetch if more bids than this min',
                        min_value = 0, max_value = 100 )
    mMinPrice       = MoneyField( 'consider fetch if price exceeds this min',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD')
    mBigPrice       = MoneyField( 'fetch if price exceeds this',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD')
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'fetchpriorities'
        db_table            = verbose_name_plural
#

class Exclude(models.Model):
    cexcludeif      = models.CharField(
                        'exclude item if description includes this text',
                        max_length = 48, db_index = True)
    ccomment        = models.TextField( 'comments', null = True )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'exclusions'
        db_table            = verbose_name_plural
#


class Item(models.Model):
    iitemnumb       = models.BigIntegerField(
                        'ebay item number', primary_key = True )
    ctitle          = models.CharField(
                        'auction headline', max_length = 48, db_index = True )
    mlastbid        = MoneyField( 'winning bid',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    clastbid        = models.CharField(
                        'winning bid (text)', max_length = 18,
                        db_index = False, null = True )
    tgotlastbid     = models.DateTimeField(
                        'retrieved last bid date/time', null = True )
    mbuyitnow       = MoneyField( 'buy it now price',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    cbuyitnow       = models.CharField(
                        'buy it now price (text)', max_length = 18,
                        db_index = False, null = True )
    binvaliditem    = models.BooleanField( 'invalid item?', default = False )
    inumberofbids   = models.PositiveSmallIntegerField( 'number of bids' )
    tauctionend     = models.DateTimeField( 'auction ending date/time' )
    tauctionbeg     = models.DateTimeField( 'auction beginning date/time' )
    iquantity       = models.PositiveSmallIntegerField( 'quantity' )
    tcannotfind     = models.DateTimeField( 'cannot retrieve outcome date/time' )
    bitemhit        = models.BooleanField( 'item of interest?', default = False )
    tlook4hits      = models.DateTimeField(
                        'assessed interest date/time', null = True )
    tlook4images    = models.DateTimeField(
                        'tried to retrieve images date/time', null = True )
    bgotimages      = models.NullBooleanField( 'got images?' )
    igetbecause     = models.ForeignKey( FetchPriorty )
    tlastcheck      = models.DateTimeField( 'got status most recently date/time' )
    bkeeper         = models.NullBooleanField( 'keep this?' )
    bnotwanted      = models.BooleanField( 'not wanted', default = False )
    bgetdetails     = models.BooleanField( 'get details', default = False )
    basktoget       = models.BooleanField( 'ask whether to get details', default = False )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'items'
        db_table            = verbose_name_plural
#

class ItemDetail(models.Model):
    iitem           = models.OneToOneField( Item )
    breservemet     = models.NullBooleanField( 'reserve met?' )
    bbuyitnow       = models.BooleanField( 'buy it now?', default = False )
    brelisted       = models.BooleanField( 'relisted?', default = False )
    clocation       = models.CharField( 'location', max_length = 48 )
    cregion         = models.CharField( 'region', max_length = 48 )
    cseller         = models.CharField( 'seller', max_length = 48 )
    isellerfeedback = models.PositiveIntegerField( 'seller feedback' )
    cbuyer          = models.CharField( 'buyer', max_length = 48, null = True )
    ibuyerfeedback  = models.PositiveIntegerField(
                        'buyer feedback', null = True )
    cshipping       = models.CharField( 'shipping info', max_length = 188 )
    cdescription    = models.TextField( 'description' )
    iimages         = models.PositiveSmallIntegerField( '# of pictures' )
    irelistitemnumb = models.BigIntegerField( 'relist item number' )
    
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'itemdetails'
        db_table            = verbose_name_plural
#

class ItemHit(models.Model):
    iitem           = models.OneToOneField( Item )
    dhitstars       = models.DecimalField(
                        'hit stars', max_digits = 3, decimal_places = 2 )
    bmaxhitstars    = models.BooleanField( 'max hit stars', default = False )
    imodel          = models.ForeignKey( Model )
    ibrand          = models.ForeignKey( Brand )
    itype           = models.ForeignKey( Type )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    
    class Meta:
        verbose_name_plural = 'itemhits'
        db_table            = verbose_name_plural
#

class ItemImage(models.Model):
    iitem           = models.ForeignKey( Item )
    isequence       = models.PositiveSmallIntegerField( 'sequence', db_index=True )
    cfilename       = models.CharField( 'local file name', max_length = 28 )
    coriginalurl    = models.TextField( 'original URL' )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    
    class Meta:
        verbose_name_plural = 'itemimages'
        db_table            = verbose_name_plural
#

class ModelExclude(models.Model):
    imodel          = models.ForeignKey( Model )
    cexcludeif      = models.CharField( 'exclude if found', max_length = 48 )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    class Meta:
        verbose_name_plural = 'modelexclusions'
        db_table            = verbose_name_plural
#


class Search(models.Model):
    cdescribe       = models.CharField( 'description', max_length = 28 )
    cpriority       = models.CharField( 'priority', max_length = 2, null=True)
    cstartpage      = models.TextField( 'start page URL' )
    csearchpic      = models.CharField(
                        'picture for this search', max_length = 28, null = True )
    ccomment        = models.TextField( 'comments', null=True)
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )

    class Meta:
        verbose_name_plural = 'searches'
        db_table            = verbose_name_plural
#


class SearchLog(models.Model):
    isearch         = models.ForeignKey( Search )
    tlocalstart     = models.DateTimeField( 'search start time' )
    tlocalfinish    = models.DateTimeField( 'search finish time' )
    isearchpages    = models.PositiveSmallIntegerField( 'pages searched' )
    ihits           = models.PositiveSmallIntegerField( 'items found' )
    
    class Meta:
        verbose_name_plural = 'searchlog'
        db_table            = verbose_name_plural
#


"""
skipping

easily handled on the fly
LOOK4BRANDS.CSV
LOOK4MODELS.CSV
LOOK4TYPES.CSV

there must be an API
MONEYCODES.CSV
MONEYEXCHANGE.CSV

not sure how ebay api will handle pics, may not be necessary
PICHOSTS.CSV
PICOMITS.CSV
PICSUBST.CSV

SKIPFRAGWHEN.CSV

SUBSTYPE.CSV

"""



if __name__ == "__main__":
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    # cannot work!
    #
    sayTestResult( lProblems )
    