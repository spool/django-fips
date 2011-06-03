import unittest
from fips import fields

class USStateFipsClassTest(unittest.TestCase):

    def testSimpleAlaska(self):
        ak = fields.USStateFipsCode('AK')
        self.equals_alaska(ak)

    def testNonStandardAlaska(self):
        ak = fields.USStateFipsCode('ak')
        self.equals_alaska(ak)

    def testStringNumberAlaska(self):
        ak = fields.USStateFipsCode('2')
        self.equals_alaska(ak)

    def testStringNumberLeadingZeroAlaska(self):
        ak = fields.USStateFipsCode('02')
        self.equals_alaska(ak)

    def testNumberAlaska(self):
        ak = fields.USStateFipsCode(2)
        self.equals_alaska(ak)
        
    def testFloatAlaska(self):
        ak = fields.USStateFipsCode(2.0000)
        self.equals_alaska(ak)

    def testDecimalAlaska(self):
        ak = fields.USStateFipsCode(2.0001)
        self.equals_alaska(ak)

    def testFipsNumberError(self):
        self.assertRaises(fields.InvalidFIPS, fields.USStateFipsCode, 600)

    def testFipsFloatError(self):
        self.assertRaises(fields.InvalidFIPS, fields.USStateFipsCode, 600.0)

    def testFipsStringError(self):
        self.assertRaises(fields.InvalidFIPS, fields.USStateFipsCode, 'AS')

    def equals_alaska(self, ak):
        self.assertEqual(ak.name, 'Alaska')
        self.assertEqual(ak.number, 2)
        self.assertEqual(ak.code, 'AK')

