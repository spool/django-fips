from django.utils import unittest # Makes use of unittest2 https://docs.djangoproject.com/en/dev/topics/testing/
from django.db import models
from fips import fields

class FIPSTestModel(models.Model):
    fips = fields.USStateFipsField()
    fips_blank = fields.USStateFipsField(blank=True)
    fips_null = fields.USStateFipsField(null=True)
    fips_blank_null = fields.USStateFipsField(blank=True, null=True)

class FIPSTest(unittest.TestCase):

    def equals_alaska(self, ak):
        self.assertEqual(ak.name, 'Alaska')
        self.assertEqual(ak.number, 2)
        self.assertEqual(ak.code, 'AK')

class USStateFipsFieldTest(FIPSTest):

    def instance_equals_alaska(self, instance):
        self.equals_alaska(instance.fips)
        self.equals_alaska(instance.fips_blank)
        self.equals_alaska(instance.fips_blank_null)
        self.equals_alaska(instance.fips_null)

    def testSave(self):
        a = FIPSTestModel(fips=2, fips_blank=2.0, fips_null='ak', fips_blank_null='AK')
        a.save()
        self.instance_equals_alaska(a)
        b = FIPSTestModel.objects.get(id=a.id)
        self.instance_equals_alaska(b)

    def testNull(self):
        a = FIPSTestModel(fips=2, fips_blank=2.0)
        a.save()
        self.equals_alaska(a.fips)
        self.equals_alaska(a.fips_blank)
        self.equals_alaska(FIPSTestModel.objects.get(id=a.id).fips)
        self.equals_alaska(FIPSTestModel.objects.get(id=a.id).fips_blank)

class QueryTest(FIPSTest):

    def setUp(self):
        self.a = FIPSTestModel.objects.create(fips=2, fips_blank=2.0, fips_null='ak', fips_blank_null='AK')
        self.b = FIPSTestModel.objects.create(fips=56, fips_blank=56.0, fips_null='wy', fips_blank_null='WY')

    def testFlatValuesList(self):
        print type(u'AK')
        self.assertEqual(FIPSTestModel.objects.values_list('fips_blank', flat=True), [u'AK', u'WY'])

class USStateFipsClassTest(FIPSTest):

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
