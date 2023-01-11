[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4005636.svg)](https://doi.org/10.5281/zenodo.4005636)
[![Downloads](https://pepy.tech/badge/impact-factor)](https://pepy.tech/project/impact-factor)
![PyPI - License](https://img.shields.io/pypi/l/mi?style=plastic)
![PyPI](https://img.shields.io/pypi/v/impact_factor)
![PyPI - Status](https://img.shields.io/pypi/status/impact_factor)


# Impact Factor Toolkits

## Installation
```bash
python3 -m pip -U install impact_factor
```

## Use in CMD
### `help`
```bash
IF -h
# or
impact_factor -h
```

### `build`
> build/update the database
```bash
# optional, only required when you need build or update the database
IF build
```

### `search`
> search with `journal`, `journal_abbr`, `issn`, `eissn` or `nlm_id`
```bash
IF search nature         # search journal
IF search 'nature c%'    # like search journal
IF search 0028-0836      # search ISSN
IF search 1476-4687      # search eISSN
IF search 0410462        # search nlm_id
IF search nature --color # colorful output
```

### `filter`
> filter `factor` with `min_value` and `max_value`
```bash
IF filter -m 100 -M 200 --color

# output with pubmed filter format
IF filter -m 100 -M 200 --pubmed-filter
```

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
