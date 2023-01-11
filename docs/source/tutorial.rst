=========
Tutorials
=========

``build``
=========

build the database
------------------

.. code:: console

    impact_factor build # default

    impact_factor -d test.db build -i IF.xlsx

.. note::
    * ``-d dbfile`` specify a dbfile
    * ``-i excel``  specify a excel file


``search``
==========

search the database
-------------------

* search with ISSN::

    impact_factor search 0028-0836

* search with NLM_ID::

    impact_factor search 0410462

* search with Journal Name::

    impact_factor search nature

* like search with Journal Name::

    impact_factor search "nature com%"


``filter``
=================

filter with factor
------------------

IF >= 30::

    impact_factor filter -min 30
    
IF <= 1::

    impact_factor filter -min 1

5 <= IF <= 10::

    impact_factor filter -min 5 -max 10

output pubmed filter format::

    impact_factor filter -min 5 -max 10 --pubmed-filter


use as a module
===============
.. code:: python

    from impact_factor.core import Factor

    fa = Factor()

    print(fa.dbfile)

    fa.search('nature')
    fa.search('nature c%')

    fa.filter(min_value=100, max_value=200)
    fa.filter(min_value=100, max_value=200, pubmed_filter=True)