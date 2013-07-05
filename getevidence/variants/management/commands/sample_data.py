"""Create sample variant data for development and testing."""

from django.core.management.base import BaseCommand
from ...models import DbSNP, Variant, VariantPublicationReview, Publication

def create_HBB_E7V():
    """Create sample data for HBB-E7V."""
    # Create Variant. (Creates VariantReview and Gene if necessary.)
    try:
        v01 = Variant.variant_lookup('HBB-E7V')
    except Variant.DoesNotExist:
        v01 = Variant.create(gene_name='HBB', aa_ref='E', aa_pos=7, aa_var='V')
    # Create dbSNP and add to Variant.
    s01, unused = DbSNP.objects.get_or_create(rsid='rs334')
    if not s01 in v01.dbsnps.all():
        v01.dbsnps.add(s01)
    # In 'HBB' Gene, set GeneTests and GeneReviews to "True".
    v01.gene.genetests = True
    v01.gene.genereviews = True
    v01.gene.save()
    # Add data to VariantReview.
    v01.variantreview.review_summary = "Causes sickle cell anemia."
    v01.variantreview.evidence_computational = 1
    v01.variantreview.evidence_functional = 3
    v01.variantreview.evidence_casecontrol = 5
    v01.variantreview.evidence_familial = 5
    v01.variantreview.clinical_severity = 4
    v01.variantreview.clinical_treatability = 4
    v01.variantreview.clinical_penetrance = 5
    v01.variantreview.impact = 'pat'
    v01.variantreview.inheritance = 'rec'
    v01.variantreview.review_long = ("Most common cause of sickle-cell " +
                                     "anemia, most often found in individuals" +
                                     " with African ancestry.")
    v01.variantreview.save()
    try:
        p01 = Publication.objects.get(pmid = '10631276')
        VariantPublicationReview.objects.get(variantreview = v01.variantreview,
                                             publication = p01)
    except Publication.DoesNotExist, VariantPublicationReview.DoesNotExist:
        VariantPublicationReview.create(variantreview = v01.variantreview,
                                        pmid = '10631276')


def create_JAK2_V617F():
    """Create sample data for JAK2-V617F."""
    # Create Variant. (Creates VariantReview and Gene if necessary.)
    try:
        v02 = Variant.variant_lookup('JAK2-V617F')
    except Variant.DoesNotExist:
        v02 = Variant.create(gene_name='JAK2', aa_ref='V',
                             aa_pos=617, aa_var='F')
    # Create dbSNP and add to Variant.
    s02, unused = DbSNP.objects.get_or_create(rsid='rs77375493')
    if not s02 in v02.dbsnps.all():
        v02.dbsnps.add(s02)
    # Add data to VariantReview.
    v02.variantreview.review_long=("Acquired mutation in blood stem cells, " +
                                   "associated with increased risk of " +
                                   "myeloproliferative disorders.")
    v02.variantreview.save()


def create_sample_data():
    """Creates test data in database."""
    create_HBB_E7V()
    create_JAK2_V617F()


class Command(BaseCommand):
    help = 'Adds sample data to database'

    def handle(self, *args, **options):
        create_sample_data()
