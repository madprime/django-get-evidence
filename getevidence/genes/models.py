"""
===========
Gene models
===========

Functions
=========

variant_lookup(variant_string): Returns Gene object for hgnc_name string


Models
======

Gene
    hgnc_name:    HGNC gene symbol (CharField)
    genetests:    Listed in GeneTests genetic testing list (BooleanField)
    genereviews:  GeneReviews article mentions gene (BooleanField)

"""

from django.db import models


def gene_lookup(gene_name):
    """Finds and returns Gene in database based on gene symbol."""
    gene_match = Gene.objects.get(hgnc_name__exact=gene_name)
    return gene_match


class Gene(models.Model):
    hgnc_name = models.CharField(
        unique=True,
        verbose_name='HGNC gene symbol',
        max_length=30,
        )
    genetests = models.BooleanField(default=False)
    genereviews = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.hgnc_name


