"""
Tests sample_data.py in variants app.
"""

from django.test import TestCase
from ..sample_data import create_HBB_E7V, create_JAK2_V617F, create_sample_data

class VariantsSampleDataTest(TestCase):
    """Tests sample data creation script."""

    def test_create_HBB_E7V(self):
        create_HBB_E7V()

    def test_JAK2_V617F(self):
        create_JAK2_V617F()

    def test_create_sample_data(self):
        create_sample_data()
