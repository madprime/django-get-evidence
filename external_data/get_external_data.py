from ftplib import FTP

# According to http://www.genenames.org/about/overview (copied 2013/07/08)
# "No restrictions are imposed on access to, or use of, the data provided by
# the HGNC, which are provided to enhance knowledge and encourage progress
# in the scientific community. The HGNC provide these data in good faith,
# but make no warranty, express or implied, nor assume any legal liability
# or responsibility for any purpose for which they are used."
hgnc_ftp = FTP('ftp.ebi.ac.uk')
hgnc_ftp.login()
# The following download is the HGNC gene symbols, which we use as gene names.
with open('hgnc_gene_with_protein_product.txt.gz', 'wb') as outfile:
    hgnc_ftp.retrbinary('RETR pub/databases/genenames/locus_types/' + 
                        'gene_with_protein_product.txt.gz', 
                        outfile.write)
hgnc_ftp.quit()

# According to ftp://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/README.txt
# (copied 2013/07/08): "All the files and tables in this directory are
# freely usable for any purpose."
ucsc_ftp = FTP('hgdownload.soe.ucsc.edu')
ucsc_ftp.login()
# The following download is the list of knownCanonical genes our genome
# interpretation uses (thus the list of all possible genes we could matchl).
# Gene objects in the Django site come from (and only from) this list.
with open('ucsc_hg19_knownCanonical.txt.gz', 'wb') as outfile:
    ucsc_ftp.retrbinary('RETR goldenPath/hg19/database/knownCanonical.txt.gz',
                        outfile.write)
# The following download links UCSC transcript IDs to HGNC Gene Symbols.
with open('ucsc_hg19_kgXref.txt.gz', 'wb') as outfile:
    ucsc_ftp.retrbinary('RETR goldenPath/hg19/database/kgXref.txt.gz',
                        outfile.write)
ucsc_ftp.quit()

# There was no data use, copyright, or licensing information found on the NCBI
# FTP site (checked 2013/07/08). We believe these files are work produced by the
# US government and thus public domain under Section 105 of the Copyright Act.
ncbi_ftp = FTP('ftp.ncbi.nih.gov')
ncbi_ftp.login()
# The following is from NCBI's Genetic Testing Registry, which tells us which
# genes have registered clinical testing (uses NCBI Gene IDs).
with open('ncbi_gene_testing_registry.txt', 'wb') as outfile:
    ncbi_ftp.retrbinary('RETR pub/GTR/data/test_condition_gene.txt', outfile.write)
# The following download links NCBI Gene IDs with HGNC Gene Symbols.
with open('ncbi_homo_sapiens_gene_info.txt.gz', 'wb') as outfile:
    ncbi_ftp.retrbinary('RETR gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz',
                        outfile.write)
# The following download links NCBI Gene IDs with MIM IDs.
with open('ncbi_mim2gene.txt', 'wb') as outfile:
    ncbi_ftp.retrbinary('RETR gene/DATA/mim2gene', outfile.write)
ncbi_ftp.quit()
