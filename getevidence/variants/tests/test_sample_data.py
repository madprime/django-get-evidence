"""
Tests sample_data.py in variants app.
"""

from django.test import TestCase
from ..sample_data import create_sample_data

class VariantsSampleDataTest(TestCase):
    """Tests sample data creation script."""

    def test_create_sample_data(self):
        create_sample_data()
