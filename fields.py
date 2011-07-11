from django.contrib.localflavor.us import us_states
from django.contrib.localflavor.us.models import USStateField
from django.db import models
from . import US_STATE_CHAR2FIPS, US_STATE_FIPS, US_STATE_FIPS_SHORT

class USStateFipsCode:
    """A US state class which includes FIPS characters and numbers."""

    def __init__(self, code):
        if code:
            self.code = self.force_2char(code)
            self.number = int(US_STATE_CHAR2FIPS[self.code])
            self.name = US_STATE_FIPS[str(self.number)]
        else:
            self.code = None
            self.name = None
            self.number = None

    @staticmethod
    def force_2char(value):
        if value:
            if isinstance(value, str) or isinstance(value, unicode):
                if value in US_STATE_CHAR2FIPS:
                    return value
                elif value in us_states.STATES_NORMALIZED:
                    return us_states.STATES_NORMALIZED[value]
                else:
                    try:
                        value = str(int(value))
                        return US_STATE_FIPS_SHORT[value]
                    except:
                        raise InvalidFIPS(value)
            if isinstance(value, int) or isinstance(value, float):
                try:
                    value = str(int(value))
                    return US_STATE_FIPS_SHORT[value]
                except:
                    raise InvalidFIPS(value)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        try:
            return "<%s: %s>" % (self.__class__.__name__, self.code)
        except AttributeError:
            return None

class InvalidFIPS(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '%s is an invalid FIPS code' % repr(self.value)


class USStateFipsField(USStateField):

    __metaclass__ = models.SubfieldBase # Ensures to_python is always called.

    def to_python(self, value):
        if isinstance(value, USStateFipsCode):
            return value
        else:
            return USStateFipsCode(value)

    def get_prep_value(self, value):
        return value.code

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^fips\.fields\.USStateFipsField"])
except:
    pass

