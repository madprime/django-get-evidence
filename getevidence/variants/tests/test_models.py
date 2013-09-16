"""
Tests models.py in variants app.
"""

from django.conf import settings
from django.test import TestCase
from ..models import DbSNP, Gene, Variant, VariantReview
from ..management.commands.add_external_gene_data import add_external_gene_data
from ..management.commands.sample_data import create_HBB_E7V

class VariantsModelsTest(TestCase):
    """Tests the functions and models in models.py."""

    def setUp(self):
        add_external_gene_data(settings.SITE_ROOT + '/../external_data/getevidence_external_gene_data_mini.csv')
        create_HBB_E7V()

    def test_parse_variant_with_HBB_E7V(self):
        """Tests classmethod parse_variant with 'HBB-E7V'."""
        output = Variant.parse_variant('HBB-E7V')
        self.assertIn('gene_name', output)
        self.assertIn('aa_ref', output)
        self.assertIn('aa_pos', output)
        self.assertIn('aa_var', output)
        self.assertEqual(output['gene_name'], 'HBB')
        self.assertEqual(output['aa_ref'], 'E')
        self.assertEqual(output['aa_pos'], 7)
        self.assertEqual(output['aa_var'], 'V')

    def test_variant_lookup_with_HBB_E7V(self):
        """Tests classmethod variant_lookup with 'HBB-E7V'."""
        variant = Variant.variant_lookup('HBB-E7V')
        self.assertEqual(variant.gene.hgnc_symbol, 'HBB')
        self.assertEqual(variant.aa_reference, 'E')
        self.assertEqual(variant.aa_position, 7)
        self.assertEqual(variant.aa_variant, 'V')

    def test_Variant_create_with_JAK2_V617F(self):
        """Tests Variant creation."""
        Variant.create(gene_name='JAK2', aa_ref='V', aa_pos=617, aa_var='F')

    def test_Variant_remove_with_HBB_E7V(self):
        """Tests Variant removal."""
        variant = Variant.variant_lookup('HBB-E7V')
        Variant.remove(variant=variant)

    def test_DbSNP_create_with_rs77375493(self):
        """Tests DbSNP creation."""
        DbSNP.objects.create(rsid='rs77375493')

    def test_DbSNP_delete_with_rs334(self):
        """Tests DbSNP deletion."""
        DbSNP.objects.get(rsid='rs334').delete()

    def test_Variant_dbSNP_add_and_remove(self):
        """Tests adding dbSNP (ManyToMany) to Variant."""
        s = DbSNP.objects.get(rsid='rs334')
        v = Variant.objects.get(gene__hgnc_symbol='HBB',
                                aa_reference='E',
                                aa_position=7, aa_variant='V')
        v.dbsnps.add(s)
        v.dbsnps.remove(s)
