from django.contrib.localflavor.us.models import USStateField
from django.db import models
from . import *

class USStateFipsCode:
    """A US state class which includes FIPS characters and numbers."""

    def __init__(self, code):
        try:
            self.number = int(US_STATE_CHAR2FIPS[code])
        except KeyError:
            raise InvalidFIPS(code)
        self.code = code
        self.name = US_STATE_FIPS[str(self.number)]

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "USStateField('%s')" % self.code


class USStateFipsField(USStateField):

    __metaclass__ = models.SubfieldBase

    @property
    def fips(self):
        return int(self)

class InvalidFIPS(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '%s is an invalid FIPS code' % repr(self.value)
