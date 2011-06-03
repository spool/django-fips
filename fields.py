from django.contrib.localflavor.us.models import USStateField
from django.contrib.localflavor.us import us_states
from django.db import models
from . import *

class USStateFipsCode:
    """A US state class which includes FIPS characters and numbers."""

    def __init__(self, code):
        if isinstance(code, str) or isinstance(code, unicode):
            if code in US_STATE_CHAR2FIPS:
                self.code = code
            elif code in us_states.STATES_NORMALIZED:
                self.code = us_states.STATES_NORMALIZED[code]
            else:
                try:
                    code = str(int(code))
                    self.code = US_STATE_FIPS_SHORT[code]
                except:
                    raise InvalidFIPS(code)
        if isinstance(code, int) or isinstance(code, float):
            try:
                code = str(int(code))
                self.code = US_STATE_FIPS_SHORT[code]
            except:
                raise InvalidFIPS(code)
        self.number = int(US_STATE_CHAR2FIPS[self.code])
        self.name = US_STATE_FIPS[str(self.number)]

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "USStateField('%s')" % self.code

class InvalidFIPS(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '%s is an invalid FIPS code' % repr(self.value)


class USStateFipsField(USStateField):

    #__metaclass__ = models.SubfieldBase # Ensures to_python is always called.

    def to_python(self, value):
        if isinstance(value, USStateFipsCode):
            return value



