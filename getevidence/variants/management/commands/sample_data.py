"""Create sample variant data for development and testing."""

from django.core.management.base import BaseCommand
from ...models import DbSNP, Variant, VariantPublicationReview
from ...models import Gene, Publication

def create_HBB_E7V():
    """Create sample data for HBB-E7V."""
    # Create Variant and VariantReview. Genes should be already loaded.
    try:
        v01 = Variant.variant_lookup('HBB-E7V')
    except Variant.DoesNotExist:
        v01 = Variant.create(gene_name='HBB', aa_ref='E', aa_pos=7, aa_var='V')
    # Create dbSNP and add to Variant.
    s01, unused = DbSNP.objects.get_or_create(rsid='rs334')
    if not s01 in v01.dbsnps.all():
        v01.dbsnps.add(s01)
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
    # Add publications.
    try:
        p01 = Publication.objects.get(pmid = '10631276')
        VariantPublicationReview.objects.get(variantreview = v01.variantreview,
                                             publication = p01)
    except Publication.DoesNotExist, VariantPublicationReview.DoesNotExist:
        VariantPublicationReview.create(variantreview = v01.variantreview,
                                        pmid = '10631276')


def create_JAK2_V617F():
    """Create sample data for JAK2-V617F."""
    # Create Variant and VariantReview. Genes should be already loaded.
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


def create_SCN5A_G615E():
    """Create sample data for SCN5A-G615E."""
    # Create Variant and VariantReview. Genes should be already loaded.
    try:
        v03 = Variant.variant_lookup('SCN5A-G615E')
    except Variant.DoesNotExist:
        v03 = Variant.create(gene_name='SCN5A', aa_ref='G',
                             aa_pos=615, aa_var='E')
    # Create dbSNP and add to Variant.
    s03, unused = DbSNP.objects.get_or_create(rsid='rs12720452')
    if not s03 in v03.dbsnps.all():
        v03.dbsnps.add(s03)
    # Add data to VariantReview.
    v03.variantreview.review_summary=(
        "Rare, reported to be associated with long-QT syndrome (can cause " +
        "syncopal spells, sudden death as a teenager / young adult), but " +
        "observations are scattered may have some publication bias.")
    v03.variantreview.evidence_computational = 3
    v03.variantreview.evidence_casecontrol = 1
    v03.variantreview.clinical_severity = 4
    v03.variantreview.clinical_treatability = 3
    v03.variantreview.clinical_penetrance = 4
    v03.variantreview.impact = 'pat'
    v03.variantreview.inheritance = 'dom'
    v03.variantreview.save()
    # Add publications.
    try:
        p03a = Publication.objects.get(pmid = '11997281')
        VariantPublicationReview.objects.get(variantreview = v03.variantreview,
                                             publication = p03a)
    except Publication.DoesNotExist, VariantPublicationReview.DoesNotExist:
        VariantPublicationReview.create(variantreview = v03.variantreview,
                                        pmid = '11997281')
    try:
        p03b = Publication.objects.get(pmid = '15840476')
        VariantPublicationReview.objects.get(variantreview = v03.variantreview,
                                             publication = p03b)
    except Publication.DoesNotExist, VariantPublicationReview.DoesNotExist:
        VariantPublicationReview.create(variantreview = v03.variantreview,
                                        pmid = '15840476')


def create_sample_data():
    """Creates test data in database."""
    create_HBB_E7V()
    create_JAK2_V617F()
    create_SCN5A_G615E()


class Command(BaseCommand):
    help = 'Adds sample data to database'

    def handle(self, *args, **options):
        create_sample_data()
