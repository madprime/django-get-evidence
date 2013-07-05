"""
==============
Variant models
==============

DbSNP:         Information for a dbSNP entry
Variant:       Tracks immutable variant data
VariantReview: Tracks user-editable data for a variant

"""

import re
from django.db import models
from genes.models import Gene
from publications.models import Publication


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
    # Regex validates and parses strings representing variants.
    VARIANT_RE = r'^([A-Z0-9]+)-([A-Z]+)([0-9]+)([A-Z]+)$'

    # Combination of gene and amino acid change uniquely define Variant.
    gene = models.ForeignKey(Gene)
    aa_reference = models.CharField(max_length=10,
                                    verbose_name='reference amino acid')
    aa_position = models.IntegerField(verbose_name='amino acid position')
    aa_variant = models.CharField(max_length=10,
                                  verbose_name='variant amino acid')

    # ManyToMany because dbSNP entries can be duplicate or tri-allelic.
    dbsnps = models.ManyToManyField(DbSNP)

    @classmethod
    def create(cls, gene_name=None, aa_ref=None, aa_pos=None, aa_var=None):
        gene, unused = Gene.objects.get_or_create(hgnc_name=gene_name)
        variant = cls(gene = gene,
                      aa_reference = aa_ref,
                      aa_position = aa_pos,
                      aa_variant = aa_var)
        variant.save()
        variantreview = VariantReview(variant = variant)
        variantreview.save()
        return variant

    @classmethod
    def remove(cls, variant=None):
        varrev = VariantReview.objects.get(variant=variant)
        varrev.delete()
        variant.delete()

    @classmethod
    def parse_variant(cls, variant_string):
        """Parse variants identified by gene and amino acid change.

        Examples: HBB-E7V, APOE-C130R

        The first part before the dash is the HGNC gene symbol.
        After the dash is the reference amino acid, the amino acid position,
        and the variant amino acid.
        """
        assert re.match(cls.VARIANT_RE, variant_string)
        parsed = re.match(cls.VARIANT_RE, variant_string).groups()
        return { 'gene_name': parsed[0],
                 'aa_ref': parsed[1],
                 'aa_pos': int(parsed[2]),
                 'aa_var': parsed[3],
                 }

    @classmethod
    def variant_lookup(cls, variant_string):
        """Find and return Variant in database matching identifying string."""
        var_parse = cls.parse_variant(variant_string)
        var_match = cls.objects.get(
            gene__hgnc_name__exact=var_parse['gene_name'],
            aa_reference__exact=var_parse['aa_ref'],
            aa_position__exact=var_parse['aa_pos'],
            aa_variant__exact=var_parse['aa_var'],
            )
        return var_match

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

    Non-editable data attributes:
    variant:                Variant (OneToOneField)

    Editable data attributes:
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
    publications:           Publication (ManyToManyField through
                                         VariantPublicationReview)
    """
    variant = models.OneToOneField(Variant, editable=False)

    review_summary = models.TextField(blank=True)
    review_long = models.TextField(blank=True)
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
                                                      blank=True,
                                                      choices=SCORE_CHOICES)
    evidence_functional = models.SmallIntegerField(null=True,
                                                   blank=True,
                                                   choices=SCORE_CHOICES)
    evidence_casecontrol = models.SmallIntegerField(null=True,
                                                    blank=True,
                                                    choices=SCORE_CHOICES)
    evidence_familial = models.SmallIntegerField(null=True,
                                                 blank=True,
                                                 choices=SCORE_CHOICES)
    clinical_severity = models.SmallIntegerField(null=True,
                                                 blank=True,
                                                 choices=SCORE_CHOICES)
    clinical_treatability = models.SmallIntegerField(null=True,
                                                     blank=True,
                                                     choices=SCORE_CHOICES)
    clinical_penetrance = models.SmallIntegerField(null=True,
                                                   blank=True,
                                                   choices=SCORE_CHOICES)
    # Define publications as ManyToMany through VariantPublicationReview
    publications = models.ManyToManyField(Publication,
                                          through='VariantPublicationReview')

    def __unicode__(self):
        """Returns text containing long variant review."""
        return self.review_summary


class VariantPublicationReview(models.Model):
    """Tracks user-editable variant-specific publication reviews.

    Data attributes:
    variant:       Variant
    publication:   Publication from publications.models
    summary:       review of publication's info regarding variant (TextField)

    """
    variantreview = models.ForeignKey(VariantReview)
    publication = models.ForeignKey(Publication)
    summary = models.TextField()

    class Meta:
        """Defines combination of variant and publication as unique."""
        unique_together = (('variantreview', 'publication',))

    def __unicode__(self):
        """Returns string containing variant, publication, and summary."""
        return str(self.publication) + ',' + str(self.variantreview.variant) + ':' + self.summary

    @classmethod
    def create(cls, variantreview=None, pmid=None):
        try:
            pub = Publication.pub_lookup(pmid)
        except Publication.DoesNotExist:
            pub = Publication.create(pmid=pmid)
            pub.save()
        varpubreview = cls(variantreview=variantreview, publication=pub)
        varpubreview.save()
        return varpubreview
