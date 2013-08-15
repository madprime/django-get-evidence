import requests
from django.db import models
import reversion
import re

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

    def pubmed_text_parse(self):
        """Parse important information from PubMed text"""
        betweenpre = re.compile("(<pre>\n\d{1}.\s{1})(.+)(\[PubMed.+\])", flags=re.DOTALL)
        split_text = betweenpre.search(f).groups()
        split_nopre = split_text[1]
        split_nolinebreak = split_nopre.strip().replace("\n\n", " ").replace("\n"," ")
        split_everything = re.compile(
            """(?P<journal>^[A-Z]{1}[a-z]*\s*[A-Z]*[a-z]*\s*[A-Z]*[a-z]*) # Matches journal name
                                        \.\s{0,1}
                                        (?P<publishing_date>(19|20)[0-9]{2}\s{0,1}[A-Z]{0,1}[a-z]{0,2}\s{0,1}[0-9]{0,2}) # Matches publishing date
                                        ;\s{0,1}
                                        (?P<volume_and_edition>[0-9]+\([0-9]+\)) # Matches volume and edition(?)
                                        :
                                        (?P<page_numbers>[0-9]+-[0-9]*) # Matches page numbers
                                        \.\s{0,1}
                                        (doi:\s)?(?P<doi>[0-9a-z\./]+.\s)? # Matches digital object identifier, if given
                                        (Epub)?\s?(?P<EPub_date>19|20[0-9]{2}\s?[A-Z]{1}?[a-z]{2}?\s?[0-9]{1,2}?\.\s{0,1})? # Matches epublishing info, if given
                                        (?P<article_title>.+?) # Matches article title
                                        \.\s{0,1}
                                        (?P<authors>[A-Z\S]{1}[A-Za-z-\S]+\s{1}[A-Z\S]{1,2}\s?[A-Za-zI-III]{0,3}(,\s{1}[A-Z\S]{1}[A-Za-z-\S]+\s{1}[A-Z\S]{1,2}\s?[A-Za-zI-III]{0,3})*?) #Matches list of authors
                                        \.\s{0,1}
                                        (?P<lab_info>(Department|Center)?.+\s[0-9]+?-?[0-9]*?,\s[A-Z]+?) # Matches University\lab information
                                        \.\s{0,1}
                                        (Comment.+?\.\s19|20[0-9]{2}\s?[A-Z]{1}?[a-z]{2}?\s?[0-9]{1,2}?;?[0-9]+?\(?[0-9]*?\)?:?[0-9]*?-?[0-9]*?\.\s)? # Matches comment info, if given
                                        (?P<email>[A-Za-z0-9]+(\.[A-Za-z0-9]+)*@[A-Za-z0-9]+?(\.[A-Za-z0-9]+)*?.(edu|com|net|org))? # Matches contact e-mail, if given
                                        \s{0,1}
                                        (?P<abstract>.+) # Matches abstract
                                        \.\s?(PMCID)?:?\s?
                                        (?P<PMCID>PMC[0-9]+)? # Matches PMCID
                                        \s?PMID:\s{0,1}
                                        (?P<PMID>[0-9]+$) # Matches PMID
                                        """
                                        ,re.X|re.UNICODE)
        info_dictionary = split_everything.search(split_nolinebreak).groupdict()
        return info_dictionary
# Register model with reversion.
reversion.register(Publication)
