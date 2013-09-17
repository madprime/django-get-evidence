"""Create sample variant data for development and testing."""

from django.core.management.base import BaseCommand
from django.test.client import Client
from ...models import DbSNP, Variant

def create_HBB_E7V():
    """Create sample data for HBB-E7V."""
    cl = Client()

    # Create variant if doesn't already exist via POST.
    cl.post('/variant/new',
            {'gene': 'HBB',
             'aa_reference': 'E',
             'aa_position': 7,
             'aa_variant': 'V',
             })

    # Add edit data.
    cl.post('/variant/HBB-E7V/edit',
            {'review_summary': "Sickle cell anemia.",
             'review_long': ("Most common cause of sickle-cell " +
                             "anemia, most often found in individuals" +
                             " with African ancestry."),
             'impact': 'pat',
             'inheritance': 'rec',
             'evidence_computational': '1',
             'evidence_functional': '3',
             'evidence_casecontrol': '5',
             'evidence_familial': '5',
             'clinical_severity': '4',
             'clinical_treatability': '3',
             'clinical_penetrance': '5'})

    # Create dbSNP and add to Variant.
    v01 = Variant.variant_lookup('HBB-E7V')
    s01, _ = DbSNP.objects.get_or_create(rsid='rs334')
    if not s01 in v01.dbsnps.all():
        v01.dbsnps.add(s01)
        v01.variantreview.save()

    # Add publications.
    cl.post('/variant/HBB-E7V/add_pub',
            {'pmid': '10631276'})
    cl.post('/variant/HBB-E7V/add_pub',
            {'pmid': '655188'})

    # Edit summary.
    cl.post('/variant/HBB-E7V/edit',
            {'review_summary': ("Causes Sickle Cell Disease when homozygous. " +
                                "Heterozygotes have Sickle Cell Trait."),
             'review_long': ("Often called 'E6V' -- positioning here is based " +
                             "on numbering of amino acids in initial mRNA " +
                             "translation. Post-translation modification means " +
                             "later removes the initial Methionine, changing this " + 
                             "to the 6th position."),
             'impact': 'pat',
             'inheritance': 'rec',
             'evidence_computational': '1',
             'evidence_functional': '3',
             'evidence_casecontrol': '5',
             'evidence_familial': '5',
             'clinical_severity': '4',
             'clinical_treatability': '3',
             'clinical_penetrance': '5',
             })


def create_JAK2_V617F():
    """Create sample data for JAK2-V617F."""
    cl = Client()

    # Create variant if doesn't already exist via POST.
    cl.post('/variant/new',
            {'gene': 'JAK2',
             'aa_reference': 'V',
             'aa_position': 617,
             'aa_variant': 'F',
             })

    # Create dbSNP and add to Variant.
    v02 = Variant.variant_lookup('JAK2-V617F')
    s02, unused = DbSNP.objects.get_or_create(rsid='rs77375493')
    if not s02 in v02.dbsnps.all():
        v02.dbsnps.add(s02)

    # Add edit data.
    cl.post('/variant/JAK2-V617F/edit',
            {'review_summary': '',
             'review_long': ("Acquired mutation in blood stem cells, " +
                             "associated with increased risk of " +
                             "myeloproliferative disorders."),
             'impact': 'not',
             'inheritance': 'unk',
             'evidence_computational': '',
             'evidence_functional': '',
             'evidence_casecontrol': '',
             'evidence_familial': '',
             'clinical_severity': '',
             'clinical_treatability': '',
             'clinical_penetrance': ''})


def create_SCN5A_G615E():
    """Create sample data for SCN5A-G615E."""
    cl = Client()

    # Create variant if doesn't already exist via POST.
    cl.post('/variant/new',
            {'gene': 'SCN5A',
             'aa_reference': 'G',
             'aa_position': 615,
             'aa_variant': 'E',
             })

    # Create dbSNP and add to Variant.
    v03 = Variant.variant_lookup('SCN5A-G615E')
    s03, unused = DbSNP.objects.get_or_create(rsid='rs12720452')
    if not s03 in v03.dbsnps.all():
        v03.dbsnps.add(s03)

    # Add edit data.
    cl.post('/variant/SCN5A-G615E/edit',
            {'review_summary': ("Rare, reported to be associated with long-QT " +
                                "syndrome (can cause syncopal spells, sudden " +
                                "death as a teenager / young adult), but " +
                                "observations are scattered may have some " +
                                "publication bias."),
             'review_long': '',
             'impact': 'pat',
             'inheritance': 'dom',
             'evidence_computational': '3',
             'evidence_functional': '',
             'evidence_casecontrol': '1',
             'evidence_familial': '',
             'clinical_severity': '4',
             'clinical_treatability': '3',
             'clinical_penetrance': '4'})

    # Add publications.
    cl.post('/variant/add_pub',
            {'pmid': '11997281'})
    cl.post('/variant/add_pub',
            {'pmid': '15840476'})


def create_sample_data():
    """Creates test data in database."""
    create_HBB_E7V()
    create_JAK2_V617F()
    create_SCN5A_G615E()


class Command(BaseCommand):
    help = 'Adds sample data to database'

    def handle(self, *args, **options):
        create_sample_data()
