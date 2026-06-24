import re
import openpyxl


def get_jcr(category):
    """
    get catagory of JCR
    """
    res = re.findall(r"[|(](Q\d)[)|]", category)
    return res[0] if res else ""


def parse_excel(infile):
    """
    parse excel file of JCR IF

    fields: JIF, ISSN, EISSN, JCR, ZKY, JOURNAL, JOURNAL_ABBR
    """
    wb = openpyxl.load_workbook(infile)
    ws = wb.active

    title = []
    for values in ws.values:
        if values[0] in ("JOURNAL", "Journal Name", "Name", "Rank"):
            title = [str(v).upper() for v in values]
            continue
        if values[0] is None or not title:
            continue

        context = dict(zip(title, values))
        data = {}
        data["factor"] = context.get("2025 JIF", context.get("JIF"))
        data["issn"] = context["ISSN"]
        data["eissn"] = context["EISSN"]
        data["journal"] = context.get(
            "JOURNAL", context.get("JOURNAL NAME", context.get("NAME"))
        )
        data["jcr"] = context.get("JIF QUARTILE", context.get("JCR"))
        data["zky"] = context.get("ZKY")
        data["journal_abbr"] = context.get(
            "ABBREVIATED JOURNAL", context.get("JOURNAL_ABBR")
        )

        yield data


if __name__ == "__main__":
    for context in parse_excel("tests/CopyofImpactFactor2024.xlsx"):
        print(context)
