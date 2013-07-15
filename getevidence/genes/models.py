"""
===========
Gene models
===========

Functions
=========

gene_lookup(variant_string): Returns Gene object matching gene symbol


Models
======

Gene: Contains non-user-editable gene data.

"""

from django.db import models


class Gene(models.Model):
    """Contains non-user-editable gene data.

    All of the following are required and required unique for all Genes.
    hgnc_symbol:    HGNC gene symbol (CharField)
    hgnc_id:        HGNC gene ID (CharField)
    ucsc_knowngene: UCSC KnownGene transcript ID (CharField)
    ncbi_gene_id:   NCBI gene ID (CharField)

    Note: Although genes typically have alternative transcripts, to avoid
    multiple alternative names for variants affecting amino acids, we
    currently have a single default transcript defined. Whenever possible,
    this is the one defined as "knownCanonical" by UCSC.

    The remaining fields are potential additional data for genes.
    mim_id:           MIM (Mendelian Inheritance in Man) ID (CharField)
    clinical_testing: Listed in NCBI's Genetic Testing Registry (BooleanField)
    acmg_recommended: In ACMG's 2013 return of data guidelines (BooleanField)

    """

    hgnc_symbol = models.CharField(unique=True,
                                   verbose_name='HGNC gene symbol',
                                   max_length=15,)
    hgnc_id = models.CharField(unique=True,
                               verbose_name='HGNC ID',
                               max_length=5,)
    ucsc_knowngene = models.CharField(unique=True,
                                      verbose_name="UCSC KnownGene transcript ID",
                                      max_length=10,)
    ncbi_gene_id = models.CharField(unique=True,
                                    verbose_name="NCBI Gene ID",
                                    max_length=9,)
    mim_id = models.CharField(blank=True,
                              verbose_name="Mendelian Inheritance in Man ID",
                              max_length=6,)
    clinical_testing = models.BooleanField(default=False)
    acmg_recommended = models.BooleanField(default=False)

    def __unicode__(self):
        return self.hgnc_symbol

    @classmethod
    def gene_lookup(cls, gene_name):
        """Find and return Gene in database matching identifying string."""
        gene_match = cls.objects.get(hgnc_symbol__exact=gene_name)
        return gene_match
