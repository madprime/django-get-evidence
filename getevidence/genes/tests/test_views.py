"""
Tests views.py in genes app.
"""

from django.test import TestCase
from django.test.client import Client


class GenesViewsTest(TestCase):
    """Tests the functions and models in views.py."""

    def setUp(self):
        self.cl = Client()
