import re
from Bio import Entrez
from django.db import models
import reversion

class Publication(models.Model):
    """Records publication information.

    Data attributes:
    pmid: Pubmed ID (IntegerField, unique)
    author_list: Comma-separated list of authors, truncated if >10 (TextField)
    title: Article title (TextField)
    pub_date: Publication date (CharField)
    journal: Title of journal, with abbreviations (CharField)
    journal_location: Volume, issue, and pagination (CharField)
    abstract: Abstract text (TextField)

    """
    pmid = models.IntegerField(unique=True)
    author_list = models.TextField(blank=True)
    title = models.TextField()
    pub_date = models.CharField(max_length=18)
    journal = models.CharField(max_length=30)
    journal_location = models.CharField(max_length=25)
    abstract = models.TextField(blank=True)

    def __unicode__(self):
        """Returns string with Pubmed ID."""
        return 'pmid:' + str(self.pmid)

    @classmethod
    def create(cls, pmid=None):
        pub = cls(pmid=pmid)
        pub.get_pubmed_data()
        return pub

    @classmethod
    def pub_lookup(cls, pmid):
        """Find and return Publication in database matching pmid string."""
        pub_match = cls.objects.get(pmid__exact=pmid)
        return pub_match

    def get_pubmed_data(self):
        """Pull and parse abstract text from NCBI."""
        Entrez.email = "mad-getevidence@printf.net"
        handle = Entrez.efetch(db="pubmed", id=str(self.pmid), retmode="xml")
        record = Entrez.parse(handle).next()

        # Author data
        authors = record['MedlineCitation']['Article']['AuthorList']
        self.author_list = ', '.join([a['LastName'] + ' ' + a['Initials']
                                 for a in authors[0:10]])
        if len(authors) > 10:
            self.author_list += ', et al.'
        else:
            self.author_list += '.'

        # Article title
        self.title = record['MedlineCitation']['Article']['ArticleTitle']

        # Date data
        date_data = record['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
        self.pub_date = date_data['Year']
        if 'Month' in date_data:
            self.pub_date += ' ' + date_data['Month']
            if 'Day' in date_data:
                self.pub_date += ' ' + date_data['Day']

        # Journal name (abbreviated)
        self.journal = record['MedlineCitation']['Article']['Journal']['ISOAbbreviation']
        self.journal = re.sub('\.','', self.journal)

        # Journal article location (volume/issue/pagination)
        journal_issue_data = record['MedlineCitation']['Article']['Journal']['JournalIssue']
        self.journal_location = ''
        if 'Volume' in journal_issue_data:
            self.journal_location += journal_issue_data['Volume']
        if 'Issue' in journal_issue_data:
            self.journal_location += "(" + journal_issue_data['Issue'] + ")"
        if ('Pagination' in record['MedlineCitation']['Article'] and
            'MedlinePgn' in record['MedlineCitation']['Article']['Pagination']):
            if self.journal_location:
                self.journal_location += ':'
            self.journal_location += record['MedlineCitation']['Article']['Pagination']['MedlinePgn']

        if ('Abstract' in record['MedlineCitation']['Article'] and
            'AbstractText' in record['MedlineCitation']['Article']['Abstract']):
            self.abstract = ' '.join([x for x in
                                      record['MedlineCitation']['Article']['Abstract']['AbstractText']])


# Register model with reversion.
reversion.register(Publication)
