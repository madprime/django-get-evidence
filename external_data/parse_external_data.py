import csv
import gzip
import re
import sys

# All final data will be stored in gene_symbols.
gene_symbols = dict()

def tsv_row(line):
    return line.rstrip('\n').split('\t')

def process_hgnc_data(hgnc_data):
    hgnc_ids = dict()
    hgnc_prev_symbols = dict()
    hgnc_synonyms = dict()
    hgnc_accessions = dict()
    for row in [tsv_row(x) for x in hgnc_data]:
        hgnc_ids[row[0]] = row[1]
        gene_symbols[row[1]] = { 'hgnc_id': row[0],
                                 'hgnc_symbol': row[1],
                                 'hgnc_name': row[2] }

        if row[4]:
            prev_symbols = row[4].split(', ')
            for symbol in prev_symbols:
                if symbol in hgnc_prev_symbols:
                    hgnc_prev_symbols[symbol] = None
                else:
                    hgnc_prev_symbols[symbol] = row[1]

        if row[6]:
            synonyms = row[6].split(', ')
            for synonym in synonyms:
                if synonym in hgnc_synonyms:
                    hgnc_synonyms[synonym] = None
                else:
                    hgnc_synonyms[synonym] = row[1]

        if row[8]:
            accessions = row[8].split(', ')
            for accession in accessions:
                if accession in hgnc_accessions:
                    hgnc_accessions[accession] = None
                else:
                    hgnc_accessions[accession] = row[1]
    return hgnc_ids, hgnc_prev_symbols, hgnc_synonyms, hgnc_accessions


def process_ucsc_knowncanonical(ucsc_knowncanonical_data):
    ucsc_knowncanonical = set()
    for row in [tsv_row(x) for x in ucsc_knowncanonical_data]:
        ucsc_knowncanonical.add(row[4])
    return ucsc_knowncanonical


def process_ucsc_kgxref(ucsc_kgxref_data, ucsc_knowncanonical,
                        hgnc_accessions, hgnc_prev_symbols, hgnc_synonyms):
    for row in [tsv_row(x) for x in ucsc_kgxref_data]:
        ucsc_data = { 'ucsc_transcript': row[0] }
        if row[0] in ucsc_knowncanonical:
            ucsc_data['ucsc_canonical'] = True
        if row[4]:
            ucsc_data['ucsc_symbol'] = row[4]
        if row[1]:
            ucsc_data['ucsc_mrna'] = row[1]
        if row[7]:
            ucsc_data['ucsc_description'] = row[7]

        # Set of decisions to decide on a symbol.
        symbol = row[4]
        # Symbol uniquely associated with accession supersedes UCSC's pick.
        if row[1] in hgnc_accessions and hgnc_accessions[row[1]]:
            symbol = hgnc_accessions[row[1]]
        # If UCSC pick isn't in HGNC list: try previous symbols, then synonyms.
        if not symbol in gene_symbols:
            if symbol in hgnc_prev_symbols and hgnc_prev_symbols[symbol]:
                symbol = hgnc_prev_symbols[symbol]
            elif symbol in hgnc_synonyms and hgnc_synonyms[symbol]:
                symbol = hgnc_synonyms[symbol]

        # If we found an HGNC symbol match, add this transcript.
        if symbol in gene_symbols:
            if 'ucsc_transcripts' in gene_symbols[symbol]:
                gene_symbols[symbol]['ucsc_transcripts'].append(ucsc_data)
            else:
                gene_symbols[symbol]['ucsc_transcripts'] = [ ucsc_data ]


def resolve_ucsc_transcripts(transcript_list):
    if len(transcript_list) == 1:
        return transcript_list[0]['ucsc_transcript']
    canonical = list()

    # Return unique knowncanonical transcript if possible.
    for tx in transcript_list:
        if 'ucsc_canonical' in tx:
            canonical.append(tx)
    if len(canonical) == 1:
        return canonical[0]['ucsc_transcript']
    elif len(canonical) > 1:
        # And if there's more than one canonical, choose between these.
        transcript_list = canonical

    # Search for a transcript named something like "variant 1"
    variant1 = list()
    for tx in transcript_list:
        if 'ucsc_description' in tx and re.search('variant [Aa1]', 
                                                  tx['ucsc_description']):
            variant1.append(tx['ucsc_transcript'])
    if len(variant1) == 1:
        return variant1[0]

    # If all else failed, take the alphabetically first UCSC transcript ID.
    tx_names = list()
    for tx in transcript_list:
        tx_names.append(tx['ucsc_transcript'])
    tx_names.sort()
    return tx_names[0]


