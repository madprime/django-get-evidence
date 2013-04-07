"""Create sample variant data for development and testing."""

from models import DbSNP, Gene, Variant, VariantReview

def create_HBB_E7V():
    """Create sample data for HBB-E7V."""
    g01, unused = Gene.objects.get_or_create(hgnc_name='HBB',
                                             genetests=True,
                                             genereviews=True)
    s01, unused = DbSNP.objects.get_or_create(rsid='rs334')
    try:
        v01 = Variant.objects.get(gene__id=g01.id,
                                  aa_reference='E',
                                  aa_position=7,
                                  aa_variant='V',)
    except Variant.DoesNotExist:
        v01 = Variant.objects.create(gene=g01, 
                                     aa_reference='E', 
                                     aa_position=7, 
                                     aa_variant='V')
    if not s01 in v01.dbsnps.all():
        v01.dbsnps.add(s01)

    vr01 = VariantReview.objects.create(variant=v01,
               review_summary="Causes sickle cell anemia.",
               evidence_computational=1,
               evidence_functional=3,
               evidence_casecontrol=5,
               evidence_familial=5,
               clinical_severity=4,
               clinical_treatability=4,
               clinical_penetrance=5,
               impact = 'pat',
               inheritance = 'rec',
               review_long = "Most common cause of sickle-cell anemia, most often " +
                             "found in individuals with African ancestry.")


def create_JAK2_V617F():
    """Create sample data for JAK2-V617F."""
    g02, unused = Gene.objects.get_or_create(hgnc_name='JAK2',
                                             genetests=True,
                                             genereviews=False)
    s02, unused = DbSNP.objects.get_or_create(rsid='rs77375493')
    try:
        v02 = Variant.objects.get(gene__id=g02.id,
                                  aa_reference='V',
                                  aa_position=617,
                                  aa_variant='F')
    except Variant.DoesNotExist:
        v02 = Variant.objects.create(gene=g02,
                                     aa_reference='V',
                                     aa_position=617,
                                     aa_variant='F')
    if not s02 in v02.dbsnps.all():
        v02.dbsnps.add(s02)
    try:
        vr02 = VariantReview.objects.get(variant__id=v02.id)
    except VariantReview.DoesNotExist:
        vr02 = VariantReview.objects.create(variant=v02,
               review_long="Acquired mutation in blood stem cells, " +
                           "associated with increased risk of " +
                           "myeloproliferative disorders.")


def create_sample_data():
    """Creates test data in database."""

    # Erases all old data.
    Gene.objects.all().delete()
    Variant.objects.all().delete()
    DbSNP.objects.all().delete()

    create_HBB_E7V()
    create_JAK2_V617F()

