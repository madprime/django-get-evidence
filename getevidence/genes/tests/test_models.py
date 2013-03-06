"""
Tests models.py in genes app.
"""

from django.test import TestCase
from ..models import Gene

class GenesModelsTest(TestCase):
    """Tests models in models.py"""

    def setUp(self):
        Gene.objects.get_or_create(hgnc_name='HBB',
                                   genetests=True,
                                   genereviews=True)

    def test_Gene_create_with_JAK2(self):
        """Tests Gene creation."""
        Gene.objects.create(hgnc_name='JAK2',
                            genetests=True,
                            genereviews=False)

    def test_Gene_delete_with_HBB(self):
        """Tests Gene deletion."""
        Gene.objects.get(hgnc_name='HBB').delete()
