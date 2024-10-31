[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7539859.svg)](https://doi.org/10.5281/zenodo.7539859)

[![Downloads](https://pepy.tech/badge/impact-factor)](https://pepy.tech/project/impact-factor)
![PyPI - License](https://img.shields.io/pypi/l/mi?style=plastic)
![PyPI](https://img.shields.io/pypi/v/impact_factor)
![PyPI - Status](https://img.shields.io/pypi/status/impact_factor)


# ***最新SCI期刊影响因子查询系统***
- *已更新 **[2024年数据](https://www.researchgate.net/publication/381580823_Journal_Citation_Reports_JCR_Impact_Factor_2024_PDF_Web_of_Science)***
- *包含JCR分区表数据*

## Installation
```bash
python3 -m pip install -U impact_factor
```

## Use in CMD
```bash
impact_factor -h
```
![](https://suqingdong.github.io/impact_factor/src/help.png)

### `build`
> build/update the database

```bash
# optional, only required when you need build or update the database
impact_factor build -i tests/IF.xlsx

# with a ncbi api_key
impact_factor build -k YOUR_NCBI_API_KEY

# use a new dbfile [*recommend*]
impact_factor -d test.db build -i tests/IF.xlsx

# without nlm_catalog
impact_factor -d test.db build -i tests/IF.xlsx -n
```

### `search`
> search with `journal`, `journal_abbr`, `issn`, `eissn` or `nlm_id`

```bash
impact_factor search nature         # search journal
impact_factor search 'nature c%'    # like search journal
impact_factor search 0028-0836      # search ISSN
impact_factor search 1476-4687      # search eISSN
impact_factor search 0410462        # search nlm_id
impact_factor search nature --color # colorful output
```

![](https://suqingdong.github.io/impact_factor/src/search.png)

### `filter`
> filter `factor` with `min_value` and `max_value`

```bash
impact_factor filter -m 100 -M 200 --color

# output with pubmed filter format
impact_factor filter -m 100 -M 200 --pubmed-filter
```

![](https://suqingdong.github.io/impact_factor/src/filter.png)

## Use in Python
```python
from impact_factor.core import Factor

fa = Factor()

print(fa.dbfile)

fa.search('nature')
fa.search('nature c%')

fa.filter(min_value=100, max_value=200)
fa.filter(min_value=100, max_value=200, pubmed_filter=True)
```

## Documents
https://impact-factor.readthedocs.io
