from impact_factor.util import safe_open


def parse_journal(infile):
    with safe_open(infile) as f:
        for line in f:
            if line.startswith('-----'):
                continue
            key, value = line.strip('\n').split(':', 1)
            value = value.strip()
            if key == 'JournalTitle':
                context = {'journal': value}
            elif key == 'MedAbbr':
                context['med_abbr'] = value
            elif key == 'IsoAbbr':
                context['iso_abbr'] = value
            elif key == 'ISSN (Print)':
                context['issn'] = value
            elif key == 'ISSN (Online)':
                context['e_issn'] = value
            elif key == 'NlmId':
                context['nlm_id'] = value
                yield context


if __name__ == '__main__':
    for context in parse_journal('/data/www/data/ncbi/pubmed/journal/J_Entrez.gz'):
        print(context)
    