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
    """
    wb = openpyxl.load_workbook(infile)
    ws = wb.active

    for values in ws.values:
        if values[0] is None:
            continue
        if values[0] in ('Journal Name', 'Name'):
            title = [v.upper() for v in values]
            continue
        context = dict(zip(title, values))
        data = {}
        data['factor'] = context.get('2021 JIF') or context.get('JIF')
        data['issn'] = context['ISSN'] if context['ISSN'] != 'N/A' else ''
        data['eissn'] = context['EISSN'] if context['EISSN'] != 'N/A' else ''
        data['jcr'] = get_jcr(context['CATEGORY'])
        data['journal'] = context.get('JOURNAL NAME') or context.get('NAME')

        yield data


if __name__ == '__main__':
    # for context in parse_excel('tests/2022_JCR_IF.xlsx'):
    for context in parse_excel('tests/CopyofImpactFactor2024.xlsx'):
        print(context)
