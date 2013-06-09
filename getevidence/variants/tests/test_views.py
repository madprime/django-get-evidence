"""
Tests views.py in variants app.
"""

import re
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

    def test_edit(self):
        """Test a sample edit submission."""
        response = self.cl.post('/variant/HBB-E7V/edit',
                                {'review_summary': "Sickle cell anemia.",
                                 'review_long': "Acts in recessive manner.",
                                 'impact': 'pat',
                                 'inheritance': 'rec',
                                 'evidence_computational': '1',
                                 'evidence_functional': '3',
                                 'evidence_casecontrol': '5',
                                 'evidence_familial': '5',
                                 'clinical_severity': '4',
                                 'clinical_treatability': '3',
                                 'clinical_penetrance': '5'})

        # Should perform a redirect.
        self.assertEqual(response.status_code, 302)

        # Check that edit was successful.
        v = Variant.objects.get(gene__hgnc_name='HBB', aa_reference='E',
                                aa_position=7, aa_variant='V')
        self.assertEqual(VariantReview.objects.get(variant=v).review_long,
                         "Acts in recessive manner.")

        # Test poorly formatted variant.
        response = self.cl.post('/variant/E7V-HBB/edit',
                                {'variant_review_long': "Filler."})
        self.assertTrue(re.search("Badly formatted variant", response.content))

        # Test nonexistent variant.
        response = self.cl.post('/variant/HBB-E27V/edit',
                                {'variant_review_long': "Filler."})
        self.assertTrue(re.search("No variant found", response.content))

    def test_new(self):
        """Test new variant entry page."""
        # Test creating empty page.
        response = self.cl.get('/variant/new')
        self.assertEqual(response.status_code, 200)

        # Test creating new variant.
        response = self.cl.post('/variant/new',
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

        # Test poorly formatted variant.
        response = self.cl.post('/variant/new',
                                {'gene': 'HFE',
                                 'aa_reference': 'C',
                                 'aa_position': 'Y',
                                 'aa_variant': '282'})
        self.assertTrue(re.search("poorly formatted", response.content))

        # Test already existing variant.
        response = self.cl.post('/variant/new',
                                {'gene': 'HBB',
                                 'aa_reference': 'E',
                                 'aa_position': '7',
                                 'aa_variant': 'V'})
        self.assertTrue(re.search("already exists", response.content))

    def test_detail(self):
        """Test variant detail page."""
        response = self.cl.get('/variant/HBB-E7V')
        self.assertEqual(response.status_code, 200)
        response_var = response.context['variant']
        response_varrev = response.context['variant_review']
        self.assertEqual(response_var.gene.hgnc_name, 'HBB')
        self.assertEqual(response_var.aa_reference, 'E')
        self.assertEqual(response_var.aa_position, 7)
        self.assertEqual(response_var.aa_variant, 'V')
        self.assertEqual(response_varrev.review_summary,
                         "Causes sickle cell anemia.")
        # Test poorly formatted variant.
        response = self.cl.get('/variant/E7V-HBB')
        self.assertTrue(re.search("Badly formatted", response.content))
        # Test not existing variant.
        response = self.cl.get('/variant/HBB-E27V')
        self.assertTrue(re.search("No variant found", response.content))
