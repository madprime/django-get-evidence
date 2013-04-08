"""
==============
Variant models
==============

Functions
=========

parse_variant(string):  Parse variants identified by gene and amino acid change
variant_lookup(string): Find and return Variant matching string

Models
======

DbSNP:         Information for a dbSNP entry
Variant:       Tracks immutable variant data
VariantReview: Tracks user-editable data for a variant

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
    rsid: dbSNP identifier (CharField, unique)

    """

    rsid = models.CharField(max_length=16, unique=True)

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
    aa_reference = models.CharField(max_length=10,
                                    verbose_name='reference amino acid')
    aa_position = models.IntegerField(verbose_name='amino acid position')
    aa_variant = models.CharField(max_length=10,
                                  verbose_name='variant amino acid')
    dbsnps = models.ManyToManyField(DbSNP)

    class Meta:
        """Defines combination of gene and amino acid change as unique."""
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
    variant:                Variant (OneToOneField)
    review_summary:         interpretation summary (CharField)
    review_long:            extended interpretation (CharField)
    impact:                 impact (pathogenic, benign, etc) (CharField)
    inheritance:            inheritance (recessive, dominant, etc) (CharField)
    evidence_computational: computational evidence score (SmallIntegerField)
    evidence_functional:    functional evidence score (SmallIntegerField)
    evidence_casecontrol:   case/contral evidence score (SmallIntegerField)
    evidence_familial:      familial evidence score (SmallIntegerField)
    clinical_severity:      clinical severity score (SmallIntegerField)
    clinical_treatability:  clinical treatability score (SmallIntegerField)
    clinical_penetrance:    genetic penetrance score (SmallIntegerField)
    """
    variant = models.OneToOneField(Variant, editable=False)

    review_summary = models.TextField()
    review_long = models.TextField()
    impact_choices = (('ben', 'benign'),
                      ('pat', 'pathogenic'),
                      ('pha', 'pharmacogenetic'),
                      ('pro', 'protective'),
                      ('not', 'not reviewed'))
    impact = models.CharField(max_length=3,
                              choices=impact_choices,
                              default='not' )
    inheritance_choices = (('dom', 'dominant'),
                           ('rec', 'recessive'),
                           ('oth', 'other'),
                           ('und', 'undefined in literature'),
                           ('unk', 'unknown or not review'))
    inheritance = models.CharField(max_length=3,
                                   choices=inheritance_choices,
                                   default='unk' )

    # Define evidence and clinical importance scores.
    SCORE_CHOICES = ( (-1, -1), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5) )
    evidence_computational = models.SmallIntegerField(null=True,
                                                      choices=SCORE_CHOICES)
    evidence_functional = models.SmallIntegerField(null=True,
                                                   choices=SCORE_CHOICES)
    evidence_casecontrol = models.SmallIntegerField(null=True,
                                                    choices=SCORE_CHOICES)
    evidence_familial = models.SmallIntegerField(null=True,
                                                 choices=SCORE_CHOICES)
    clinical_severity = models.SmallIntegerField(null=True,
                                                 choices=SCORE_CHOICES)
    clinical_treatability = models.SmallIntegerField(null=True,
                                                     choices=SCORE_CHOICES)
    clinical_penetrance = models.SmallIntegerField(null=True,
                                                   choices=SCORE_CHOICES)

    def __unicode__(self):
        """Returns text containing long variant review."""
        return self.review_summary
