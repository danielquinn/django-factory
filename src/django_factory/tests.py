"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.db import models
from django_factory.models import Factory

class Product(Factory):

	name = models.CharField(max_length=128)

	def __unicode__(self):
		return self.name



class AlphaProduct(Product):
	alpha = models.CharField(max_length=128)



class BravoProduct(Product):
	bravo = models.CharField(max_length=128)



class CharlieProduct(BravoProduct):
	charlie = models.CharField(max_length=128)



class SimpleTest(TestCase):

	fixtures = ["inheritance.json",]

	def test_inheritance(self):
		self.assertEqual(Product.objects.acquire(pk=1), AlphaProduct.objects.get(pk=1))
		self.assertEqual(Product.objects.acquire(pk=2), BravoProduct.objects.get(pk=2))
		self.assertEqual(Product.objects.acquire(pk=3), CharlieProduct.objects.get(pk=3))
