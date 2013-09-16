"""
Tests sample_data.py in variants app.
"""

from django.conf import settings
from django.test import TestCase
from ..management.commands.add_external_gene_data import add_external_gene_data
from ..management.commands.sample_data import create_HBB_E7V, create_JAK2_V617F, create_sample_data

class VariantsSampleDataTest(TestCase):
    """Tests sample data creation script."""

    def setUp(self):
        add_external_gene_data(settings.SITE_ROOT + '/../external_data/getevidence_external_gene_data_mini.csv')

    def test_create_HBB_E7V(self):
        create_HBB_E7V()

    def test_JAK2_V617F(self):
        create_JAK2_V617F()

    def test_create_sample_data(self):
        create_sample_data()