def process_ncbi_gene_info(ncbi_gene_info_data, hgnc_ids):
    ncbi_gene_info_data.next()
    ncbi_gene_ids = dict()
    for row in [tsv_row(x) for x in ncbi_gene_info_data]:
        ncbi_gene_id = row[1]
        symbol = row[2]

        # Get crossreference database IDs.
        hgnc_id = None
        mim_id = None
        dbXrefs = row[5].split('|')
        for xref in dbXrefs:
            if xref[0:5] == 'HGNC:':
                hgnc_id = xref
            if xref[0:4] == 'MIM:':
                mim_id = xref

        # Identify using HGNC IDs, since symbols can change.
        if hgnc_id in hgnc_ids:
            symbol = hgnc_ids[hgnc_id]

        if symbol in gene_symbols:
            ncbi_gene_ids[ncbi_gene_id] = symbol
            gene_symbols[symbol]['ncbi_gene_id'] = ncbi_gene_id
            if mim_id:
                gene_symbols[symbol]['mim_id'] = mim_id

    return ncbi_gene_ids


def process_ncbi_gene_testing(ncbi_gene_testing_data, ncbi_gene_ids):
    ncbi_gene_testing_data.next()
    for row in [tsv_row(x) for x in ncbi_gene_testing_data]:
        if not row[3] == 'gene':
            continue
        if row[7] in ncbi_gene_ids:
            symbol = ncbi_gene_ids[row[7]]
            if symbol in gene_symbols:
                gene_symbols[symbol]['clinical_testing'] = True


def process_acmg_recommendations(acmg_recommendations_data):
    for line in acmg_recommendations_data:
        row = line.rstrip('\n').split('\t')
        if row[0] in gene_symbols:
            gene_symbols[row[0]]['acmg_recommended'] = True


def main(outputfilename):
    with gzip.open('hgnc_gene_with_protein_product.txt.gz') as hgnc_data:
        (hgnc_ids, hgnc_prev_symbols, 
         hgnc_synonyms, hgnc_accessions) = process_hgnc_data(hgnc_data)

    with gzip.open('ucsc_hg19_knownCanonical.txt.gz') as ucsc_knowncanonical_data:
        ucsc_knowncanonical = process_ucsc_knowncanonical(ucsc_knowncanonical_data)
    with gzip.open('ucsc_hg19_kgXref.txt.gz') as ucsc_kgxref_data:
        process_ucsc_kgxref(ucsc_kgxref_data, ucsc_knowncanonical,
                            hgnc_accessions, hgnc_prev_symbols, hgnc_synonyms)

    # Resolve on a single UCSC knownGene transcript for each gene.
    # (Typically this will be the knownCanonical transcript for a locus.)
    # If there are none, remove the gene symbol.
    symbols = gene_symbols.keys()
    for symbol in symbols:
        if 'ucsc_transcripts' in gene_symbols[symbol]:
            kg_tx_id = resolve_ucsc_transcripts(gene_symbols[symbol]
                                                ['ucsc_transcripts'])
            gene_symbols[symbol]['ucsc_knowngene_id'] = kg_tx_id
            del gene_symbols[symbol]['ucsc_transcripts']
        else:
            del gene_symbols[symbol]

    with gzip.open('ncbi_homo_sapiens_gene_info.txt.gz') as ncbi_gene_info_data:
        ncbi_gene_ids = process_ncbi_gene_info(ncbi_gene_info_data, hgnc_ids)
    with open('ncbi_gene_testing_registry.txt') as ncbi_gene_testing_data:
        process_ncbi_gene_testing(ncbi_gene_testing_data, ncbi_gene_ids)
    with open('acmg_2013_recommendations_hgnc_list.txt') as acmg_recommendations_data:
        process_acmg_recommendations(acmg_recommendations_data)

    data_out = open(outputfilename, 'w')
    csv_out = csv.writer(data_out, lineterminator='\n')
    header = ['hgnc_symbol', 'hgnc_id', 'hgnc_name', 'ucsc_knowngene',
              'ncbi_gene_id', 'mim_id', 'clinical_testing', 'acmg_recommended']
    csv_out.writerow(header)

    gene_symbol_list = gene_symbols.keys()
    gene_symbol_list.sort()
    for symbol in gene_symbol_list:
        data = gene_symbols[symbol]
        data_out = [None for x in range(len(header))]
        data_out[0] = data['hgnc_symbol']
        data_out[1] = data['hgnc_id'][5:]
        data_out[2] = data['hgnc_name']
        data_out[3] = data['ucsc_knowngene_id']
        data_out[4] = data['ncbi_gene_id']
        if 'mim_id' in data:
            data_out[5] = data['mim_id'][4:]
        if 'clinical_testing' in data and data['clinical_testing']:
            data_out[6] = 'Y'
        if 'acmg_recommended' in data and data['acmg_recommended']:
            data_out[7] = 'Y'
        csv_out.writerow(data_out)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please provide output filename as an argument."
    else:
        main(sys.argv[1])
