import requests
from django.db import models
import reversion

class Publication(models.Model):
    """Records publication information.

    Data attributes:
    pmid: Pubmed ID (CharField, unique)
    review: general summary of paper (TextField)

    """
    pmid = models.CharField(max_length=16, unique=True)
    pubmed_text = models.TextField()    

    def __unicode__(self):
        """Returns string with Pubmed ID."""
        return 'pmid:' + self.pmid

    @classmethod
    def create(cls, pmid=None):
        pub = cls(pmid=pmid)
        pub.get_pubmed_text()
        return pub

    @classmethod
    def pub_lookup(cls, pmid):
        """Find and return Publication in database matching pmid string."""
        pub_match = cls.objects.get(pmid__exact=pmid)
        return pub_match

    def get_pubmed_text(self):
        """Pull abstract text from NCBI."""
        req = requests.get('http://www.ncbi.nih.gov/pubmed/' + 
                           self.pmid + '?format=text')
        if req.status_code == 200:
            self.pubmed_text = req.text

# Register model with reversion.
reversion.register(Publication)
