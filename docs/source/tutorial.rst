=========
Tutorials
=========

``build``
=========

Download NCBI Journals
----------------------

`NCBI Journal List`_

.. _NCBI Journal List: https://www.ncbi.nlm.nih.gov/books/NBK3827/table/pubmedhelp.T.journal_lists/

download with ``wget``::

    wget -c ftp://ftp.ncbi.nih.gov/pubmed/J_Entrez.gz
    wget -c ftp://ftp.ncbi.nih.gov/pubmed/J_Medline.gz

.. note::
    You can also download the journals from browser, or you can speed up with ``ascp``


Build the Database
------------------

.. code:: console

    impact_factor build -ef J_Entrez.gz -mf J_Medline.gz -t 32

.. note::
    * ``--threads N`` parameter can be used to speed up building
    * ``--echo`` parameter will show the detail processing of building



``version``
===========

Show the informations of database

.. code:: console

    impact_factor version

might shown as follows::

    ==========================================================
    program version:    1.0.0
    database version:   2020 [2020-08-20 15:32:34.141140]
    total journals:     9167
    indexed journals:   8714
    database filepath:  /data/work/suqingdong/code/impact_factor/impact_factor/data/impact_factor.db
    ==========================================================

``search``
==========

* search with ISSN::

    impact_factor search 0028-0836

* search with NLM_ID::

    impact_factor search 0410462

* search with Journal Name::

    impact_factor search nature

* like search with Journal Name::

    impact_factor search "nature com%"


``pubmed_filter``
=================

IF >= 30::

    impact_factor pubmed_filter -min 30
    
IF <= 1::

    impact_factor pubmed_filter -min 1

5 <= IF <= 10::

    impact_factor pubmed_filter -min 5 -max 10

save result to a file::

    impact_factor pubmed_filter -min 5 -max 10 -o 5_10.txt


use as a module
===============
.. code:: python

    from impact_factor import ImpactFactor

    IF = ImpactFactor()

    IF.check_version()

    IF.search('nature')

    IF.search('nature com%')

    IF.pubmed_filter(min_value=30)

    IF.pubmed_filter(min_value=5, max_value=10)
