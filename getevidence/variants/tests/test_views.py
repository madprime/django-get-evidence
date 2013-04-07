"""
Tests views.py in variants app.
"""

from django.test import TestCase
from django.test.client import Client
from ..sample_data import create_sample_data
from ..models import Variant, VariantReview

class VariantsViewsTest(TestCase):
    """Tests the functions and models in views.py."""

    def setUp(self):
        """Set up a client and sample data using ..sample_data"""
        self.cl = Client()
        create_sample_data()

    def test_index(self):
        """Test variants index."""
        response = self.cl.get('/variant/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['variant_list']), 2)

    def test_submit_edit(self):
        """Test a sample edit submission."""
        response = self.cl.post('/variant/HBB-E7V/submit_edit', 
                                {'variant_review_long':
                                     "Most common cause of sickle cell anemia."})

        # Should perform a redirect.
        self.assertEqual(response.status_code, 302)

        # Check that edit was successful.
        v = Variant.objects.get(gene__hgnc_name='HBB', aa_reference='E',
                                aa_position=7, aa_variant='V')
        self.assertEqual(VariantReview.objects.get(variant=v).review_long,
                         "Most common cause of sickle cell anemia.")

    def test_submit_new(self):
        """Test submitting a new variant."""
        response = self.cl.post('/variant/submit_new',
                                {'gene': 'HFE',
                                 'aa_reference': 'C',
                                 'aa_position': '282',
                                 'aa_variant': 'Y'})
        # Should perform a redirect.
        self.assertEqual(response.status_code, 302)

        # Check that edit was successful.
        v = Variant.objects.get(gene__hgnc_name='HFE', aa_reference='C',
                                aa_position=282, aa_variant='Y')
        self.assertTrue(v)
