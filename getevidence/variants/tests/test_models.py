"""
Tests models.py in variants app.
"""

from django.test import TestCase
from ..models import parse_variant, variant_lookup, DbSNP, Gene, Variant


class VariantsModelsTest(TestCase):
    """Tests the functions and models in models.py."""

    def setUp(self):
        """Adds or creates test data in database.

        gene: HBB
        variant: HBB-E7V
        """
        g, unused = Gene.objects.get_or_create(hgnc_name='HBB')
        s, unused = DbSNP.objects.get_or_create(rsid='rs334')
        try:
            v = Variant.objects.get(gene__id=g.id,
                                    aa_reference='E',
                                    aa_position=7,
                                    aa_variant='V',)
        except Variant.DoesNotExist:
            v = Variant(gene=g, aa_reference='E', aa_position=7, aa_variant='V')
            v.save()

    def test_parse_variant_with_HBB_E7V(self):
        """Tests function parse_variant with 'HBB-E7V'."""
        output = parse_variant('HBB-E7V')
        self.assertIn('gene_name', output)
        self.assertIn('aa_ref', output)
        self.assertIn('aa_pos', output)
        self.assertIn('aa_var', output)
        self.assertEqual(output['gene_name'], 'HBB')
        self.assertEqual(output['aa_ref'], 'E')
        self.assertEqual(output['aa_pos'], 7)
        self.assertEqual(output['aa_var'], 'V')

    def test_variant_lookup_with_HBB_E7V(self):
        """Tests function variant_lookup with 'HBB-E7V'."""
        variant = variant_lookup('HBB-E7V')
        self.assertEqual(variant.gene.hgnc_name, 'HBB')
        self.assertEqual(variant.aa_reference, 'E')
        self.assertEqual(variant.aa_position, 7)
        self.assertEqual(variant.aa_variant, 'V')

    def test_DbSNP_create_with_rs77375493(self):
        """Tests DbSNP creation."""
        DbSNP.objects.create(rsid='rs77375493')

    def test_DbSNP_delete_with_rs334(self):
        """Tests DbSNP deletion."""
        DbSNP.objects.get(rsid='rs334').delete()

    def test_Variant_create_with_JAK2_V617F(self):
        """Tests Variant creation."""
        g, unused = Gene.objects.get_or_create(hgnc_name='JAK2')
        Variant.objects.filter(gene__id=g.id, aa_reference='V',
                               aa_position=617, aa_variant='F').delete()
        Variant.objects.create(gene=g, aa_reference='V',
                               aa_position=617, aa_variant='F')

    def test_Variant_delete_with_HBB_E7V(self):
        """Tests Variant deletion."""
        Variant.objects.get(gene__hgnc_name='HBB', aa_reference='E',
                            aa_position=7, aa_variant='V').delete()
