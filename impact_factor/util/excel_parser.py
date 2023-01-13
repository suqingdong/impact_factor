import re
import openpyxl


def get_jcr(category):
    """
        get catagory of JCR
    """
    res = re.findall(r'\((Q\d)\)', category)
    return res[0]


def parse_excel(infile):
    """
        parse excel file of JCR IF
    """
    wb = openpyxl.load_workbook(infile)
    ws = wb.active

    for values in ws.values:
        if values[0] is None:
            continue
        if values[0] == 'Journal Name':
            title = values
            continue
        context = dict(zip(title, values))
        data = {}
        data['factor'] = context['2021 JIF']
        data['issn'] = context['ISSN'] if context['ISSN'] != 'N/A' else ''
        data['eissn'] = context['eISSN'] if context['eISSN'] != 'N/A' else ''
        data['jcr'] = get_jcr(context['Category'])
        data['journal'] = context['Journal Name']

        yield data


if __name__ == '__main__':
    for context in parse_excel('tests/2022_JCR_IF.xlsx'):
        print(context)
