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


def gene_lookup(gene_name):
    """Returns Gene object matching gene symbol."""
    gene_match = Gene.objects.get(hgnc_name__exact=gene_name)
    return gene_match


class Gene(models.Model):
    """Contains non-user-editable gene data.

    hgnc_name:    HGNC gene symbol (CharField, unique)
    genetests:    Listed in GeneTests genetic testing list (BooleanField)
    genereviews:  GeneReviews article mentions gene (BooleanField)

    """

    hgnc_name = models.CharField(unique=True,
                                 verbose_name='HGNC gene symbol',
                                 max_length=30,)
    genetests = models.BooleanField(default=False)
    genereviews = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.hgnc_name
