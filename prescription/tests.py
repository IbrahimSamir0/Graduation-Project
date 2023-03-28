from django.test import TestCase
from prescription.models import *

# Create your tests here.

class StandardDrugsTestCase(TestCase):
    def setUp(self):
        StandardDrugs.objects.create(name="TestCase0",
                                     desease="deseaseTestCase",
                                     sideEffects="sideEffectsTEST",
                                     description="descriptionTest",
                                     drugType="drugTypeTest")

    def test_my_model(self):
        obj = StandardDrugs.objects.get(name="TestCase0")
        self.assertEqual(obj.name, "TestCase0")
        self.assertEqual(obj.desease, "deseaseTestCase")
        self.assertEqual(obj.sideEffects, "sideEffectsTEST")
        self.assertEqual(obj.description, "descriptionTest")
        self.assertEqual(obj.drugType, "drugTypeTest")