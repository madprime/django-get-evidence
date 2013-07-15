"""
Tests models.py in genes app.
"""

from django.test import TestCase
from ..models import Gene

class GenesModelsTest(TestCase):
    """Tests models in models.py"""

    def setUp(self):
        Gene.objects.get_or_create(hgnc_symbol='HBB',
                                   hgnc_id='4827',
                                   ucsc_knowngene='uc001mae.1',
                                   ncbi_gene_id='3043',
                                   mim_id='141900',
                                   clinical_testing=True)

    def test_Gene_create_with_JAK2(self):
        """Tests Gene creation."""
        Gene.objects.create(hgnc_symbol='JAK2',
                            hgnc_id='6192',
                            ucsc_knowngene='uc003ziw.3',
                            ncbi_gene_id='3717',
                            mim_id='147796',
                            clinical_testing=True)

    def test_Gene_delete_with_HBB(self):
        """Tests Gene deletion."""
        Gene.objects.get(hgnc_symbol='HBB').delete()
