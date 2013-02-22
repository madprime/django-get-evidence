"""
==============
Variant models
==============

Functions
=========

parse_variant(variant_string):  returns gene, amino acids, and position 
                                parsed from a variant string

variant_lookup(variant_string): returns Variant object for variant string


Models
======

DbSNP
    rsid:         dbSNP ID (CharField)

Variant
    gene:         Gene from genes.models (ForeignKey)
    aa_reference: amino acid(s) for reference it this position (CharField)
    aa_position:  position of amino acid variant (IntegerField)
    aa_variant:   variant amino acid(s) at this position (CharField)
    dbsnps:       DbSNP (ManyToManyField)

    Note: amino acids are recorded according to single letter codes.

VariantReview
    variant:      Variant (OneToOneField)
    review_long:  text containing variant interpretation (CharField)

"""

import re
from django.db import models
from genes.models import Gene


VARIANT_RE = r'^([A-Z0-9]+)-([A-Z]+)([0-9]+)([A-Z]+)$'


def parse_variant(variant_string):
    """Parse variants identified by gene and amino acid change.

    Examples: HBB-E7V, APOE-C130R

    The first part before the dash is the HGNC gene symbol.
    After the dash is the reference amino acid, the amino acid position,
    and the variant amino acid.

    """
    assert re.match(VARIANT_RE, variant_string)
    parsed = re.match(VARIANT_RE, variant_string).groups()
    return { 'gene_name': parsed[0],
             'aa_ref': parsed[1],
             'aa_pos': int(parsed[2]),
             'aa_var': parsed[3],
             }


def variant_lookup(variant_string):
    """Find and return Variant in database matching identifying string."""
    var_parse = parse_variant(variant_string)
    var_match = Variant.objects.get(
        gene__hgnc_name__exact=var_parse['gene_name'],
        aa_reference__exact=var_parse['aa_ref'],
        aa_position__exact=var_parse['aa_pos'],
        aa_variant__exact=var_parse['aa_var'],
        )
    return var_match


class DbSNP(models.Model):
    """Contains dbSNP information.

    dbSNP IDs are a separate class with a many-to-many mapping because
    (1) some variants have multiple dbSNP IDs mapped to the same
    location, (2) dbSNP IDs refer to a position and some have more
    than two alleles (e.g. triallelic)

    Data attributes:
    rsid: dbSNP identifier (CharField)

    """

    rsid = models.CharField(max_length = 16)

    def __unicode__(self):
        """Returns string with dbSNP identifier."""
        return self.rsid


class Variant(models.Model):
    """Tracks immutable variant data.
    
    Data attributes:
    gene:         Gene from genes.models
    aa_reference: amino acid(s) for reference it this position
    aa_position:  position of amino acid variant
    aa_variant:   variant amino acid(s) at this position
    dbsnps:       DbSNP (ManyToManyField)
    
    The combination of gene, aa_reference, aa_position, and aa_variant 
    is required to be unique.

    """
    gene = models.ForeignKey(Gene)

    aa_reference = models.CharField(
        max_length = 10,
        verbose_name='reference amino acid',
        )
    aa_position = models.IntegerField(
        verbose_name='amino acid position',
        )
    aa_variant = models.CharField(
        max_length = 10,
        verbose_name='variant amino acid',
        )
    dbsnps = models.ManyToManyField(DbSNP)

    class Meta:
        unique_together = (('gene', 'aa_reference', 
                            'aa_position', 'aa_variant'),)

    def __unicode__(self):
        """Returns string with gene name and amino acid change."""
        return (self.gene.hgnc_name + '-' + self.aa_reference + 
                str(self.aa_position) + self.aa_variant)

    name = property(__unicode__)


class VariantReview(models.Model):
    """Tracks user-editable data for a variant.

    Data attributes:
    variant:     Variant (OneToOneField)
    review_long: text containing variant interpretation (CharField)

    """
    variant = models.OneToOneField(Variant)

    review_long = models.TextField()

    def __unicode__(self):
        """Returns text containing long variant review."""
        return self.review_long
