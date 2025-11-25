import re
import openpyxl


def get_jcr(category):
    """
        get catagory of JCR
    """
    res = re.findall(r'[|(](Q\d)[)|]', category)
    return res[0] if res else ''


def parse_excel(infile):
    """
        parse excel file of JCR IF

        fields: JIF, ISSN, EISSN, JCR, ZKY, JOURNAL, JOURNAL_ABBR
    """
    wb = openpyxl.load_workbook(infile)
    ws = wb.active

    for values in ws.values:
        if values[0] is None:
            continue
        if values[0] in ('JOURNAL', 'Journal Name', 'Name'):
            title = [v.upper() for v in values]
            continue
        context = dict(zip(title, values))
        data = {}
        data['factor'] = context['JIF']
        data['issn'] = context['ISSN']
        data['eissn'] = context['EISSN']
        data['journal'] = context['JOURNAL']
        data['jcr'] = context.get('JCR')
        data['zky'] = context.get('ZKY')
        data['journal_abbr'] = context.get('JOURNAL_ABBR')

        yield data


if __name__ == '__main__':
    # for context in parse_excel('tests/2022_JCR_IF.xlsx'):
    for context in parse_excel('tests/CopyofImpactFactor2024.xlsx'):
        print(context)
